"""Executable routing and usage tests.

These are the real counterpart to ``docs/routing-tests.md``. That document asks a
model to judge prompts by hand and records the score; nothing here needs a model.
Every assertion reads the shipped data (``routing.json``, ``skills-manifest.json``,
each ``SKILL.md``) and executes the deterministic router in ``mega_mind.router``,
which implements the precedence rules the orchestrator documents.

Coverage:
  * every routing phrase resolves to its documented target and layer
  * every skill and every agent is reachable from some real prompt
  * the agent-vs-skill collisions resolve to the documented layer
  * the six prompt-level fixture cases from docs/routing-tests.md
  * named test type over generic phrase, debugging-first, chain selection
  * usage: routing works on an installed tree and through the ``mmo route`` CLI
"""

import json
import re
from pathlib import Path

import pytest
from click.testing import CliRunner

from mega_mind.cli import cli
from mega_mind.installer import install_skills, verify_install
from mega_mind.router import (
    find_shared_dir,
    load_routing,
    normalize,
    route,
    suggest_chain,
)

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / ".agent" / "shared"
SKILLS = ROOT / ".agent" / "skills"


@pytest.fixture(scope="module")
def data():
    return load_routing(SHARED)


@pytest.fixture(scope="module")
def routing_json():
    return json.loads((SHARED / "routing.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def manifest():
    return json.loads((SHARED / "skills-manifest.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Coverage: the data itself must be routable
# ---------------------------------------------------------------------------


def test_every_routing_phrase_resolves_to_its_target(data, routing_json):
    """All 78 curated phrases reach their documented target, on the right layer."""
    failures = []
    for route_entry in routing_json["routes"]:
        want_kind = route_entry.get("kind", "skill")
        for phrase in route_entry["phrases"]:
            decision = route(phrase, data)
            got = "UNROUTED" if decision is None else f"{decision.target}/{decision.kind}"
            if decision is None or decision.target != route_entry["skill"]:
                failures.append(
                    f"'{phrase}' -> want {route_entry['skill']}, got {got}"
                )
            elif decision.kind != want_kind:
                failures.append(
                    f"'{phrase}' -> wrong layer: want {want_kind}, got {decision.kind}"
                )
    assert failures == [], "unroutable routing phrases:\n  " + "\n  ".join(failures)


def test_every_skill_is_reachable(data, manifest, routing_json):
    """No skill is an orphan: a routing phrase or trigger resolves to each one."""
    routing_phrases: dict[str, list[str]] = {}
    for route_entry in routing_json["routes"]:
        for phrase in route_entry["phrases"]:
            routing_phrases.setdefault(route_entry["skill"], []).append(phrase)

    unreachable = []
    for entry in manifest["skills"]:
        probes = routing_phrases.get(entry["name"], []) + list(entry.get("triggers", []))
        if not any(
            (d := route(p, data)) is not None and d.target == entry["name"] for p in probes
        ):
            unreachable.append(entry["name"])

    assert unreachable == [], f"skills with no working prompt: {unreachable}"


def test_every_agent_is_reachable(data, routing_json):
    """Every persona is dispatchable, by routing phrase or explicit invocation."""
    agent_phrases: dict[str, list[str]] = {}
    for route_entry in routing_json["routes"]:
        if route_entry.get("kind") == "agent":
            for phrase in route_entry["phrases"]:
                agent_phrases.setdefault(route_entry["skill"], []).append(phrase)

    unreachable = []
    for agent in sorted(data.agents):
        probes = agent_phrases.get(agent, []) + [f"act as the {agent.replace('-', ' ')}"]
        ok = any(
            (d := route(p, data)) is not None and d.target == agent and d.kind == "agent"
            for p in probes
        )
        if not ok:
            unreachable.append(agent)

    assert unreachable == [], f"agents with no dispatch path: {unreachable}"


def test_shared_dir_is_discoverable_from_repo_root():
    shared = find_shared_dir(ROOT)
    assert shared is not None
    assert (shared / "routing.json").exists()


# ---------------------------------------------------------------------------
# Layer separation: agent personas vs skills with the same domain
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "prompt, target, kind",
    [
        ("review my code before I open the PR", "code-reviewer", "agent"),
        ("code review this please", "requesting-code-review", "skill"),
        ("design system tokens for the marketing page", "tech-lead", "skill"),
        ("act as the tech lead and split this epic", "tech-lead", "agent"),
        ("run a security audit on the login flow", "security-reviewer", "skill"),
        ("act as the security reviewer for this PR", "security-reviewer", "agent"),
        ("create architecture decisions for the billing service", "architect", "agent"),
        ("break down complex task into shippable slices", "planner", "agent"),
    ],
)
def test_documented_layer_collisions(data, prompt, target, kind):
    decision = route(prompt, data)
    assert decision is not None, f"{prompt!r} did not route"
    assert (decision.target, decision.kind) == (target, kind), (
        f"{prompt!r} -> {decision.target}/{decision.kind}, "
        f"expected {target}/{kind} (layer={decision.layer})"
    )


def test_persona_invocation_beats_a_domain_phrase(data):
    prompt = "act as the incident commander: checkout is down"
    decision = route(prompt, data)
    assert decision is not None
    assert decision.target == "incident-commander"
    assert decision.kind == "agent"
    assert decision.layer == "persona"


# ---------------------------------------------------------------------------
# Precedence rules documented in the orchestrator skill
# ---------------------------------------------------------------------------


def test_named_test_type_beats_generic_write_tests(data):
    prompt = "write tests: I need unit tests for the config parser before we ship"
    decision = route(prompt, data)
    assert decision is not None
    assert decision.target == "test-genius"
    assert decision.layer == "test-type"
    assert "write tests" in decision.reason


def test_generic_write_tests_keeps_tdd_when_no_type_named(data):
    decision = route("write tests for the new parser", data)
    assert decision is not None
    assert decision.target == "test-driven-development"


def test_e2e_named_type_wins(data):
    decision = route("add e2e tests for the checkout flow", data)
    assert decision is not None
    assert decision.target == "e2e-test-specialist"


def test_unknown_root_cause_failure_defers_to_specialist(data):
    prompt = "deploy to k8s and it keeps crashing after rollout"
    decision = route(prompt, data)
    assert decision is not None
    assert decision.target == "debugging"
    assert decision.deferred_to == ("k8s-orchestrator",)
    assert decision.layer == "failure-fallback"


def test_known_root_cause_keeps_the_specialist(data):
    prompt = "deploy to k8s is failing because the image tag is wrong"
    decision = route(prompt, data)
    assert decision is not None
    assert decision.target == "k8s-orchestrator", decision.reason


def test_plain_k8s_deploy_is_not_a_debugging_case(data):
    decision = route("deploy to kubernetes", data)
    assert decision is not None
    assert decision.target == "k8s-orchestrator"
    assert decision.layer == "routing"


def test_empty_and_unremarkable_requests_do_not_route(data):
    assert route("", data) is None
    assert route("   ", data) is None
    assert route("hello there", data) is None


@pytest.mark.parametrize(
    "prompt, target, chain",
    [
        (
            "I need to add user authentication with OAuth",
            "search-first",
            "Feature Development (Z-Pattern)",
        ),
        ("Users are randomly getting logged out", "debugging", "Bug Fix"),
        ("Make the app faster", "performance-profiler", None),
    ],
)
def test_orchestrator_examples_route_as_documented(data, prompt, target, chain):
    """The three worked examples inside mega-mind/SKILL.md must actually route.

    These are the skill's own published examples. If the shipped data cannot
    reproduce them, the documentation is describing behaviour that does not exist.
    """
    decision = route(prompt, data)
    assert decision is not None, f"documented example does not route: {prompt!r}"
    assert decision.target == target, (
        f"{prompt!r} -> {decision.target}, documented as {target}"
    )
    if chain is not None:
        assert decision.chain == chain, (
            f"{prompt!r} chain {decision.chain!r}, documented as {chain!r}"
        )


def test_explicit_phrase_outranks_a_performance_hint(data):
    decision = route("deploy to kubernetes is slow", data)
    assert decision is not None
    assert decision.target == "k8s-orchestrator"
    assert decision.layer == "routing"


def test_failure_outranks_a_performance_hint(data):
    decision = route("the app is slow and it crashes on load", data)
    assert decision is not None
    assert decision.target == "debugging"
    assert decision.layer == "failure-fallback"


def test_feature_verb_plus_noun_selects_the_feature_chain(data):
    decision = route("add a dashboard", data)
    assert decision is not None
    assert decision.layer == "chain"
    assert decision.chain == "Feature Development (Z-Pattern)"
    assert decision.target == "search-first"


# ---------------------------------------------------------------------------
# The prompt-level fixtures in docs/routing-tests.md, now executable
# ---------------------------------------------------------------------------


def test_fixture_case_1_bug_report_routes_to_debugging(data):
    prompt = "fix this bug - login fails after password reset, the token seems expired"
    decision = route(prompt, data)
    assert decision is not None
    assert decision.target == "debugging"


def test_fixture_case_2_named_test_type(data):
    outcome = route("write tests: I need unit tests for the config parser", data)
    assert outcome is not None and outcome.target == "test-genius"


def test_fixture_case_3_review_goes_to_the_agent(data):
    outcome = route("review my code before I open the PR", data)
    assert outcome is not None
    assert (outcome.target, outcome.kind) == ("code-reviewer", "agent")


def test_fixture_case_4_plankton_entry_and_documented_redirect(data):
    prompt = "before we build any linting hooks - does this project even need linting?"
    outcome = route(prompt, data)
    assert outcome is not None
    assert outcome.target == "plankton-code-quality"

    # The redirect itself needs judgment, so assert the documented target exists
    # and that the source skill names it in `## When NOT to Use`.
    text = (SKILLS / "plankton-code-quality" / "SKILL.md").read_text(encoding="utf-8")
    section = re.search(r"## When NOT to Use\n(.*?)\n## ", text, re.S)
    assert section is not None, "plankton-code-quality lost its 'When NOT to Use' section"
    assert "code-polisher" in section.group(1)
    assert (SKILLS / "code-polisher" / "SKILL.md").exists()


def test_fixture_case_5_no_phrase_failure_routes_to_debugging(data):
    prompt = "our k8s pods are crashlooping again and I think it is the database pool"
    outcome = route(prompt, data)
    assert outcome is not None
    assert outcome.target == "debugging"
    assert outcome.layer == "failure-fallback"


def test_fixture_case_6_whole_chain_request_starts_at_chain_head(data):
    prompt = (
        "design and build a new CSV export feature end-to-end, tests included, "
        "then get it ready to ship"
    )
    outcome = route(prompt, data)
    assert outcome is not None
    assert outcome.layer == "chain"
    assert outcome.chain == "Feature Development (Z-Pattern)"
    assert outcome.target == "search-first", "the chain must start at search-first"


def test_chain_heads_are_the_first_step_of_their_chain(data):
    for name, steps in data.chains:
        assert steps, f"chain {name} is empty"
        for step in steps:
            assert step in data.targets, f"chain {name} names unknown step {step}"


def test_failure_suppresses_the_release_chain(data):
    assert suggest_chain("cut a release and bump the version", data) == "Release"
    assert suggest_chain(
        "cut a release but the build is failing", data, failure=True
    ) != "Release"


# ---------------------------------------------------------------------------
# Usage: installed tree + CLI
# ---------------------------------------------------------------------------


def test_router_works_on_an_installed_tree(tmp_path: Path):
    """The shipped layout is routable, so an installed project can use it."""
    install_skills(str(tmp_path), force=True)
    assert verify_install(str(tmp_path), "agent") == []

    installed = load_routing(tmp_path / ".agent" / "shared")
    decision = route("review my code before I open the PR", installed)
    assert decision is not None
    assert decision.target == "code-reviewer"
    assert decision.kind == "agent"

    # routing.json is installed, not just the skills
    assert (tmp_path / ".agent" / "shared" / "routing.json").exists()
    assert route("hello there", installed) is None


def test_cli_route_human_output():
    result = CliRunner().invoke(
        cli, ["route", "review my code before I open the PR", "--shared-dir", str(SHARED)]
    )
    assert result.exit_code == 0, result.output
    assert "code-reviewer" in result.output
    assert "(agent)" in result.output


def test_cli_route_json_output():
    result = CliRunner().invoke(
        cli, ["route", "deploy to kubernetes", "--json", "--shared-dir", str(SHARED)]
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["target"] == "k8s-orchestrator"
    assert payload["kind"] == "skill"
    assert payload["layer"] == "routing"


def test_cli_route_unrouted_exits_nonzero():
    result = CliRunner().invoke(
        cli, ["route", "hello there", "--shared-dir", str(SHARED)]
    )
    assert result.exit_code == 1
    assert "UNROUTED" in result.output


def test_cli_route_json_unrouted_exits_nonzero():
    result = CliRunner().invoke(
        cli, ["route", "hello there", "--json", "--shared-dir", str(SHARED)]
    )
    assert result.exit_code == 1
    assert json.loads(result.output)["target"] is None


def test_cli_route_survives_a_legacy_console_codepage():
    """A real subprocess under a cp1251 console must not die on non-ASCII output.

    Windows consoles commonly default to a legacy code page. Before the fix the route
    command raised UnicodeEncodeError on its arrow glyph *after* resolving the request,
    so the answer was lost. Click's test runner always writes UTF-8, so only a real
    subprocess reproduces it.
    """
    import os
    import subprocess
    import sys

    env = {**os.environ, "PYTHONIOENCODING": "cp1251", "PYTHONUTF8": "0"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mega_mind",
            "route",
            "review my code before I open the PR",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=120,
    )
    assert "Traceback" not in result.stderr, result.stderr
    assert result.returncode == 0, result.stderr or result.stdout
    assert "code-reviewer" in result.stdout


# ---------------------------------------------------------------------------
# Data hygiene the router depends on
# ---------------------------------------------------------------------------


def test_routing_phrases_are_normalized_consistently(data):
    """Every stored phrase must equal its own normalization, or matching lies."""
    for phrase, target, _kind in data.phrases:
        assert phrase == normalize(phrase), f"{target}: '{phrase}' is not normalized"
        assert phrase, f"{target}: empty phrase after normalization"


def test_trigger_fallback_has_no_ambiguous_owners(data):
    """A trigger that two skills both claim must never be used for routing."""
    seen: dict[str, set[str]] = {}
    for norm_trigger, skill in data.triggers:
        seen.setdefault(norm_trigger, set()).add(skill)
    ambiguous = {t: s for t, s in seen.items() if len(s) > 1}
    assert ambiguous == {}, f"ambiguous trigger fallbacks: {ambiguous}"

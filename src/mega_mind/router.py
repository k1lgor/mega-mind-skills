"""Deterministic request router for Mega-Mind.

The routing layer used to be data plus prose: ``.agent/shared/routing.json``
held the phrases, and an agent was expected to read them and pick a target.
That made routing untestable — every check either verified that the data was
well-formed (the validator) or asked a model to judge a prompt by hand
(``docs/routing-tests.md``).

This module turns the same data into a function. It implements exactly the
precedence rules the orchestrator skill documents, so the rules can be asserted
in CI instead of trusted by reading:

  1. Explicit persona invocation ("act as the tech lead") selects the agent.
  2. A named test type beats the generic "write tests" phrase.
  3. A failing behaviour with an unknown root cause routes to ``debugging``
     first, deferring to the matched platform/domain skill.
  4. Otherwise the longest matching routing phrase wins.
  5. Unambiguous skill frontmatter triggers are a fallback, so a skill that has
     no curated routing phrase is still reachable.
  6. No match and no failure signal means the request is unrouted; callers get
     ``None`` plus a reason rather than a silent wrong answer.

Nothing here calls a model or the network.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# --- documented precedence data ------------------------------------------------

#: Generic test-writing phrase owned by test-driven-development.
GENERIC_TEST_TARGET = "test-driven-development"

#: A named test type overrides the generic phrase (mega-mind 2.1.2).
NAMED_TEST_TYPES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("test-genius", ("unit tests", "unit test", "integration tests", "integration test")),
    ("e2e-test-specialist", ("e2e tests", "e2e test", "end to end tests", "end to end test")),
    ("eval-harness", ("capability eval", "capability evals")),
)

#: A failure signal plus no known root cause routes to debugging first.
DEBUGGING = "debugging"
FAILURE_SIGNALS = (
    "crashloop",
    "crashlooping",
    "crash looping",
    "crash",
    "crashes",
    "crashing",
    "fails",
    "failing",
    "failing behaviour",
    "failed",
    "failure",
    "error",
    "errors",
    "exception",
    "traceback",
    "broken",
    "not working",
    "regression",
    "logged out",
    "getting logged out",
    "signed out",
    "keeps dropping",
    "not loading",
    "hangs",
    "freezes",
    "timed out",
    "timing out",
    "timeout",
    "500",
    "flaky",
    "segfault",
    "panic",
)

#: Fixed failure symptom words mean the root cause is already known.
KNOWN_ROOT_CAUSE = ("because", "root cause is", "caused by", "due to", "the cause is")

#: Platforms/domains that defer to debugging when the cause is unknown.
CORE_WORKFLOW_CATEGORY = "core-workflow"

PERSONA_INVOCATION = re.compile(
    r"\b(?:act as|acting as|you are|be the|switch to|as the|use the)\s+(?:an?\s+|the\s+)?([a-z0-9 \-]{3,40})"
)

#: Frontmatter triggers that appear on several skills and must never route.
AMBIGUOUS_TRIGGER_STOPWORDS = {
    "workflow",
    "workflows",
    "verify",
    "testing",
    "tests",
    "test",
    "feature",
    "production",
    "code",
    "plan",
    "review",
}

#: Ambiguous performance complaints. The orchestrator's Example 3 resolves these to
#: performance-profiler with an instruction to find the bottleneck first, because
#: "faster" alone does not say whether the bundle, the API, rendering or the CDN is at
#: fault. Encoded here so the documented behaviour is executable.
PERFORMANCE_TARGET = "performance-profiler"
PERFORMANCE_HINTS = (
    "faster",
    "slow",
    "slower",
    "sluggish",
    "laggy",
    "lag",
    "takes too long",
    "takes forever",
    "latency",
    "performance",
)

#: Feature nouns that turn a build/add verb into a whole-chain feature request
#: (orchestrator Example 1: "add user authentication with OAuth"). The point is the
#: verb+noun pair, not either half alone.
FEATURE_VERBS = ("add", "build", "implement", "create", "introduce", "ship", "support")
FEATURE_NOUNS = (
    "authentication",
    "oauth",
    "login",
    "signup",
    "sign up",
    "sso",
    "export",
    "dashboard",
    "endpoint",
    "integration",
    "feature",
    "page",
    "form",
    "api",
    "search",
    "notification",
    "billing",
    "checkout",
)

#: Chain suggestions keyed by observable request signals.
CHAIN_SIGNALS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Incident Response",
        ("outage", "sev1", "sev2", "sev3", "sev4", "incident", "postmortem", "post-mortem"),
    ),
    ("Accessibility Audit", ("wcag", "accessibility", "screen reader", "a11y", "contrast")),
    ("Adversarial Test", ("chaos", "fuzz", "fuzzing", "resilience", "adversarial")),
    ("Release", ("release", "version bump", "changelog", "rollout", "publish")),
    ("Bug Fix", ("bug", "defect", "regression", "broken", "failing")),
    ("Autoresearch / Self-Improvement", ("autoresearch", "self-improvement", "improve skills")),
    ("Autonomous Development", ("autonomous", "without intervention", "unattended")),
    ("New Project", ("greenfield", "new project", "from scratch", "boilerplate")),
    (
        "Feature Development (Z-Pattern)",
        ("feature", "implement", "build", "add support", "end-to-end", "end to end"),
    ),
)


# --- data loading -------------------------------------------------------------


@dataclass(frozen=True)
class RoutingData:
    """Routing tables loaded from an install tree (``.agent/shared`` or assets)."""

    phrases: tuple[tuple[str, str, str], ...]  # (normalized phrase, target, kind)
    personas: tuple[tuple[str, str], ...]  # (normalized name, agent name)
    triggers: tuple[tuple[str, str], ...]  # (normalized trigger, skill name)
    chain_starts: frozenset[str]
    chains: tuple[tuple[str, tuple[str, ...]], ...]
    skills: frozenset[str]
    agents: frozenset[str]

    @property
    def targets(self) -> frozenset[str]:
        return self.skills | self.agents


def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


def _has_phrase(haystack: str, needle: str) -> bool:
    return f" {needle} " in f" {haystack} "


def load_routing(shared_dir: Path) -> RoutingData:
    """Load routing.json + skills-manifest.json from a ``shared/`` directory."""
    shared_dir = Path(shared_dir)
    routing = json.loads((shared_dir / "routing.json").read_text(encoding="utf-8"))
    manifest = json.loads(
        (shared_dir / "skills-manifest.json").read_text(encoding="utf-8")
    )

    skills = frozenset(s["name"] for s in manifest["skills"])
    # Agents live next to shared/: shared/../agents/<name>.md
    agents_dir = shared_dir.parent / "agents"
    agents = frozenset(p.stem for p in agents_dir.glob("*.md")) if agents_dir.exists() else frozenset()

    phrases: list[tuple[str, str, str]] = []
    for route in routing["routes"]:
        for phrase in route["phrases"]:
            norm = normalize(phrase)
            if norm:
                phrases.append((norm, route["skill"], route.get("kind", "skill")))

    personas = tuple((normalize(a.replace("-", " ")), a) for a in sorted(agents))

    # Trigger fallback: only triggers that unambiguously own one skill.
    trigger_owners: dict[str, set[str]] = {}
    for entry in manifest["skills"]:
        for trigger in entry.get("triggers", []):
            norm = normalize(trigger)
            if not norm or norm.startswith(" ") or "/" in trigger:
                continue
            if norm in AMBIGUOUS_TRIGGER_STOPWORDS or len(norm) < 6:
                continue
            trigger_owners.setdefault(norm, set()).add(entry["name"])
    triggers = tuple(
        (norm, next(iter(owners)))
        for norm, owners in sorted(trigger_owners.items())
        if len(owners) == 1
    )

    chains = tuple((c["name"], tuple(c["steps"])) for c in routing["chains"])
    chain_starts = frozenset(steps[0] for _, steps in chains if steps)

    return RoutingData(
        phrases=tuple(phrases),
        personas=personas,
        triggers=triggers,
        chain_starts=chain_starts,
        chains=chains,
        skills=skills,
        agents=agents,
    )


def find_shared_dir(start: Path | None = None) -> Path | None:
    """Locate a ``shared/`` directory holding routing.json + the manifest.

    Checks the packaged assets first (always available in a wheel), then walks
    up from ``start`` looking for an installed ``.agent/shared``.
    """
    packaged = Path(__file__).resolve().parent / "assets" / "shared"
    if (packaged / "routing.json").exists():
        return packaged
    current = (start or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        for candidate in (
            directory / ".agent" / "shared",
            directory / ".pi" / "shared",
            directory / ".claude" / "shared",
            directory / ".codex" / "shared",
        ):
            if (candidate / "routing.json").exists():
                return candidate
    return None


# --- decision -----------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    """The resolved target for one request."""

    target: str
    kind: str  # "skill" or "agent"
    layer: str  # "routing" | "persona" | "trigger" | "failure-fallback" | "test-type"
    matched: str
    chain: str | None = None
    deferred_to: tuple[str, ...] = field(default_factory=tuple)
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "kind": self.kind,
            "layer": self.layer,
            "matched": self.matched,
            "chain": self.chain,
            "deferred_to": list(self.deferred_to),
            "reason": self.reason,
        }


def suggest_chain(text: str, data: RoutingData, failure: bool = False) -> str | None:
    """Pick a documented workflow chain from request signals, if any.

    A failure signal suppresses the Release chain: a crash during rollout is a
    bug to diagnose, not a version bump to cut.
    """
    norm = normalize(text)
    for name, signals in CHAIN_SIGNALS:
        if failure and name == "Release":
            continue
        if any(_has_phrase(norm, normalize(s)) for s in signals):
            if any(name == c[0] for c in data.chains):
                return name
    return None


def _failure_signal(norm: str) -> bool:
    return any(_has_phrase(norm, normalize(s)) for s in FAILURE_SIGNALS)


def _known_root_cause(norm: str) -> bool:
    return any(_has_phrase(norm, normalize(s)) for s in KNOWN_ROOT_CAUSE)


def _best_phrase_match(
    norm: str, data: RoutingData
) -> tuple[str, str, str, str] | None:
    """Return (target, kind, matched, layer) for the best literal match."""
    candidates: list[tuple[int, int, int, str, str, str, str]] = []

    for phrase, target, kind in data.phrases:
        if _has_phrase(norm, phrase):
            # longest phrase wins; curated routing outranks persona names
            candidates.append((len(phrase), 0, 0, phrase, target, kind, "routing"))

    for name, agent in data.personas:
        if _has_phrase(norm, name):
            candidates.append((len(name), 1, 0, name, agent, "agent", "persona"))

    if not candidates:
        # Ordered word-subsequence fallback: "fix this bug" contains "fix bug".
        tokens = norm.split()
        for phrase, target, kind in data.phrases:
            parts = phrase.split()
            if len(parts) < 2:
                continue
            pos = 0
            for token in tokens:
                if pos < len(parts) and token == parts[pos]:
                    pos += 1
            if pos == len(parts) and len(parts) >= 2 and len(tokens) <= len(parts) + 5:
                candidates.append((len(phrase), 2, 1, phrase, target, kind, "routing"))

    for phrase, skill in data.triggers:
        if _has_phrase(norm, phrase):
            candidates.append((len(phrase), 2, 2, phrase, skill, "skill", "trigger"))

    if not candidates:
        return None

    candidates.sort(key=lambda c: (-c[0], c[1], c[2], c[4]))
    _, _, _, matched, target, kind, layer = candidates[0]
    return target, kind, matched, layer


def _named_test_type(norm: str) -> tuple[str, str] | None:
    for target, phrases in NAMED_TEST_TYPES:
        for phrase in phrases:
            if _has_phrase(norm, normalize(phrase)):
                return target, phrase
    return None


def _performance_hint(norm: str) -> str | None:
    """Return the performance phrase that fired, if the request is a speed complaint."""
    for phrase in PERFORMANCE_HINTS:
        if _has_phrase(norm, normalize(phrase)):
            return phrase
    return None


def _feature_request(norm: str) -> bool:
    """True when a build/add verb is applied to a feature noun."""
    has_verb = any(_has_phrase(norm, normalize(v)) for v in FEATURE_VERBS)
    has_noun = any(_has_phrase(norm, normalize(n)) for n in FEATURE_NOUNS)
    return has_verb and has_noun


def route(text: str, data: RoutingData) -> Decision | None:
    """Resolve one request. Returns None when nothing matches."""
    norm = normalize(text)
    if not norm:
        return None

    failure = _failure_signal(norm)
    unknown_cause = failure and not _known_root_cause(norm)
    chain = suggest_chain(text, data, failure=unknown_cause)

    # 1. Explicit persona invocation: "act as the tech lead".
    invocation = PERSONA_INVOCATION.search(norm)
    if invocation:
        spoken = invocation.group(1).strip()
        for name, agent in data.personas:
            if spoken == name or spoken.startswith(name + " "):
                return Decision(
                    target=agent,
                    kind="agent",
                    layer="persona",
                    matched=spoken,
                    chain=chain,
                    reason="explicit persona invocation selects the agent, not the skill",
                )

    match = _best_phrase_match(norm, data)

    if match is None:
        # 6. No phrase: a failure with no known cause still has an owner.
        if failure:
            return Decision(
                target=DEBUGGING,
                kind="skill",
                layer="failure-fallback",
                matched="failure signal with no known root cause",
                chain=chain or "Bug Fix",
                reason="no routing phrase matched; a failing behaviour routes to debugging first",
            )

        # 6a. Ambiguous speed complaint: identify the bottleneck before choosing a
        # specialist (orchestrator Example 3).
        perf = _performance_hint(norm)
        if perf:
            return Decision(
                target=PERFORMANCE_TARGET,
                kind="skill",
                layer="hint",
                matched=perf,
                chain=chain,
                reason=(
                    f"performance complaint ('{perf}') is ambiguous about the bottleneck; "
                    "profile first, then route to the owning specialist"
                ),
            )

        # 6b. Whole-chain requests ("build this feature end-to-end") name no
        # single skill. They start at the first step of the suggested chain.
        if chain:
            steps = next((s for n, s in data.chains if n == chain), ())
            if steps:
                start = steps[0]
                return Decision(
                    target=start,
                    kind="agent" if start in data.agents else "skill",
                    layer="chain",
                    matched=chain,
                    chain=chain,
                    reason=(
                        f"no single-skill phrase matched; '{chain}' chain selected, "
                        f"starting at '{start}'"
                    ),
                )

        # 6c. A build/add verb paired with a feature noun is a feature request even
        # when no curated phrase covers the wording (orchestrator Example 1).
        if _feature_request(norm):
            steps = next(
                (s for n, s in data.chains if n == "Feature Development (Z-Pattern)"), ()
            )
            if steps:
                return Decision(
                    target=steps[0],
                    kind="agent" if steps[0] in data.agents else "skill",
                    layer="chain",
                    matched="feature request",
                    chain="Feature Development (Z-Pattern)",
                    reason=(
                        "build/add verb applied to a feature noun: run the Feature "
                        "Development chain, starting at search-first"
                    ),
                )
        return None

    target, kind, matched, layer = match

    # 2. Named test type beats the generic "write tests" phrase.
    if target == GENERIC_TEST_TARGET:
        named = _named_test_type(norm)
        if named:
            named_target, named_phrase = named
            return Decision(
                target=named_target,
                kind="skill",
                layer="test-type",
                matched=named_phrase,
                chain=chain,
                reason=(
                    f"a named test type overrides the generic phrase "
                    f"'{matched}' (mega-mind 2.1.2 precedence)"
                ),
            )

    # 3. Failure-first: a platform/domain skill must not absorb an undiagnosed failure.
    if (
        unknown_cause
        and kind == "skill"
        and target != DEBUGGING
        and target in data.skills
    ):
        return Decision(
            target=DEBUGGING,
            kind="skill",
            layer="failure-fallback",
            matched=matched,
            chain=chain or "Bug Fix",
            deferred_to=(target,),
            reason=(
                "failing behaviour with an unknown root cause: debugging runs first, "
                f"then hands off to {target}"
            ),
        )

    return Decision(
        target=target,
        kind=kind,
        layer=layer,
        matched=matched,
        chain=chain,
        reason=f"matched {layer} phrase '{matched}'",
    )


def route_from_dir(text: str, start: Path | None = None) -> Decision | None:
    """Convenience wrapper: discover routing data, then route."""
    shared = find_shared_dir(start)
    if shared is None:
        raise FileNotFoundError(
            "no routing.json found — run `mmo init` or run from the repo root"
        )
    return route(text, load_routing(shared))

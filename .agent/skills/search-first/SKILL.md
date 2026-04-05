---
name: search-first
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Research-before-coding discipline. Always search for existing solutions before writing code. Use when adding any new dependency, integration, utility, or feature that likely has prior art.
triggers:
  - "add functionality"
  - "implement a utility"
  - "search first"
  - "research before"
  - "find a library"
  - "should I use"
  - "is there a package"
---

# Search-First Skill

## Identity

You are a research-first engineering specialist. Your core belief: **the best code is code you don't have to write**. Before a single line of implementation code is written, you exhaustively search for existing solutions.

## When to Use

- Starting a new feature that likely has existing solutions
- Adding any new dependency or integration
- Before creating a new utility, helper, or abstraction
- When the user asks "add X" and you're about to write code
- Before picking a pattern from memory — verify it's still current

## When NOT to Use

- When building something genuinely novel with no prior art (new algorithm, domain-specific proprietary logic)
- When a library choice has already been made, approved, and is already a project dependency — don't re-search what's already decided
- For tiny helper functions that are 3-5 lines — the cost of installing and maintaining a dependency exceeds writing it inline
- When the task is to remove or replace an existing library — research is already done; the decision is made

## The Workflow

```
┌─────────────────────────────────────────────┐
│  1. NEED ANALYSIS                           │
│     Define what functionality is needed     │
│     Identify language/framework constraints │
├─────────────────────────────────────────────┤
│  2. PARALLEL SEARCH                         │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │  npm /   │ │  MCP /   │ │  GitHub /│  │
│     │  PyPI    │ │  Skills  │ │  Web     │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE CANDIDATES                     │
│     Score: functionality, maintenance,      │
│     community, docs, license, bundle size   │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build  │  │
│     │ as-is   │  │  /Wrap   │  │  Custom │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. IMPLEMENT                               │
│     Install package / Configure MCP /       │
│     Write minimal custom code               │
└─────────────────────────────────────────────┘
```

## Step 1: Define the Need Precisely

Before searching, write a one-sentence need statement:

```
NEED: "A [language] library that can [specific capability]
      with [constraint 1] and [constraint 2]"
```

Example:

```
NEED: "A TypeScript library that validates JSON schemas at runtime
      with good TypeScript inference and minimal bundle size"
```

## Step 2: Parallel Search Strategy

Run these searches simultaneously:

### Search Category A: Package Registries

```bash
# Node.js
npm search [keyword] --json | head -20
npx package-json-to-readme [package-name]

# Python
pip search [keyword]
pypi search [keyword]

# Check weekly downloads (popularity signal)
npm info [package] downloads
```

### Search Category B: Existing Skills/MCP

- Check if an MCP server already provides this capability
- Check if an existing skill in this system covers it
- Check `AGENTS.md` / `CLAUDE.md` / `copilot-instructions.md` / project context for established patterns

### Search Category C: Web Research

- Search GitHub for "[language] [keyword] library"
- Check awesome-[language] lists
- Search recent blog posts (filter last 12 months)

## Step 3: Evaluate Candidates

Score each candidate on this rubric:

| Criterion           | Weight | Signal                                     |
| ------------------- | ------ | ------------------------------------------ |
| Functionality match | 40%    | Does it cover 80%+ of the need?            |
| Maintenance health  | 20%    | Recent commits, open issues, response time |
| Community size      | 15%    | Stars, npm weekly downloads, PyPI monthly  |
| Documentation       | 15%    | README quality, examples, API docs         |
| License             | 5%     | MIT/Apache preferred                       |
| Bundle/dep size     | 5%     | Especially critical for frontend           |

## Step 4: Decision Matrix

| Signal                                   | Action                                         |
| ---------------------------------------- | ---------------------------------------------- |
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly           |
| Partial match (60-80%), good foundation  | **Extend** — install + write thin wrapper      |
| Multiple weak matches                    | **Compose** — combine 2-3 small packages       |
| Nothing suitable OR security concerns    | **Build** — write custom, informed by research |
| MCP server already exists for this       | **MCP** — configure and use existing server    |

## Step 5: Document Your Research

Before proceeding to implementation, output a research summary:

```markdown
## Search-First Research: [Feature Name]

### Need

[One-sentence need statement]

### Candidates Evaluated

| Package | Stars | Downloads/wk | Match% | Decision |
| ------- | ----- | ------------ | ------ | -------- |
| lib-a   | 12k   | 2M           | 95%    | ✅ Adopt |
| lib-b   | 3k    | 500k         | 60%    | ❌ Skip  |
| lib-c   | 800   | 50k          | 40%    | ❌ Skip  |

### Decision

**Action**: Adopt `lib-a`
**Rationale**: [Why this choice]
**Install**: `bun install (or npm install) lib-a`
**Caveats**: [Any known issues]
```

## Anti-Patterns to Avoid

- ❌ **Writing from scratch** without checking registry first, because you duplicate existing battle-tested logic and inherit all the bugs the library already solved, while adding maintenance burden with no differentiating value
- ❌ **Ignoring MCP** — always check if an MCP server provides the capability, because reinventing an MCP-provided tool means writing authentication, error handling, and pagination that the server already implements correctly
- ❌ **Over-customizing** — wrapping a library so heavily it loses its benefits, because deep wrapper layers make upgrades impossible without rewriting the wrapper, locking you to an old version when security patches ship
- ❌ **Dependency bloat** — installing a 500KB package for a 10-line utility, because every added dependency increases bundle size, attack surface, and the probability of a supply-chain compromise affecting your production build
- ❌ **Stale knowledge** — using a library you "remember" without checking if it's still maintained, because unmaintained packages accumulate unpatched CVEs that scanners will flag and block your CI pipeline
- ❌ **First result bias** — installing the first npm result without comparing alternatives, because the top search result is often an older package with fewer features and more open security advisories than a newer maintained alternative

## Integration Points

### With `brainstorming` skill

Run search-first **before** brainstorming approaches — knowing what's available changes which approaches are viable.

### With `mega-mind` orchestrator

The orchestrator should invoke `search-first` automatically at the start of any "implement feature" task.

### With `tech-lead` skill

Tech-lead uses search-first to populate the architecture with proven, battle-tested components instead of custom solutions.

## Search Shortcuts by Domain

### AI / LLM Integration

```
npm: @anthropic-ai/sdk, openai, @langchain, llama-index
MCP: Check mcp-servers.json for available servers
```

### Database / Data

```
npm: drizzle-orm, prisma, kysely, pg, mongoose
Python: sqlalchemy, alembic, tortoise-orm
```

### HTTP / API

```
npm: axios, ky, got, ofetch
Python: httpx, aiohttp, requests
```

### Auth

```
npm: next-auth, lucia, better-auth, clerk
Check: Does your framework (Next.js, SvelteKit) have built-in auth?
```

### Testing

```
npm: vitest, jest, playwright, @testing-library
Python: pytest, hypothesis, locust
```

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Library found but last commit is 3+ years ago, effectively unmaintained | Search ranked by stars not by recency; maintainer abandoned the project | Filter candidates to only those with a commit in the last 12 months; look for active forks or successors |
| Multiple options with similar star counts, no clear winner, analysis paralysis | Candidates evaluated on stars alone without applying the scoring rubric | Apply the full rubric (functionality 40%, maintenance 20%, community 15%, docs 15%, license 5%, bundle 5%); pick highest total score |
| Library has known CVE not yet patched, security team blocks it | Security scan skipped; CVE only visible after `npm audit` or Snyk check | Run `npm audit` / `pip-audit` immediately after install; if CVE found, evaluate a patched fork or alternative |
| License is AGPL, incompatible with proprietary product | License column skipped during evaluation; AGPL copyleft not flagged | Check the LICENSE file before any integration; AGPL requires the consuming product to also be open-source — choose MIT/Apache alternative |
| Search returns outdated Stack Overflow answer referencing deprecated API | Web search found a high-voted answer from 5+ years ago; library has since changed | Filter web search to last 12 months; cross-reference the Stack Overflow answer with the library's current official docs |

## Tips

- **Time-box your search**: 5-10 minutes max before deciding
- **Check the issue tracker**: A starred repo with 500 open issues is a red flag
- **Last commit date matters**: No commits in 2+ years = maintenance risk
- **Bundle size check**: Use bundlephobia.com for frontend packages
- **Security scan**: `rtk bun pm untrusted (or rtk npm audit)` after install, check Snyk for known CVEs

## Self-Verification Checklist

- [ ] Chosen library has a commit in the last 12 months — verified on GitHub repository's commit history
- [ ] No open CVEs: `npm audit --audit-level=high` or `pip-audit` exits 0, or all issues documented with justification
- [ ] License is compatible: `grep -c "MIT\|Apache-2.0\|BSD\|ISC" package.json` returns > 0 for the chosen library
- [ ] npm/PyPI/GitHub searched before writing implementation: `grep -c "search-first\|npm search\|pypi" task.md` returns > 0
- [ ] Top 3 candidates evaluated against scoring rubric (weekly downloads, last commit, license, bundle size)
- [ ] Decision documented in a "Search-First Research" block: `grep -c "Search-First Research\|search-first" docs/` returns > 0
- [ ] MCP server alternatives checked: `grep -c "MCP\|mcp server" task.md` returns >= 1

## Success Criteria

This skill is complete when: 1) the search has confirmed whether a suitable library exists, 2) the top candidates are scored against the rubric and the choice is documented, and 3) the decision (use library X, or build custom because Y) is recorded before any implementation begins.

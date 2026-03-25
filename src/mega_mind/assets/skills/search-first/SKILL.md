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

- ❌ **Writing from scratch** without checking registry first
- ❌ **Ignoring MCP** — always check if an MCP server provides the capability
- ❌ **Over-customizing** — wrapping a library so heavily it loses its benefits
- ❌ **Dependency bloat** — installing a 500KB package for a 10-line utility
- ❌ **Stale knowledge** — using a library you "remember" without checking if it's still maintained
- ❌ **First result bias** — installing the first npm result without comparing alternatives

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

## Tips

- **Time-box your search**: 5-10 minutes max before deciding
- **Check the issue tracker**: A starred repo with 500 open issues is a red flag
- **Last commit date matters**: No commits in 2+ years = maintenance risk
- **Bundle size check**: Use bundlephobia.com for frontend packages
- **Security scan**: `rtk bun pm untrusted (or rtk npm audit)` after install, check Snyk for known CVEs

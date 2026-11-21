# Discovery Playbook

Read this only when a task needs broad or hard-to-find solution discovery. The aim is **high recall with controlled noise**, not a fixed number of search results.

## 1. Build a solution-neutral query map

Write the user's desired behavior as a short verb-object phrase; do not embed the initially preferred protocol or implementation in every query.

Generate independent query families:

| Family | What to search | Why |
|---|---|---|
| Job-to-be-done | "tool to <achieve outcome>", "software for <user situation>" | Finds user-facing solutions |
| Capability | "<required behavior> tool", "<feature A> <feature B>" | Finds projects with different positioning |
| Mechanism | Multiple plausible architectures (CLI, extension, SDK, bridge, native capability, hosted API, etc.) | Expands beyond initial design |
| Product/delivery | "open source <outcome>", "<outcome> MCP", "<outcome> agent skill", "<outcome> SaaS" | Finds ecosystem-specific offerings |
| Synonyms & adjacent users | Different vocabulary, older names, translations, complementary workflows | Finds differently named solutions |
| Comparative / reverse | "<seed> alternatives", "<seed> vs", "like <seed>", "compare <category>" | Snowballs through competitor graph |
| Native reuse | "<target app> built in feature", official docs, extensions and changelog | Avoids external tool dependency if built-in suffices |

Translate non-English requests into relevant English search terms, but do not discard original-language sources.

### Example: user wants persistent authenticated browser access for multiple coding agents

These are **different discovery hypotheses**, not extra hard requirements:

- `shared browser persistent login multiple AI agents`
- `AI agent control existing browser tabs extension`
- `multi session browser automation CLI Windows`
- `MCP browser use authenticated Chrome profile`
- `multi-agent browser tab ownership isolation`
- `browser automation built-in feature coding assistant`

Never stop at queries containing only "CDP" or only "MCP". Search product outcomes without architecture words.

## 2. Choose sources intentionally

Use source categories relevant to the user's goal, and mark what is inaccessible.

**Primary discovery:** General web engines, GitHub repository search, GitHub code search, official directories, product category pages and relevant awesome lists.

**Software registries:** npm, PyPI, crates.io, Maven, NuGet, etc. Search *only* relevant ecosystems; do not blindly query all registries.

**Agent ecosystem:** Agent Skills catalogs (e.g. Skills.sh and GitHub `SKILL.md` search), MCP Registry, provider directories, GitHub topics, app/plugin marketplaces.

**Native solutions:** Official documentation, release notes, native commands, platform integrations and existing project dependencies.

**Alternative-signal sources:** GitHub Issues/Discussions, README "Alternatives"/"Related projects", independent comparison pages, Hacker News/Reddit posts for firsthand problems. These sources are leads/opinions, not verification.

Prefer direct canonical repo/product URLs. Deduplicate different URL mirrors, listings, forks and multiple versions of the same project.

## 3. Three-wave discovery protocol

**Wave A — diversified broad discovery**
- Search a few independent query families across available source categories, not dozens of slight variants.
- Record the query, source, date, and promising leads in a compact ledger.
- Group candidates by working mechanism, not only by popularity.
- Seek a plausible end-to-end implementation before resorting to a list of components.

**Wave B — seed expansion**
- For each leading candidate, look for its alternatives, competing products, implementation families, ecosystem integrations and referenced repositories.
- Use comparative ("X vs Y"), official ecosystem catalogs, related topics and code-search references.
- Explicitly search again **without the winner's jargon**.
- Search adjacent audiences who face the same job.

**Wave C — independent gap search**
- Look at the candidate map and ask which whole-solution families are absent.
- Search at least two decision-relevant missing families (if any).
- Try counterqueries that would falsify the leading recommendation.
- Review strong rejections for accidental keyword gating or "not documented" misinterpreted as "unsupported".
- If a newly discovered candidate materially changes the top options, extend discovery instead of finalizing immediately.

Do not treat 15–25 search hits as 15–25 *distinct* solutions. Conversely, do not make "20 candidates" an artificial pass criterion. Search effort scales with stakes and diversity.

## 4. Candidate ledger

Maintain a compact, internal working list. Externalize it when the user asks for traceability or a longer report.

```text
name | canonical URL | delivery type | mechanism family | plausible overlap
source/query | discovered in wave | status: lead / primary-verified / code-verified / tested
hard gates: met / conditional / failed / unknown | open questions
```

Separate a tool that **orchestrates** other tools from a tool that natively implements the behavior. A library or API primitive is not a turnkey product.

## 5. Coverage and stopping

A research pass may stop when:

- Important solution families have been independently searched, AND
- At least one expansion wave has tested for new categories, AND
- Further independent queries are not producing decision-changing credible candidates, OR
- The available research budget, tools or source access impose a clearly stated limit.

Record: source families searched; notable families unavailable; query-family coverage; when the search was performed; relevant omissions; next reversible search/test.

**Do not claim exhaustiveness.** "No relevant tool found within the examined sources" is valid. "No such tool exists" usually is not.

## 6. Fallback when tools are limited

Prefer the agent's connected web/GitHub tools. The optional `scripts/github_search.py` queries public GitHub repository search using Python's standard library; `GITHUB_TOKEN` or `GH_TOKEN` improves rate limits.

It does **not** search arbitrary websites, package registries, code search, or private repositories. If none of those sources is available, narrow claims accordingly. Never imply that a successful script run proves any candidate's functionality.

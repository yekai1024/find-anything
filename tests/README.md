# How to test Find Anything

A plausible report is **not** proof that this Skill improves discovery. Test the agent's behavior and the resulting candidate set.

## 1. Offline script tests

Requires Python 3.10 or later, no third-party packages and no network:

```powershell
python -m unittest discover -s tests -v
python scripts/github_search.py --help
```

These tests cover URL-independent result normalization, query provenance, deduplication, error disclosure, text escaping and CLI validation. They **do not** test GitHub's live API or whether the agent's research is good.

## 2. Blind recall benchmark

Use the scenario in [cases/shared-chrome.md](cases/shared-chrome.md). It contains the user prompt and acceptance criteria, but deliberately **no answer list**.

- Run a fresh Agent session **without** this Skill. Preserve the prompt, tool access, time limit, and candidate output.
- Run an equivalent fresh session **with** the Skill, without showing it the previous run or any gold-standard project list.
- After both finish, independently compare **canonical repo identities** against the current gold set, which must be kept **outside the agent's readable workspace/context**.
- Count recall of credible relevant existing approaches, not just raw search hits.
- Inspect false positives: attractive-looking but functionally unrelated projects, dead links, wrong platform, and invented capabilities.
- Inspect verification: how many claims have linked primary evidence, how many critical requirements remain unknown.
- Inspect design bias: did the Agent prematurely suggest custom CDP/automation infrastructure before evaluating turnkey projects?
- Record sources/tool availability, date, run budgets, actual candidates, accepted matches, missed categories, unsupported claims, and decision.

If the agent can read the gold list, the run is **not blind**. Do not bake target project names into `SKILL.md` or its examples.

## 3. Add heterogeneous scenarios

Do not optimize only for Shared Chrome. Suggested further cases:

1. Find a coding tool/Skill that explains architectural design decisions in large GitHub repositories.
2. Find a practical multi-platform public-content research tool; distinguish scraping capabilities, login requirements and service restrictions.
3. Compare existing open-source data import/conversion pipelines with a proposed custom script.

For each case preserve a separate privately held set of "important to discover" candidates, and update it as the ecosystem changes.

## 4. Suggested evaluation sheet

| Metric | How to evaluate |
|---|---|
| Important-candidate recall | Known relevant verified candidates discovered / known relevant candidates in gold set |
| Family coverage | Distinct credible solution architectures discovered / relevant known architecture families |
| Precision | Relevant plausible candidates / all promoted candidates |
| Evidence quality | Decision-changing claims with appropriate primary evidence / such claims |
| False-negative risk | Relevant alternatives rejected for missing keywords or unverified assumptions |
| Premature build | Did custom architecture appear before whole solutions were screened? |
| Decision quality | Would the recommended option pass the stated user acceptance tests? |

**Never claim numerical improvements unless repeatable runs actually establish them.** A written test case is not an executed benchmark.

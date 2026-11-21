# Report Contract and Templates

Adapt to the user's question. A short, well-supported decision is better than a long generic catalog.

## Compact answer (default)

```markdown
## 结论
[One direct sentence: best fit, conditional recommendation, or what remains unknown.]

## 最值得看的方案
| Project (canonical link) | Type / approach | Meets the job | Important constraint | Evidence |
|---|---|---|---|---|
| A | Complete product | ... | ... | Official README / source path |
| B | Different implementation family | ... | ... | ... |
| C | Component / alternative | ... | ... | ... |

## 关键差异
[Discuss the 2–4 decisive acceptance criteria, not generic feature lists.]

## 选型建议
[Adopt / Adapt / Combine / Build / Defer, and narrow next test.]

## 检索覆盖与未确认
[Sources + query families + date, gaps, source limits; avoid claiming exhaustive search.]
```

Do not overload the first screen with 20 candidates. Offer the larger pool if it adds value. For straightforward lookups, use prose instead of a table.

## Extended decision report (when stakes warrant)

1. **Decision brief:** job, exact hard gates, non-goals, acceptance tests.
2. **Search coverage:** date, source types, query families, discovery waves and newly found categories.
3. **Landscape map:** whole products, alternative mechanism families, libraries/components, native options.
4. **Candidate ledger:** unique canonical identifiers, source/evidence strength, excluded reasons.
5. **Verification matrix:** candidates × each must-have behavior; Met / Conditional / Failed / Unknown with supporting primary source links and version/date.
6. **Finalists:** strengths, weaknesses, integration steps, pricing/licensing/security and ongoing cost.
7. **Counter-search findings:** what appeared only in expansion, what was missed, remaining weak spots.
8. **Decision:** Adopt/Adapt/Combine/Build/Defer + smallest meaningful PoC.
9. **Uncertainty:** what cannot yet be verified and what observation would change the conclusion.

## Evidence language

- **Observed:** "In the tested Windows environment, X worked under Y conditions."
- **Source-verified:** "The code in <file@commit> implements X."
- **Documented:** "The official documentation says X, but no live test was performed."
- **Conditional:** "X is possible through a wrapper, not a native feature."
- **Unknown:** "No decisive evidence found for X."
- **Unsupported:** "Release notes explicitly state X is unavailable on Windows."

Cite the actual primary source with the smallest available locator. Avoid deceptive precision: a numerical score made up from intuition is not measurement.

## Search-audit mini checklist

- [ ] Started from the outcome, not an implementation.
- [ ] Searched at least three distinct mechanism families if relevant.
- [ ] Checked native/end-to-end products before designing components.
- [ ] Expanded via competitors, alternatives, related projects.
- [ ] Tested a contrary search direction.
- [ ] Read first-hand evidence for final candidates.
- [ ] Distinguished unknown from no.
- [ ] Explained why another discovery wave is / is not likely to change the decision.

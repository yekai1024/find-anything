# Evidence, Verification, and Selection

Research is useful only if the findings survive contact with the user's actual constraints.

## Evidence levels (per claim, not per project)

| Level | Meaning | Can be asserted |
|---|---|---|
| L0 — Lead | Search result, directory listing, forum mention, model memory | Only that a lead was found |
| L1 — Primary docs | Official README/docs/release notes actually read | The author documents that functionality |
| L2 — Source/tests | Relevant implementation or tests inspected, exact file/commit | The checked source/test contains supporting behavior |
| L3 — Executed | A scoped PoC actually run, with environment, results and date | Behavior observed in that tested environment |

L1 is not L3. Repo CI badges and author-reported test counts do not mean *you* executed tests. A missing description is **unknown**. Only explicit evidence supports **not supported**. Capabilities may be offered only in paid tiers, plugins or hosted versions.

For each **decision-changing** assertion, cite a canonical source and where practical the supporting section, file, line range, tag or commit. Tie version-specific or time-sensitive facts to an as-of date.

## Hard-gate status

Use four distinct statuses:

- **Met** — primary or stronger evidence satisfies the actual acceptance test.
- **Conditional** — possible through extra setup, plugin, adapter or a limitation the user may accept.
- **Failed** — direct evidence contradicts a mandatory acceptance criterion.
- **Unknown** — no adequate evidence, not a pass and not a fail.

Never filter a project because its description omitted the user's technical keyword. Inspect underlying behavior first if it could be an important candidate.

## Candidate validation checklist

For serious finalists, verify as applicable:

- Problem/feature fit: exact behavior, workflow and semantic boundary.
- Delivery shape: whole product vs SDK/API/CLI/MCP/Skill vs example/demo.
- Deployment/platform: native Windows/macOS/Linux, browser/desktop, supported runtime.
- Authentication and data: persistent state, secrets, identity boundaries, locality and hosted dependencies.
- Integration: required adapters, manual steps, cross-agent compatibility, config and operating burden.
- Concurrency/reliability: actual isolation model, failure recovery and observable diagnostics where required.
- Release/maintenance: relevant update, issues, contributors, upstream dependency fragility.
- Security/license: actual LICENSE and security posture, origin and trust of remote services.
- Cost: subscription/credits/hosting, complexity, integration/upgrade time.
- Evidence: documented, source-reviewed, executed, or unverified.

Use the user's acceptance criteria, not a generic feature-count score, to decide feasibility.

## Decide by elimination then trade-offs

1. Apply **hard gates first**, but label unresolved critical gates unknown rather than guessing.
2. For surviving finalists, compare *fit*, *implementation work*, *operational ownership*, *risk* and *portability*. Use a qualitative order unless the user requests and supports meaningful weights.
3. Consider the full system, including existing runtime/native features and glue code.
4. Choose a decision type:
   - **Adopt**: use the solution as delivered.
   - **Adapt**: small configuration, wrapper or extension.
   - **Combine**: complementary off-the-shelf components, justified integration burden.
   - **Build**: only if concrete, verified missing acceptance tests defeat feasible existing options.
   - **Defer**: unresolved material blocker; propose the smallest evidence-producing check.
5. For any Build recommendation, explicitly name the leading existing alternatives and their evidence-backed blocking gaps. Do not build a CDP proxy, scheduler, parser, auth stack or other generic subsystem merely because it is easy to imagine.

Avoid treating stars, downloads, benchmarks, popularity or a README feature checklist as a substitute for actual fit.

## Proof-of-fit checklist

Only run third-party code when authorized. For an authorized spike:

```text
Question under test:
Candidate + exact version/commit:
Environment:
Test input / acceptance steps:
Result observed:
Failure / uncertainty:
What changes in the decision:
```

Use a disposable, least-privilege environment; do not give candidate code live credentials or private files unless the user explicitly authorizes it. No PoC result should be invented.

## Adversarial review

Ask:
1. What would I have missed if I searched only the user's mechanism words?
2. Is a native end-to-end solution missing while I compare APIs and components?
3. Did I confuse "not mentioned" with "does not exist"?
4. Is the leader best only because it appeared in the first search?
5. Could my custom proposal be replaced by configuring a mature dependency?
6. Which one query or test could plausibly overturn my recommendation?

Revise the result when the answer reveals a material gap.

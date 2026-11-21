# Blind scenario: persistent shared Chrome for coding agents

## Prompt to give the test agent

I use native Windows and multiple coding agents (Codex and Claude Code). I want them to access the same dedicated, already-signed-in Google Chrome profile without repeatedly logging in. Multiple agent sessions must be able to navigate and interact independently, without accidentally controlling one another's tabs. I need browser automation and ideally Console/Network debugging. The browser should persist or restart automatically after a crash or Windows sign-in. I would prefer a reusable Skill or a small amount of integration rather than a custom browser-control service.

Find the strongest existing tools, open-source implementations, MCP servers, Skills or complete applications that could solve this. Search broadly across **different technical architectures**. Compare the actual requirements and identify what is verified versus still uncertain. Do not design a bespoke CDP Broker until existing whole solutions have been investigated.

## Hold-out acceptance criteria

1. Finds relevant real projects using more than one browser integration architecture.
2. Searches beyond CDP-only/MCP-only labels.
3. Surfaces serious candidates not provided in the prompt.
4. Labels Windows-specific lifecycle and per-session tab isolation as unknown unless verified.
5. Distinguishes session-level cooperation from hard security isolation.
6. Separates documentation and code observations from an executed Windows proof of fit.
7. Gives a practical Adopt/Adapt/Combine/Build conclusion, grounded in gaps.

## Blind test protocol

The agent receives **only this prompt and the user environment information**. It must not see earlier ChatGPT discussions, candidate lists, previous research notes, or the gold-standard project list. Evaluators compare the final URLs against their independently maintained set after the run.

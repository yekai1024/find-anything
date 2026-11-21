# Find Anything

> **Discover first. Verify next. Build only when necessary.**

**Find Anything** 是一个面向 Codex、Claude Code 等编码 Agent 的研究型 Skill。它的任务不是生成尽可能多的搜索结果，而是从你的真实需求出发，**发现现有工具、开源项目、Agent Skills、MCP、CLI、浏览器扩展、API 和成熟软件**，核实能力并帮助做技术选型。

这个项目来自一个实际问题：最初搜索“让多个 Agent 共享一个已登录 Chrome”时，如果搜索只围绕 CDP 关键词，就会遗漏通过扩展、CLI、持久化浏览器运行时等其他技术路线实现同一目标的项目。

## 设计目标

1. **从问题出发，不预设实现**：先明确要实现的结果和验收条件，而不是先设计技术架构。
2. **多路径发现**：需求词、功能词、技术机制、产品类别、竞品/替代关系、内置能力。
3. **扩大重要候选的召回率**：从最初结果沿竞品关系和不同技术路线继续扩展，避免找到两三个工具就结束。
4. **区分事实和推断**：搜索摘要 ≠ README 声明 ≠ 源码证据 ≠ 实测结果。
5. **选型而非堆目录**：提供项目链接、优劣、需求覆盖、未知条件和 Adopt / Adapt / Combine / Build 建议。
6. **避免重复造轮子**：只有关键需求确实无法通过现有产品或轻量改造实现时，才建议自研。

## 使用示例

在安装后，对 Codex 或 Claude Code 直接说：

- `$find-anything 帮我寻找能让 Codex 和 Claude Code 共享一个 Windows Chrome、保留登录态但互不干扰的现成方案。不要只找 CDP 项目。`
- `$find-anything 有哪些 Skill 或工具能帮助程序员快速理解一个大型 GitHub 项目的架构？需要比较，不只是列清单。`
- `$find-anything 比较这两个开源项目，并主动找同类替代品。结论要基于源码和实际功能，不要只看 Stars。`
- `$find-anything 我考虑开发一个工具，先帮我检索现有完整产品，再决定哪些值得自己写。`

也可以不写 `$find-anything`，直接提出相似需求；能否自动触发取决于 Agent 客户端如何发现 Skill。

## 安装：Windows PowerShell

这是一个标准 Agent Skills 文件夹。无需安装 Python 也可以使用**核心检索与选型方法**，前提是你的 Agent 能访问联网搜索工具。

### Codex（全局）

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
git clone https://github.com/yekai1024/find-anything.git "$HOME\.agents\skills\find-anything"
```

Codex 可从 `~/.agents/skills` 发现用户级 Skill。安装后通过 `$find-anything` 使用。

### Claude Code

Claude Code 如未从 `~/.agents/skills` 发现它，可以单独安装到 `~/.claude/skills`：

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/yekai1024/find-anything.git "$HOME\.claude\skills\find-anything"
```

请按你的 Claude Code 版本确认 Skill 搜索路径；不要求与 Codex 共享相同的配置文件夹。

### 更新

在对应安装目录执行：

```powershell
git -C "$HOME\.agents\skills\find-anything" pull --ff-only
```

如果同时给 Claude Code 安装了独立副本，也需要在对应目录更新。

## 文件结构

```text
find-anything/
├── SKILL.md                         # Agent 加载的核心协议
├── README.md                        # 用途、安装和示例
├── references/
│   ├── discovery-playbook.md       # 多路线搜索、竞品扩展、查漏
│   ├── evidence-and-evaluation.md  # 证据等级与技术选型
│   └── report-template.md          # 输出模板和审查清单
├── scripts/
│   └── github_search.py            # 可选：无第三方依赖的 GitHub 候选发现
└── tests/
    ├── README.md                   # 回归测试与盲测流程
    ├── cases/                      # 不包含答案的测试任务
    └── test_github_search.py       # 离线脚本单元测试
```

## 可选：本地 GitHub 搜索脚本

如果 Agent 无法直接进行 GitHub 仓库搜索，可使用标准库脚本作为**补充来源**，不是唯一搜索引擎。

```powershell
python scripts/github_search.py --query "multi agent browser persistent profile" --query "browser extension agent existing tabs" --format markdown
```

可以设置环境变量 `GITHUB_TOKEN` 或 `GH_TOKEN` 提高速率额度，但不要把 Token 写入命令行参数或提交进仓库。

脚本只查询 GitHub 的公开仓库搜索 API：它**不**搜索网页、npm、MCP Registry 或 Skill 目录，不证明候选项目的实际功能。GitHub 结果应作为线索，再由 Agent 读取一手资料验证。

## 当前阶段

**v0.1 — 方法与辅助搜索工具**。Skill 文件可直接加载；包含可选 GitHub 搜索脚本和离线单元测试。它不宣称已经通过大型真实任务的盲测，也不保证穷尽全部工具。后续改进应根据[回归案例](tests/README.md)的召回率、误报率和选型质量进行，而不是单纯增加搜索词和提示词长度。

## 参考与借鉴

方法综合了以下项目中有用、但目的不同的设计。此项目不是它们的复制或转售：

- [Tool Scout](https://github.com/LpcPaul/tool-scout-skill)：多来源搜索与候选去重。
- [GitHub Discovery](https://github.com/fulvian/github-discovery)：多渠道 GitHub 发现，不以 Stars 作为唯一质量指标。
- [Reuse-First SWE Research](https://github.com/Lu1sDV/skillsmd/tree/main/reuse-first-swe-research)：完整产品优先、复用优先、需求映射。
- [Prior-Scout](https://github.com/orange-clockwork/prior-scout)：第一手证据与谨慎表述。
- [Create / Review Existing Solutions](https://github.com/tomzx/agents)：方案调研与独立审查。
- [Superpowers / writing-skills](https://github.com/obra/superpowers)：利用失败用例验证 Skill 行为。

格式参照 [Agent Skills specification](https://agentskills.io/specification) 和 [Codex Skills documentation](https://learn.chatgpt.com/docs/build-skills)。

---

**Find anything relevant. Don't claim you've found everything.**

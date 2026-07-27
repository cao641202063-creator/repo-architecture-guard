# Repository Architecture Guard

面向产品经理和多项目开发团队的 Codex Skill。它要求 AI 在修改代码前先
核对产品目标、项目进度和代码地图，优先复用已有架构，并通过 OpenSpec、
Superpowers、TDD、用户场景测试和最新构建验证完成交付。

Repository Architecture Guard is a Codex Skill for product-goal-driven,
repository-aware software delivery.

## 主要能力

- 所有代码改动先读取 `ProjectGoal.md` 和当前项目状态。
- 生成并增量维护高密度代码地图，减少无目标的全仓扫描。
- 优先复用已有前端组件、后端方法、数据契约和测试设施。
- 非简单需求结合 OpenSpec 和 Superpowers 完成规格与计划控制。
- 行为修改使用 TDD，适用的 UI 验收使用 Playwright。
- 测试失败执行诊断、修复、重测闭环。
- 交付前验证当前最新代码构建的实际产物。
- 更新项目文档并清理已确认废弃的内容。
- 通过初始化命令安全合并现有 `AGENTS.md`，不覆盖用户已有规则。

## 环境要求

- Codex、Claude Code、Cursor 或其他兼容 Agent Skills 的工具。
- Python 3.10 或更高版本。
- Node.js/npm，仅在使用 `npx skills` 安装时需要。

运行时 Python 脚本只使用标准库。

## 安装

安装到 Codex 全局 Skill：

```powershell
npx skills add cao641202063-creator/repo-architecture-guard -g -a codex -s repo-architecture-guard -y
```

交互式选择安装目标：

```powershell
npx skills add https://github.com/cao641202063-creator/repo-architecture-guard
```

查看仓库内可安装的 Skill：

```powershell
npx skills add cao641202063-creator/repo-architecture-guard --list
```

## 更新

```powershell
npx skills update repo-architecture-guard --global --yes
```

## 初始化项目

初始化器会：

1. 收集产品名称、目标用户、业务目标、当前里程碑和成功标准。
2. 创建缺失的 `ProjectGoal.md`。
3. 创建缺失的 `docs/ai/project-status.md`。
4. 在 `AGENTS.md` 中添加或更新受控区块。
5. 保留受控区块以外的项目规则。
6. 初始化或更新 `docs/ai/code-map.json` 和 `code-map.md`。

### Windows

在目标项目根目录执行：

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\init_project.py" --root .
```

### macOS/Linux

```bash
python3 ~/.codex/skills/repo-architecture-guard/scripts/init_project.py --root .
```

### 从业务诉求文档初始化

Windows：

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\init_project.py" `
  --root . `
  --brief ".\docs\产品需求.md"
```

macOS/Linux：

```bash
python3 ~/.codex/skills/repo-architecture-guard/scripts/init_project.py \
  --root . \
  --brief ./docs/product-requirements.md
```

业务文档会作为产品输入原文保留。脚本不会把文档中未明确的内容伪装成已确认
的产品决策。

### 非交互式初始化

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\init_project.py" `
  --root . `
  --project-name "企业知识库" `
  --target-users "产品经理;实施顾问" `
  --outcome "让用户快速定位可信知识" `
  --milestone "完成首个可评审版本" `
  --success-criteria "核心检索流程通过;关键页面可用" `
  --non-goals "本阶段不接入外部计费" `
  --constraints "必须支持中文;复用现有登录体系"
```

自动化系统可以添加 `--json` 获取结构化结果。

### 文件保护规则

- 已有 `ProjectGoal.md` 默认保留；只有 `--force-goal` 才会替换。
- 已有 `project-status.md` 默认保留；只有 `--force-status` 才会替换。
- `AGENTS.md` 只修改以下标记之间的内容：

```text
<!-- repo-architecture-guard:start -->
<!-- repo-architecture-guard:end -->
```

- `--no-code-map` 可以跳过代码地图生成。

## 在 Codex 中使用

初始化后，在项目任务中输入：

```text
调用 $repo-architecture-guard，读取 ProjectGoal.md、项目状态和代码地图，
核对本次任务与产品目标，优先复用已有实现，并按适用流程完成开发和验证。
```

项目根目录 `AGENTS.md` 已经包含强制调用规则，正常情况下不需要每次重复完整
Prompt。

## 代码地图命令

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" bootstrap --root .
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" check --root . --json
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" update --root .
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" render --root .
```

代码地图是导航索引，不是源码替代品。AI 修改文件前仍必须阅读对应源码、调用方
和测试。

## 开发与验证

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s tests -v
python -m py_compile scripts/code_map.py scripts/init_project.py
```

GitHub Actions 会在 Windows、macOS 和 Linux 上运行测试。

## License

[MIT](LICENSE)

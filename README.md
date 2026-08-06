# Repository Architecture Guard

面向产品经理和多项目团队的 AI Coding Skill。它是所有代码改动的入口：先核对产品目标、项目状态和代码地图，再按影响面选择最轻量但足够的需求澄清、规格、实施和验证流程。

## 设计原则

- **一个入口**：任何代码改动先调用本 Skill。
- **一个事实源**：一项改动只由 Trellis 或 OpenSpec 之一保存 PRD、决策和任务。
- **按需编排**：只在需要时调用 Grill-me、Trellis、OpenSpec 或 Superpowers 的单项能力。
- **分层验证**：开发过程运行定向检查；完成后只对最终候选版本运行一次必要的广泛验证。
- **架构优先**：从代码地图找到 owner、调用方、契约、测试和文档，优先复用已有能力。

## 工作流

```text
任务
  → repo-architecture-guard：Context Gate、影响面、风险等级
  → Grill-me：仅需求/设计仍有关键不确定性
  → Trellis 或 OpenSpec：选择一个作为规格和任务事实源
  → Codex 实施；按需使用 Superpowers 的 TDD/调试/计划/验收能力
  → 定向验证 → 最终候选的一次广泛验证 → 交付
```

### 选择规则

| 场景 | 选用 |
|---|---|
| 需求模糊 | Grill-me |
| 个人或小团队的跨会话长任务 | Trellis |
| 正式协作、跨仓库或需要可审计规格 | OpenSpec |
| 需要 TDD、系统调试、计划评审或收尾证据 | 对应的 Superpowers 单项 Skill |
| 小而清晰的局部改动 | 仅 Repository Architecture Guard |

不要让 Trellis 与 OpenSpec 为同一个任务分别维护 PRD 或计划。

### 验证等级

| 等级 | 范围 | 验证 |
|---|---|---|
| L0 | 文档、机械或局部样式改动 | 相关 lint/format/build |
| L1 | 单模块局部变更 | `test:changed` + lint/type-check |
| L2 | 跨模块、UI 流程、状态、契约或共享组件 | L1 + 契约/集成 + 最终一次 `test:smoke` |
| L3 | 权限、安全、支付、迁移、共享基础设施、核心链路 | L2 + 最终一次 `test:full` + 可用时独立审计 |

建议每个项目提供 `test:changed`、`test:contract`、`test:smoke` 和 `test:full`。不要在每次编辑后跑全量回归。

## 安装

```powershell
npx skills add cao641202063-creator/repo-architecture-guard -g -a codex -s repo-architecture-guard -y
```

## 初始化项目

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\init_project.py" --root .
```

初始化器保留既有规则，只管理 `AGENTS.md` 的受控区块，并创建缺失的产品目标、项目状态和代码地图。

## 使用

```text
调用 $repo-architecture-guard。先完成 Context Gate，给出影响面和 L0–L3 风险判断；选择唯一的规格事实源，并按风险执行最小充分验证。
```

## 代码地图

```powershell
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" check --root . --json
python "$env:USERPROFILE\.codex\skills\repo-architecture-guard\scripts\code_map.py" update --root .
```

代码地图仅用于导航；修改文件前仍必须读取真实源码、调用方和测试。

# Langfuse Visual Guide — Roadmap & Status / 路线图与进度

Design spec: `docs/superpowers/specs/2026-06-26-langfuse-visual-guide-design.md`
Source maps (seed citations): `docs/superpowers/plans/source-maps/*.md`
Langfuse source under audit: `/home/verden/course/langfuse` (record commit per M-spec).

Each milestone: **M-spec → M-plan → subagent execution → audit (auto gates + completeness + SVG +
source-fidelity + dual review) → fix → commit**. See spec §6 for the audit contract.

## Status

| M | Scope | Lessons | Status |
| --- | --- | --- | --- |
| M0 | Infrastructure & design system + L01 baseline | L01 | ☑ done |
| M1 | Part 1 · 宏观全景 (finish) | L02–L05 | ☑ done |
| M2 | Part 2 · 前置基础 | L06–L11 | ☑ done |
| M3 | Part 3 · 摄取链路 | L12–L19 | ☑ done |
| M4 | Part 4 · 查询链路 | L20–L27 | ☑ done |
| M5 | Part 5 · 评估与评分 | L28–L33 | ☐ todo |
| M6 | Parts 6+7 · 数据集/实验 + Prompt/Playground | L34–L39 | ☐ todo |
| M7 | Parts 8+9 · 仪表盘/成本 + 自动化/集成 | L40–L47 | ☐ todo |
| M8 | Part 10 · 平台与运维 | L48–L53 | ☐ todo |
| M9 | Part 11 · 设计专题与终章 + 全局打磨 | L54–L55 | ☐ todo |

Legend: ☐ todo · ◐ in progress · ☑ done (built + audited + committed).

## Audit logs
Per-milestone audit records land in `docs/superpowers/plans/<date>-mN-audit.md`.

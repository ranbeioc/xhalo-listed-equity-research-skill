# Listed Equity Research Skill — 可审计上市公司深度研究

用于全球上市企业的**财报核验 → 经营与竞争 → 宏观传导 → 分行业估值 → 图表报告 → 自动质检**。这是可复制、可版本管理的 Agent Skills 标准技能目录，并非某一家公司的固定结论。

## 最快使用

1. 将 `listed-equity-research/` 放入所使用 Agent 的 skills 扫描目录（路径依宿主而定）；保证 `SKILL.md` 名称与目录名一致。
2. 对 Agent 说：**“使用 listed-equity-research，深度分析港股 3690.HK：核查3年财报、最新中报、竞争、宏观、现金流，生成带数据图和原始链接的中文研究报告与DCF。”**
3. Agent 按 `SKILL.md` 读取必要 `references/`，把证据录入 CSV，构建模型并生成 PDF/DOCX/Markdown/HTML（依工具可用性）。

本地脚本演示（Python 3.9+）：

```bash
python scripts/new_project.py --company 'Company' --ticker '3690.HK' --exchange 'HKEX' --output research/3690
python scripts/validate_research.py research/3690
# 把真实 sources/metrics/charts.json 填完，再运行绘图；需要 matplotlib
python scripts/render_charts.py research/3690
# 演示估值配置为假设数据，不能引用为证券的真实估值
python scripts/dcf_sotp.py assets/valuation.example.json --output /tmp/valuation-example-result.json
```

## 文件地图

| 路径 | 功能 |
|---|---|
| `SKILL.md` | Agent激活说明、研究全流程与硬门槛 |
| `references/evidence.md` | 来源层级、可回溯引用与证据等级 |
| `references/financials.md` | 三表、投资收益、现金流、SBC/租赁审计 |
| `references/macro-competition.md` | 竞争单位经济与宏观传导；避免重复定价 |
| `references/sector-lenses.md` | 互联网、消费、银行、保险、REIT、能源等行业适配 |
| `references/valuation.md` | DCF/SOTP/相对估值/终值与资本结构 |
| `references/reporting.md` | 图表清单、出版级报告结构及引用规范 |
| `references/quality-gates.md` | 模型一致性检查及发布门槛 |
| `references/xhalo-integration.md` | xHalo工作流集成设计（可选） |
| `assets/` | 报告模板、证据CSV模板、示例估值配置 |
| `scripts/` | 创建项目、资料检查、绘图、DCF/SOTP计算 |
| `examples/` | 美团案例方法论复盘（不带固化目标价） |

## 数据准则

**所有财务事实要有来源链接和具体页/表格；所有预测要有情景标签。** 运行程序时不要将演示JSON数据当成美团或其他上市公司实际预测。不能查询到付费投行研报时，应注明只使用公开摘要或二手资料。

## 标准兼容性

按公开的 [Agent Skills Specification](https://agentskills.io/specification) 编排，使用 `SKILL.md` YAML frontmatter 和 references/assets/scripts 的渐进式披露。各宿主安装路径和图表/文档插件能力不同，以具体环境为准。

## 补充资源及限制

- `assets/prompts.md`：5组可复用的首次覆盖/财报/宏观/估值/增量更新触发词。
- `assets/charts.example.json`：说明图表配置如何绑定 `metric_id` 和 `source_id`，字段仅为占位符。
- `scripts/self_test.py`：使用虚构数据验证整个本地流程，不依赖网络，不对真实证券做投资判断。
- `scripts/dcf_sotp.py` 仅负责FCFF/SOTP公式运算，不代替财报录入、分部预测和经济假设审核。
- 当前版本不包含完整三表公式工作簿自动生成器，也不内置PDF/DOCX导出引擎；在有相应文件工具的Agent环境中依SKILL说明生成。不能仅凭脚本通过就将报告标为 `decision-grade`。

## v1.0.1 安装包与完整性

如果目标 Agent 表示缺少 `references/`、`assets/`、`scripts/`、`examples/`，通常是只传了 `README.md` 和 `SKILL.md`。请改用**完整 ZIP**或**单文件离线安装器**，不要拆开上传。安装步骤见 [INSTALL.md](INSTALL.md)，校验命令：`python scripts/verify_install.py .`。

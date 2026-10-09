---
name: listed-equity-research
description: 对全球上市公司进行可审计的基本面、财报、行业竞争、宏观传导、资本配置和估值研究，并生成带逐项来源链接及数据图表的中文或英文投资研究报告。适用于A股、港股、美股、欧股及其他上市证券；适用于首次覆盖、财报深度复盘、DCF/SOTP/可比估值、买卖双方观点对比、风险情景、估值更新与研究报告输出。能够根据银行、保险、REIT、软件、平台、工业、消费、能源、医药等行业切换适用的财务与估值方法。
metadata:
  version: "1.0.1"
  language: "zh-CN"
  author: "Research methodology toolkit"
---

# Listed Equity Research | 上市公司深度研究与审计型报告

## 0. 目标与适用边界

你是**基于可复核证据的证券研究分析助手**。对上市公司建立财报事实、经营解释、外部竞争、宏观传导、分部模型、估值假设和投资观点之间的完整证据链，输出图文并茂、可复算、可更新的报告。将**企业价值**、**股权价值**和**每股价值**明确分开。所有预测须标注为研究假设，不能伪装成财报或投行一致预期。

适用：首次覆盖/专题、最新季报及同比环比、并购、资本开支、估值、投资风险、跟踪更新。对于非上市公司、纯债券信用分析或缺乏定价信息的资产须切换方法，不能套用本技能的标准股票估值结论。

**最高优先级硬约束**：

1. **先核验公司主体、证券代码、上市地点、报告期、货币单位和最新公告，再做计算。** 不得用媒体摘录代替正式财报；如原始披露缺失必须说清。
2. **数据结论与推断分层**：`reported` 财报原文，`official-stat` 统计，`consensus` 一致预测，`broker` 券商预测，`expert-estimate` 专家调查，`analyst-estimate` 自建估计，`derived` 明确公式，`illustrative` 演示，`unknown` 缺失。媒体/卖方转述不能提升为已披露事实。
3. **每条关键数值都需可回溯**到具体文献 URL + 发布日期 + 对应页码/表格/条款 + 口径；图表单独显示来源与截点。没有来源的数据不准放入“事实”表。
4. **禁止重复计价**：宏观与竞争冲击先映射到业务驱动，再评估折现率；现金、投资、债务、租赁、SBC、回购、递延税负不得在分部及股权桥重复计算。
5. **不给伪精确目标价**：关键分部利润、股数、净债务、估值输入缺失时仅输出 `screen-grade` 或 `not-decision-ready`，展示敏感性与欠缺证据，不宣称“精确合理价”。
6. **不能捏造报告/研报/市场数据**；没有实时工具就披露数据截止日。不要把上一版研究结果、卖方摘要或假设当作刚查证的数字。
7. **不以预设立场选择证据**：列出支持与反驳投资论点的数据，并给出触发观点变化的指标。报告提供研究判断，不替用户进行个性化投资决策。

## 1. 启动与路由

阅读对应参考文件（相对本目录）：
- 证据与溯源：[references/evidence.md](references/evidence.md)
- 会计与现金流审计：[references/financials.md](references/financials.md)
- 行业竞争和宏观：[references/macro-competition.md](references/macro-competition.md)
- 分行业方法选择：[references/sector-lenses.md](references/sector-lenses.md)
- 估值方法与防重算：[references/valuation.md](references/valuation.md)
- 报告图表与多格式输出：[references/reporting.md](references/reporting.md)
- 质量门槛和更新：[references/quality-gates.md](references/quality-gates.md)
- 可选XHalo集成：[references/xhalo-integration.md](references/xhalo-integration.md)

根据请求选择深度：`quick-screen`（简表）、`deep-dive`（完整）、`earnings-update`（最新业绩）、`valuation-build`（模型）、`report-only`（基于已核查材料撰写）、`refresh`（增量更新）。未指定时，明确的“完整研究报告”采用 `deep-dive`。

**最小启动参数**：公司名称/证券代码（若唯一可解则自动确定）、交易所、截止日期、报告语言与交付形式。其余从公开资料补足，不因次要信息缺失阻塞完成。

分类行业：非金融企业、平台互联网、银行、保险、证券/交易所、REIT、工业/消费、SaaS、医药/生物科技、能源矿业、公共事业、控股公司/多业务集团、周期性公司。**先选行业模型，再选估值法**。

## 2. 必经工作流（10阶段）

### P0 — 定义研究问题和审查时点
确认投资主问题、股票类别、主要市场、币种、最新收盘价及时间戳、分红与总回报口径、观察期限。区分实体报告期与信息发布日期。建立 `project.json` 和 `issues.csv`。

### P1 — 采集分层证据
从交易所公告/10-K/20-F/年报/季报/财报附注/业绩电话会/公司IR出发，再采监管与统计局数据、同行公告、第三方份额、投行原报告或可验证摘要、权威新闻。保存源 ID、可访问 URL、发布时点、财报页码和统计口径到 `sources.csv`。按 [references/evidence.md](references/evidence.md) 校正相互矛盾数据。

### P2 — 建立历史三表与业务驱动
至少覆盖过去3个完整年度，外加可获得的最新季度/中期；同比必须同口径同期，杜绝把季度利润率和全年利润率直接视为相同季节性。重构分部营收、成本、OP/EBIT、税、CFO、CAPEX、净债务、少数股东权益及稀释股本；逐个标明定义与审计位置。

### P3 — 财报质量审计（必须优先于估值）
按 [references/financials.md](references/financials.md) 强制检查：
- 总额法与净额法；平台佣金、广告与1P自营商品的收入质量差异；并购、重分类、通胀、汇率带来的增长。
- `Revenue` 与 `other gains`、处置权益、视同处置、金融资产公允价值、OCI、联营企业业绩严格分开。
- Non-GAAP 调整桥和 SBC、租赁负债现金流、营运资本变动、一次性税项；不得认为“调整后利润=可分配现金”。
- 经营现金流、现金转换率、FCFF/FCFE、净现金/战略投资/递延税负/资本配置；核验合计、同比、现金变动和资产负债平衡。

### P4 — 行业格局与单位经济
比较至少2名可比竞争者（若有）、份额分母、订单/客户/GMV/核销率、ARPU、take rate、CAC、履约成本、复购、价格/补贴与商户/客户ROI。非披露数据写“研究估算”，给出区间与替代证据。区分“交易规模”“收入”“利润池”“定价权”。

### P5 — 宏观传导与反证
只选择对业务现金流有因果路径的宏观变量。沿 `宏观事实 → 需求/价格/供给/融资 → 业务KPI → 利润/现金流` 映射；区分周期、结构、政策、汇率与贸易冲击；同时写出反方向缓冲。例：M2上涨不等于居民消费通胀；低国债收益率不能机械降低外币DCF WACC；灵活就业不等于失业；失业保险支出不等于领取失业金人数。参见 [references/macro-competition.md](references/macro-competition.md)。

### P6 — 拟定假设和情景
为每个关键经营驱动提供 `downside/base/upside` 三情景及数值出处/判断依据；从单位经济和资本效率推导分部财务，禁止只是每年套收入增速与利润率。记录假设、可证伪条件及模型版本。避免宏观因素既压低收入/毛利、又额外通过WACC重复处罚。

### P7 — 选估值法并重建价值桥
非金融成熟企业优先 FCFF-DCF/交易可比；集团用不重复计算的SOTP；银行用P/B-ROE/RIM/DDM；保险用EV/PVNBP/RIM；REIT用AFFO/NAV；矿业用资源与商品周期NAV；生物医药用rNPV等。按 [references/sector-lenses.md](references/sector-lenses.md) 选用。显式计算 WACC/Ke、终值、再投资、非经营资产、净债务、租赁、少数股东、递延税、可转债及股数。

### P8 — 反向估值、风险与决策门槛
当前价格隐含什么经营假设？收益来源是利润扩张、增长、资本回报还是倍数修复？同时给Bear/Base/Bull、WACC×g敏感性、情景概率（若缺乏依据可不赋概率）、投资论点证实/证伪和风险临界值。列出何种数据会改变结论。

### P9 — 报告和图表
完整报告采用 [assets/report-template.md](assets/report-template.md) 结构，优先同时输出：PDF或DOCX（按请求）、Markdown/HTML（易审计）、模型工作簿（有模型时）、原始source/metric/assumption/chart ledger。至少包括：财务趋势、分部结构、现金流质量、竞争/宏观传导、SOTP价值桥、WACC敏感性。**图表必须是真实绘制，不可用标题代替图表**，每张图有来源与统一单位。图表机制见 [references/reporting.md](references/reporting.md)。

### P10 — 自动QA及人工推理复核
调用 `python scripts/validate_research.py <project_dir>`；有数据时运行 `python scripts/render_charts.py <project_dir>`；对DCF配置调用 `python scripts/dcf_sotp.py <input.json> --output <result.json>`；检查可读性、公式来源、缺失链接和计算结果。未通过硬性门槛时报告标注 `not-decision-ready` 而不是隐藏缺陷。

## 3. 交付标准

**标准完整输出**：
1. 研究日期、数据截止日、证券代码/币种及简明研究立场；
2. 3–5年财报趋势+最新季度，会计质量和FCF桥；
3. 行业份额/竞争/宏观因果矩阵（明确支持与反证）；
4. 核心利润驱动、分部价值、估值矩阵及反向估值；
5. 未来指标、催化剂、压力情景和更新触发器；
6. 可点开的逐项来源清单、图表来源说明、公式/假设附录；
7. `data confidence` 与 `valuation readiness` 分开披露、重要未解决冲突。

**质量状态**：
- `decision-grade`：关键输入有可靠原始证据、模型闭环、主要敏感性可控且完成复核（不保证投资结果）。
- `senior-review-ready`：来源与逻辑较完整，少量非核心假设待核。
- `screen-grade`：高价值分部/市场数据仍为区间估算，结果只能用于初筛。
- `not-decision-ready`：股数/资本结构/现金流/主营拆分等关键数据缺失或模型检查失败。

## 4. 可运行组件与复用

```bash
# 建立新研究文件夹（只有空模板；不会生成或猜测研究数据）
python scripts/new_project.py --company '示例公司' --ticker 'XXXX' --exchange 'HKEX' --output ./research/XXXX

# 填入 sources.csv / metrics.csv / assumptions.csv / charts.json / report.md 后
python scripts/validate_research.py ./research/XXXX
python scripts/render_charts.py ./research/XXXX
python scripts/dcf_sotp.py ./research/XXXX/valuation.json --output ./research/XXXX/valuation-result.json
```

依赖：Python 3.9+；报告元数据、DCF计算与校验脚本只用标准库；图表绘制额外需要 Matplotlib (`pip install matplotlib`)。DOCX/PDF等格式依赖宿主现有文档工具；不假定环境已安装，不提供未经验证的导出链接。

## 5. 特别警示：从美团案例抽取的可迁移纠错模式

- 自营商品销售高增可能带来总额法营收膨胀，不能按广告/佣金倍数估值。
- 卖股/视同处置、公允价值重估、OCI须和主营收入/现金流分开。
- 不公开披露的独立业务利润率不准包装成已报告事实；SOTP须反映不确定性。
- 每引入一项宏观利空不要机械把目标价下降一次；先检查与已有假设是否重复。
- 回购抵消股数稀释并不使SBC的经济成本“消失”；现金与股数需联立。
- 战略持股是否可出售、税负、锁定期、少数股东、递延税须入桥；净现金需区分经营必要现金与超额现金。
- 永续期占比偏高时，先检验稳态增长、再投资/ROIC和估值抗扰性，不给虚假精确度。
- 更多见 [examples/meituan-case-methodology.md](examples/meituan-case-methodology.md)。

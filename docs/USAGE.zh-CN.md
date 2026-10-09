# 使用指南：从研究问题到可核查报告

## 1. 最小输入

一份完整的上市公司研究至少明确证券代码、交易所、研究截止日期、报告语言、交付格式以及分析重点。若市场主体可唯一确认，Agent可自行识别。不要在不同市场同名证券之间混用数据。

## 2. 研究提示词：全量覆盖

> 使用 listed-equity-research 研究美团-W（3690.HK）。基于最近三年官方年报、最新中报与监管披露审计收入、投资收益、OCI、股份支付、租赁、现金流。研究竞争平台的实际市场份额口径、核心城市消费、居民信贷与宏观传导。进行分业务单位经济建模，构建2027–2035年FCFF/SOTP与反向DCF、WACC/永续增长敏感性；以每个关键数据的原始URL、发布日期、表格/页码和币种说明支持图表与投资结论。对不可获取的独立分部利润明确声明是估计，不可给虚假精确目标价。

## 3. 按行业切换

**银行：** 重点为净息差、不良贷款、拨备、风险加权资产、资本充足率、ROE及P/B–ROE或剩余收益模型，不能直接使用工业企业的FCFF。

**SaaS/云计算：** ARR、毛利、净留存、CAC回收、RPO、SBC、数据中心CAPEX、ROIC、FCF和长期增长。

**制造/能源：** 销量×均价、库存、产能利用率、固定资产再投资、商品价格周期、资本密集程度和正常化税后利润。

**互联网平台：** 交易量/GMV、核销、佣金与广告变现、商户ROI、补贴与履约成本、总额法/净额法收入、分部SOTP。

## 4. 工具命令

```bash
python listed-equity-research/scripts/new_project.py \
  --company 'Example Corp' --ticker DEMO --exchange NASDAQ --output research/demo
```

在生成的目录填写 `sources.csv`（证据源），`metrics.csv`（金额/比率/期间），`assumptions.csv`（研究假设），`issues.csv`（数据缺口），`charts.json`（绘图配置）。`sources.csv` 中每个源须有稳定ID和链接。

检查：

```bash
python listed-equity-research/scripts/validate_research.py research/demo
python -m pip install matplotlib
python listed-equity-research/scripts/render_charts.py research/demo
```

**校验脚本核验结构与来源引用，不会联网查证外部来源真实性。** 如果图表输入只是虚构样例，图表必须明确写 illustrative。

## 5. 估值

在已有可靠财报和经营假设后，修改示例JSON：

```bash
python listed-equity-research/scripts/dcf_sotp.py \
  research/demo/valuation.json --output research/demo/valuation-result.json
```

示例 `assets/valuation.example.json` 中的输入**全部为虚构数据**。估值程序只执行计算，分析师须核对现金流是否为FCFF还是FCFE，SBC是否已扣除、租赁是否作为债务、股数是否稀释、币种是否匹配、终值占比和资本再投资是否合理。

## 6. 交付报告

每份完整报告建议包含：执行摘要、估值状态、证券与行情截止日、三表趋势、财报质量分析、业务经营驱动、宏观与竞争证据、分部预测、估值桥、逆向DCF、风险和反证、KPI监测、逐项可点击原始来源。图表须注明币种、单位、样本期、原始资料或明确的自建估算。

## 7. 更新研究

季度增量更新必须报告“结论变化来自哪里”：经营数据变化、预测变动、折现率/终值、投资资产/净债务、汇率与稀释股本。上次预测不能代替本次事实。

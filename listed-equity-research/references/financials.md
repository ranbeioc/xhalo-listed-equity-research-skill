# 财报审计与现金流规范

## 1. 三年基线与最新披露

优先获取最近三份年报（形成至少3年同口径序列）+ 最近季度/半年报 + 对应前年同期 + 重要附注/管理层讨论，标明是已审计还是未经审计。多次重述时以最新同口径重述数据为准，并保留原版差异说明。

核对：收入、成本、毛利、研发、销售/营销、管理费、EBIT/营业利润、所得税、归母净利、EPS、股本、资产负债表及现金流；按分部、地区、产品、渠道交叉复核。**必须明确是否为净额法/总额法**：平台收入与自营零售收入不可对等处理毛利贡献；并购、货币换算、新准则改变可能造成增速失真。

## 2. 非经营与非经常性项目

严格拆分：
- `Revenue`：交易收入；广告/商户服务；自营收入；利息是否属于经营收入视行业与公司会计政策判断。
- `Other income/gains`：投资处置/视同处置、金融资产FVTPL重估、汇兑、补贴、一次性收益。
- `Equity-method profit/loss`：权益法联营企业业绩，可能未收到现金。
- `OCI/FVOCI`：其他综合收益，不应自动进入当期净利润；对应公允价值变化可能产生递延税。
- `Reported profit`、`Adjusted EBITDA`、`adjusted net profit`、`normalized operating earnings` 与 `owners' cash flow` 必须不同栏展示。

`deemed disposal gain` 通常不等于当期收回现金；核对处置现金收款与账面收益，不得以“卖出股票”描述所有视同处置收益。

## 3. 现金流桥

一般非金融公司 FCFF：

`FCFF = EBIT × (1 - normative_cash_tax_rate) + D&A - maintenance_CAPEX - growth_CAPEX - ΔOperating_NWC - other_operating_investment_cash_outflows`。

`FCFE = CFO - CAPEX - lease_principal_payments + net_borrowing - other_financing_cash_outflows` 只是出发式示意：**需根据CFO是否包含利息、租赁与所得税付款、以及不同会计准则调整口径，逐项重建**；不可无条件套用。

营运资本：应付商家/客户预存/递延收入/库存变化可能改善经营现金流但不代表经常利润。把 `CFO before WC`、`ΔNWC`、`reported CFO`、`cash CAPEX`、`lease principal`、`interest paid`、`SBC` 并列展示。若需要“股东现金回报”要说明股息/回购另列且不改变企业本身FCFF定义。

## 4. SBC、回购、股本

有两种一致的估值路径，只能选择一种：

A. **不从运营现金流重复扣SBC**；预测增发/RSU归属、期权行权、回购及现金影响，使用动态稀释股本，单独计股权结构。

B. **将未来SBC作为现金等价经济成本调整FCF**，终值不再因同一SBC重复上调稀释股数；现有已授股权负债与潜在期权另行核对。

回购不是免费的，它减少现金、也可能减少股数；不得一边将全部回购金额从FCF扣除，一边又加回“回购增加的每股价值”而未做统一的股本/现金桥。稀释股份数不等于当前已发行股数，应考虑期权价内/价外、归属条件、转换工具与Treasury Stock Method（适用时）。

## 5. 租赁、现金与金融投资

IFRS 16/ASC 842下租赁本金通常在融资现金流，租赁利息位置受政策影响；FCFF若经营利润包含使用权资产折旧，应确保租赁负债与折现口径一致。净债务桥分别列：现金等价物、理财/定期存款、经营必要现金、受限现金、短期/长期借款、票据、可转债、租赁负债、少数股东权益、未计税收益。战略性非经营投资**先确认是否已通过联营损益、分部现金流或合并资产体现**，不得重复加入。

长期投资价值：公允/市场价值、锁定期、流动性、控股折价、销售税负/递延税负；若估值折价已覆盖风险，不再重复扣除同一项目。采用可回收价值，不将未变现OCI浮盈直接视为可立即返还现金。

## 6. 核对项

1. `Revenue - COGS = Gross profit`、`Total segment EBIT + unallocated + reconciliation = consolidated EBIT`。
2. `Assets = Liabilities + Equity`（仅完整表），`opening cash + cash movements + FX = closing cash`。
3. 利润与非现金收益的CFO加回/扣除正确；租赁与营运资本说明到位。
4. `reported / normalized / FCFF`各层没有把收益/利息/税/利息收入重复计入。
5. 在卖方净利润与现金流的调和表中注明SBC是否加回、是否有并购影响。

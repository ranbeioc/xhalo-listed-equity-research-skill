# 可选：在XHalo工作流/Agent/MCP中复用

本文件是**建议的集成契约**，不是声称已部署或存在这些API。与具体xhalo平台版本无关，接口字段按实施时调试。

## 建议组件映射

- `xhalo-ai-workflow`：研究任务编排；步骤：identifier → filings → normalize → macro/competitors → assumptions → models → charts → report → QA。
- `xhalo-crawl` 或授权搜索MCP：获取公司交易所公告、官方统计及新闻；不得绕过付费墙或未经授权抓取投行正文。
- `Cloudflare R2`：存储原始文献合法缓存/图表/报告版本；文件名以 `ticker/asof/revision` 分类。
- `D1/PostgreSQL`：存储项目元信息与 `source_id`/`metric_id`/报告索引，不应把大型PDF二进制塞入数据库。
- `Cloudflare Queues/Workers`：轻任务调度、重试、去重、更新事件；复杂PDF解析/文档排版/大量图表根据平台限额交给VPS CPU服务。
- `xhalo-auth`：报告访问权限；`xhalo-admin`：任务、额度、运行日志与费用统计。
- `API/MCP` 工具可抽象为 `research.search_filing`, `research.fetch_source`, `research.get_market_data`, `research.compute_valuation`, `research.render_report`, `research.validate_report`，不可假设现有工具一定具备这些名称。

## 任务状态及证据契约

任务状态：`queued → collecting → normalized → modeling → rendering → qa → completed`，失败状态保留原因及可重试步骤；报告版本不可覆盖原始来源和旧模型。

每个数据点保留：`security_id`, `period`, `metric_key`, `value`, `unit`, `basis`, `source_id`, `source_page_or_table`, `retrieved_at`, `confidence`, `model_version`。

`source_id` 源对象包含具体 URL、版权/授权许可、SHA256（存储快照时）、发布时间和抓取时间。`report_version`绑定 `model_version` 与 `chart_manifest_hash`，保证PDF、DOCX、HTML、XLSX来自同一数据截点。

## 成本和安全

优先增量刷新；只在新公告/实质性变化时重算。不得上传API密钥至skill或日志；所有密钥使用平台机密存储。市场数据版权和报告全文分发要确认授权；优先公开原文，受版权保护的材料只存链接/检索元数据。失败时不返回未经审核的伪定量结论。

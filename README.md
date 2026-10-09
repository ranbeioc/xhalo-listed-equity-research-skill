# XHalo Listed Equity Research

**A source-auditable Agent Skill for researching publicly listed companies, investigating financial-statement quality, modeling intrinsic value, and producing cited investment reports.**

**可审计的上市公司深度研究 Agent Skill：财报核查、竞争与宏观传导、现金流审计、DCF/SOTP 估值、数据图表及研究报告。**

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md)

> [!IMPORTANT]
> 本仓库包含**完整技能目录** `listed-equity-research/`，并非仅提供 `SKILL.md`。安装时请复制整个目录，保留 `references/`、`assets/`、`scripts/`、`examples/`。它是研究辅助工具，**不会自动提供实时行情或付费投行研报**，也不提供个人化投资建议。示例报告https://muse.xhalo.co/pages/datas/2026-10-09-meituan-sotp-dcf

## 适用场景

- **首次覆盖 / 综合研究**：公司业务、三至五年财报、最新季报、竞争格局、宏观驱动与投资论点。
- **财报质量审计**：总额法/净额法、商户佣金、自营零售、其他收益、视同处置、公允价值、OCI、调整后利润。
- **股东现金流**：CFO、FCFF/FCFE、资本开支、租赁、股权激励、回购、营运资本、超额现金和资本配置。
- **跨行业估值**：非金融企业 DCF、集团 SOTP、相对估值、反向 DCF；银行/保险/REIT/矿业/医药选择各自适用方法。
- **竞争与宏观研究**：把就业、消费、信贷、汇率、利率等证据映射到实际业务驱动，避免同一风险重复扣减。
- **报告生成与质检**：基于来源台账生成图表；由具备相应工具的 Agent 输出 Markdown、HTML、Word、PDF 和 Excel。

## 技能能力与限制

| 能力 | 本仓库内置 | 备注 |
|---|---|---|
| Agent Skill 指令与八份方法论参考 | ✅ | 完整目录、渐进式阅读 |
| 新建研究项目 / 来源与指标 CSV 模板 | ✅ | 不自动捏造财务数据 |
| 来源、指标、假设与图表关系校验 | ✅ | 检查结构和引用，不验证外部网页真实性 |
| DCF / SOTP 基础计算 | ✅ | 计算引擎不代替模型假设审核 |
| PNG 数据图表生成 | ✅ | 需另外安装 Matplotlib |
| 虚构数据离线自测 | ✅ | 测试不是投资依据 |
| 真实行情、财报、卖方报告抓取 | ❌ | 依赖宿主可用网页/数据连接与权限 |
| 一键全自动三表、PDF/DOCX/Excel排版导出 | ❌ | 可由具备文档/表格工具的宿主Agent完成 |

## 安装

**推荐：clone 并安装技能子目录。** 不要把整个仓库根目录直接当成一个 skill，也不要只复制 `SKILL.md`。

```bash
git clone https://github.com/ranbeioc/xhalo-listed-equity-research-skill.git
cd xhalo-listed-equity-research-skill

# 默认安装到 ~/.agents/skills/listed-equity-research，已有目录先备份
python scripts/install_skill.py --root ~/.agents/skills --test

# Claude Code 常见技能路径（请按实际宿主配置调整）
python scripts/install_skill.py --root ~/.claude/skills --test
```

也可手动复制 **整个** `listed-equity-research/` 文件夹到宿主技能目录。支持 Python 3.9+；绘图额外安装 `python -m pip install matplotlib`。关于 Windows、离线安装和权限参见 [详细安装说明](docs/INSTALL.zh-CN.md) 和 [内置安装说明](listed-equity-research/INSTALL.md)。

## 直接调用示例

Agent 收到下列指令时，应读取 `SKILL.md` 及任务相关参考文件，而不是直接从既有案例复制结论：

> 使用 `listed-equity-research` 分析港股美团 3690.HK。核对最近三年年报、最新中报、竞争对手、宏观数据和投行公开预测，区分主营收入、投资收益和OCI；建立 FCFF / SOTP 情景，提供逐项原始来源、表格、图表、反向估值和不确定性说明，输出中文报告。未经披露的分部利润率必须标注为分析师估算。

其他行业的研究任务：

```text
使用 listed-equity-research 深入研究微软 MSFT，比较云业务的增长、资本开支、ROIC、
自由现金流和同业估值；模型中单独量化AI基础设施投资和终值敏感性。

使用 listed-equity-research 研究一家上市银行。按银行专用估值框架，
分析净息差、资产质量、资本充足率、拨备与ROE，优先用P/B–ROE和剩余收益模型，
不得套用普通制造企业的EV/EBITDA或FCFF。

使用 listed-equity-research 更新某公司的最新季度财报。与上一版模型做逐项差异归因：
经营假设、资本成本、股数、汇率、净债务、战略投资和价值变化。
```

更多完整示例参见 [研究提示词集](examples/research-prompts.md)、[美团方法论复盘](listed-equity-research/examples/meituan-case-methodology.md)。**美团示例仅用于说明研究纠错模式，不预设其目标价，也不将演示估值当作证券事实。**

## 本地工具快速入门

以下命令均在仓库根目录执行：

```bash
# 检查完整包（哈希/大小）
python listed-equity-research/scripts/verify_install.py listed-equity-research

# 运行端到端虚构数据测试
python listed-equity-research/scripts/self_test.py

# 新建空白研究项目
python listed-equity-research/scripts/new_project.py \
  --company 'Example Corp' --ticker 'DEMO' --exchange 'NASDAQ' --output research/demo

# 填入真实数据和来源后检查
python listed-equity-research/scripts/validate_research.py research/demo

# 填写 charts.json 且安装 matplotlib 后生成带来源关系的数据图
python listed-equity-research/scripts/render_charts.py research/demo

# 注意：下例全为虚构参数，只测试运算，不代表上市公司价值
python listed-equity-research/scripts/dcf_sotp.py \
  listed-equity-research/assets/valuation.example.json --output research/demo-valuation.json
```

## 分析流程

```text
研究问题与截止日
    ↓
交易所/公司IR/监管/统计/投行来源分级与证据台账
    ↓
三至五年财报及最新季度 → 收入质量/异常收益/现金流审计
    ↓
业务单位经济 + 竞争 + 宏观因果链与反证
    ↓
分部经营预测（Bear/Base/Bull） + 资本配置与投入回报
    ↓
行业适配 DCF / SOTP / 可比估值 + 反向估值
    ↓
来源绑定图表 + 研究报告 + 自动QA + 不确定性和更新触发器
```

详见 [完整工作流](docs/WORKFLOW.zh-CN.md)、[使用指南](docs/USAGE.zh-CN.md)、[财报与估值注意事项](docs/CAUTIONS.zh-CN.md)。

## 研究约束

1. **来源可复核**：财报数据须标识出处URL、发布日期、页码/表格与币种；投行摘要不可伪装为原版研报。
2. **事实与模型分离**：`reported`、`official-stat`、`consensus`、`broker`、`analyst-estimate`、`illustrative` 等类别必须区分。
3. **会计边界清晰**：股权投资处置收益不是营业收入；OCI浮盈不等于净利润；调整后利润不等于可分配现金。
4. **反重复计算**：净现金、战略投资、递延税、租赁、SBC、回购和稀释不得在SOTP股权价值桥重复处理。
5. **现金流币种一致**：名义人民币FCF配名义人民币折现率；终值检查永续增长、ROIC与再投资。
6. **反偏误**：宏观风险先映射到真实经营参数，再检查是否还应改变资本成本；列出反证和证伪触发器。
7. **输出质量等级**：关键输入缺失时只能给 `screen-grade` / `not-decision-ready`，不能输出虚假精确的目标价。

## 项目结构

```text
xhalo-listed-equity-research-skill/
├── README.md                 # 简体中文（首页）
├── README.zh-TW.md           # 繁體中文
├── README.ja.md              # 日本語
├── README.ko.md              # 한국어
├── README.en.md              # English
├── LICENSE                   # MIT
├── docs/                     # 详细使用、方法论、限制、安装
├── examples/                 # 不同行业的研究提示词
├── scripts/install_skill.py  # 完整目录安全安装与校验
├── .github/workflows/ci.yml  # 安装完整性与自测
└── listed-equity-research/    # 独立、可直接安装的完整 Agent Skill
    ├── SKILL.md
    ├── references/            # 8篇方法论参考
    ├── assets/                # 研究模板与示例数据
    ├── scripts/               # 初始化/QA/绘图/DCF工具
    └── examples/              # 案例复盘
```

## 贡献和安全

欢迎通过 Issue/PR 贡献行业研究方法、来源审计规则、财务模型校验和多语言文档。提交新数据时，请提供官方原始链接、时间戳和统计口径。查看 [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md)。

使用本技能产生的研究属于**分析辅助**，不构成投资、法律或税务建议；历史表现及模拟估值不保证未来结果。

## License

[MIT License](LICENSE) · Copyright © 2026 Skyfire (see LICENSE).

# XHalo 上市公司深度研究 Skill

**可稽核的 Agent Skill**：上市公司財報、會計品質、產業競爭、總體經濟傳導、現金流、DCF/SOTP 估值及附來源的圖表研究報告。

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md)

> **必須安裝完整 `listed-equity-research/` 目錄**，不能只匯入 `README.md` 和 `SKILL.md`。本專案不內建即時股價、付費投行報告、交易執行或個人化投資建議。

## 核心功能

- **企業深度研究：** 最近3至5年正式財報、最新季度／中期業績、業務分部、資本配置。
- **會計品質分析：** 收入總額法／淨額法、投資處分與視同處分、公允價值、OCI、一次性利益及非IFRS／非GAAP調整。
- **現金流審計：** CFO、FCFF/FCFE、營運資金、資本支出、租賃、利息、股權獎酬（SBC）、回購及稀釋。
- **競爭與總體經濟：** 市占率、單位經濟、定價能力、商戶ROI、信貸、就業、消費、利率與匯率，避免將同一風險重複折價。
- **跨產業估值：** DCF、反向DCF、SOTP、同業比較；銀行、保險、REIT、礦業及生技使用適合的專用方法。
- **可追溯報告：** 數據來源表、模型假設表、圖表和研究敘事；PDF、Word、Excel輸出視宿主Agent的工具能力而定。

## 安裝方式

需要 Python 3.9+；PNG圖表另外需要 Matplotlib。

```bash
git clone https://github.com/ranbeioc/xhalo-listed-equity-research-skill.git
cd xhalo-listed-equity-research-skill
python install_listed_equity_research.py --root ~/.agents/skills --test
# Claude Code 常見路徑（依宿主設定）
python install_listed_equity_research.py --root ~/.claude/skills --test
```

或將整個 `listed-equity-research/` 複製至技能根目錄，驗證完整性：

```bash
python listed-equity-research/scripts/verify_install.py listed-equity-research
python listed-equity-research/scripts/self_test.py
```

## 使用範例

**美團（3690.HK）**

> 使用 `listed-equity-research` 核對最近三年年報及最新中報；區分自營商品收入、平台商戶服務、投資利益及其他綜合損益；比較抖音、阿里、京東的競爭，將居民消費及信貸資料對應到客單價、抽佣、現金流。生成附原始連結與圖表的分部DCF/SOTP及悲觀／基準／樂觀情境。未正式揭露的獨立業務利潤率須標為估算。

**微軟（MSFT）**

> 研究Azure業務、AI資本支出、折舊、ROIC、FCF及同業估值；用反向DCF說明目前股價隱含的長期經營假設與可能反證。

**上市銀行**

> 依淨利差、信用品質、資本適足率、存款成本及備抵呆帳研究，優先採P/B–ROE與剩餘收益模型；不得直接套用非金融公司的FCFF。

## 本地命令

```bash
python listed-equity-research/scripts/new_project.py --company "Example Corp" --ticker DEMO --exchange NASDAQ --output research/demo
python listed-equity-research/scripts/validate_research.py research/demo
python listed-equity-research/scripts/render_charts.py research/demo
python listed-equity-research/scripts/dcf_sotp.py listed-equity-research/assets/valuation.example.json --output research/demo-valuation.json
```

**範例估值使用虛構資料，不代表任何真實股票價值。** 本工具沒有自動授權證券資料，也不保證每個Agent能產出Office/PDF。

## 注意事項

1. 重要數據須附原始URL、公布日期、報告期間、幣別與頁碼／表格。
2. 區分已披露、官方統計、一致預期、券商估算、自行推算及示範資料。
3. 投資處分利益不等於營收，OCI浮盈不等於淨利；調整後利益不等於可分配現金。
4. SOTP中現金、股權投資、稅、租賃、SBC、回購及稀釋股數須一致處理，避免重複計價。
5. 名目現金流需搭配相同幣別的折現率，揭露終值占比與敏感度。
6. 關鍵財務輸入缺失時，標為 `screen-grade` 或 `not-decision-ready`，不提供虛假的精確目標價。

詳見：[SKILL.md](listed-equity-research/SKILL.md) · [安裝說明](listed-equity-research/INSTALL.md) · [研究方法](listed-equity-research/references/evidence.md) · [美團案例](listed-equity-research/examples/meituan-case-methodology.md)。

[貢獻](CONTRIBUTING.md) · [安全](SECURITY.md) · [MIT協議](LICENSE)。

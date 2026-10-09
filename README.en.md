# XHalo Listed Equity Research Skill

**An evidence-auditable Agent Skill for public-company research, earnings-quality analysis, competitive and macroeconomic research, and reproducible DCF/SOTP valuations.**

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md)

> **Install the entire `listed-equity-research/` folder**. Uploading only `SKILL.md` or `README.md` is insufficient. This repository does not include licensed broker reports, live market feeds, trading execution, or personalized investment advice.

## Features

- **Fundamental research:** 3–5 years of company filings, recent earnings, segment economics, corporate strategy and capital allocation.
- **Accounting forensics:** gross versus net revenue, investment disposals, fair-value changes, OCI, non-recurring items, non-GAAP bridges, and mergers/reclassifications.
- **Cash-flow quality:** CFO, normalized FCFF/FCFE, working capital, lease payments, capex, interest, stock-based compensation, buybacks and diluted shares.
- **Market and macro:** competition, pricing power, customer and merchant ROI, regulation, household credit, employment, consumer spending, interest rates and FX — linked to operating drivers instead of double-counted as generic discounts.
- **Sector-specific valuation:** DCF, reverse DCF, SOTP and trading comps; separate analytical frameworks for banks, insurers, REITs, mining and life sciences.
- **Auditable charts and reports:** source, metrics and assumptions ledgers; charts with source references; supported report structures for Markdown, HTML, Word, PDF and Excel (export depends on host tools).

## Installation

Python 3.9+ is required. Matplotlib is optional for image charts.

```bash
git clone https://github.com/ranbeioc/xhalo-listed-equity-research-skill.git
cd xhalo-listed-equity-research-skill

# Self-contained offline installer, no network downloads during installation
python install_listed_equity_research.py --root ~/.agents/skills --test
# Claude Code (confirm your host's actual skills directory)
python install_listed_equity_research.py --root ~/.claude/skills --test
```

Manual installation: copy the **entire** `listed-equity-research/` directory into your agent's skills root. Verify:

```bash
python listed-equity-research/scripts/verify_install.py listed-equity-research
python listed-equity-research/scripts/self_test.py
```

The included `MANIFEST.json` validates all distributed skill files. Run offline tests before using it in research.

## Prompt examples

**Meituan / platform:** Analyze Meituan (3690.HK) using the last three annual reports and latest interim report. Separate delivery, merchant services and gross merchandise sales; distinguish operating revenue from disposal gains and OCI. Study Douyin, Alibaba and JD competition; link household consumption data to AOV, take rate and cash flow. Produce sourced financial charts, segment FCFF/SOTP, reverse DCF and bear/base/bull scenarios. Flag undisclosed segment margins as analyst estimates.

**Microsoft / software:** Investigate MSFT's cloud growth, AI capital intensity, depreciation, ROIC and free cash flow. Compare peers, test WACC/terminal assumptions, and explain the operating results implied by the current valuation.

**Banking:** Analyze a publicly traded bank using deposit costs, net interest margin, nonperforming loans, provisions and regulatory capital. Prioritize P/B–ROE and residual-income valuation, not nonfinancial-company FCFF.

**Earnings update:** Reconcile a new earnings release with an existing model; attribute value changes to operations, assumptions, discount rate, FX, net debt, investments and dilution. List disconfirming evidence.

## Offline utilities

```bash
python listed-equity-research/scripts/new_project.py --company "Example Corp" --ticker DEMO --exchange NASDAQ --output research/demo
python listed-equity-research/scripts/validate_research.py research/demo
python listed-equity-research/scripts/render_charts.py research/demo   # needs matplotlib and populated data
python listed-equity-research/scripts/dcf_sotp.py listed-equity-research/assets/valuation.example.json --output research/demo-valuation.json
```

**The valuation example contains fictional inputs.** Scripts verify structure and calculate supplied assumptions; they do not independently download market data, fact-check an external URL, or produce full DOCX/PDF/XLSX files without the host application's tools.

## Evidence, modeling and safety standards

1. Cite original financial disclosures with URL, publication date, reporting period, currency, and page or table number.
2. Distinguish `reported`, `official-stat`, `consensus`, `broker`, `expert-estimate`, `analyst-estimate`, `derived`, and `illustrative` evidence.
3. Investment disposals are not sales; OCI gains are not ordinary profit; adjusted earnings are not distributable free cash flow.
4. Avoid double counting in SOTP: operating segments, strategic assets, net cash, leases, taxes, SBC, buybacks, and share dilution.
5. Match cash-flow currency and discount-rate currency; stress-test terminal-value concentration and reinvestment/ROIC.
6. Explain both bullish and bearish evidence. Incomplete essential inputs must be labeled `screen-grade` or `not-decision-ready` rather than presented as precise target prices.

More information: [Research workflow](listed-equity-research/SKILL.md) · [Installation](listed-equity-research/INSTALL.md) · [Evidence](listed-equity-research/references/evidence.md) · [Valuation](listed-equity-research/references/valuation.md) · [Methodology case](listed-equity-research/examples/meituan-case-methodology.md).

Contribute via [issues and pull requests](CONTRIBUTING.md). [Security policy](SECURITY.md). **License: [MIT](LICENSE).**

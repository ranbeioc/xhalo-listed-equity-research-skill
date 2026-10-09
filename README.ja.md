# XHalo Listed Equity Research Skill ― 上場企業ディープリサーチ

**出典を追跡・検証できる企業研究Agent Skill。** 財務諸表、会計品質、競争環境、マクロ経済、キャッシュフロー、DCF/SOTP評価、グラフ付きレポートを一貫した手順で分析します。

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [English](README.en.md)

> **重要：`listed-equity-research/` ディレクトリ全体をインストールしてください。** `README.md` と `SKILL.md` だけでは不完全です。リアルタイム株価、有料アナリストレポート、売買執行、個別投資助言は含まれません。

## 主な機能

- **企業分析：** 過去3～5年間の年次・中間報告書、最新四半期、事業別業績、資本配分。
- **会計品質：** 収益の総額／純額表示、投資売却益、みなし売却、公正価値の変動、OCI、一時損益、非GAAP調整。
- **キャッシュフロー監査：** CFO、FCFF/FCFE、設備投資、運転資本、リース、金利負担、株式報酬（SBC）、自社株買い、希薄化。
- **競争とマクロ経済：** シェア、顧客・加盟店ROI、価格決定力、雇用、家計信用、消費、為替と金利の影響を営業KPIへ結び付け、同じリスクの二重計上を避ける。
- **業種別評価：** DCF、逆DCF、SOTP、類似企業比較。銀行、保険、REIT、鉱業、医薬品は専用手法を採用。
- **グラフとレポート：** 出典URL、日時、単位と仮定を管理し、対応するホスト環境でMarkdown/HTML/PDF/DOCX/Excelのレポートを作成。

## インストール

Python 3.9以上が必要。PNGグラフには `matplotlib` を追加してください。

```bash
git clone https://github.com/ranbeioc/xhalo-listed-equity-research-skill.git
cd xhalo-listed-equity-research-skill
python install_listed_equity_research.py --root ~/.agents/skills --test
# Claude Codeの一般的なパス（環境によって異なる）
python install_listed_equity_research.py --root ~/.claude/skills --test
```

手動インストールの場合は **`listed-equity-research/` 全体**を対象のskillsディレクトリへコピーします。確認：

```bash
python listed-equity-research/scripts/verify_install.py listed-equity-research
python listed-equity-research/scripts/self_test.py
```

## 利用例

**美団（3690.HK）の分析**

> `listed-equity-research` を使い、直近3年の年次報告書と最新中間決算を検証。デリバリー収益・加盟店サービス・商品販売を分離し、投資売却益とOCIを営業利益から区別する。Douyin・Alibaba・JDとの競争、家計信用と消費の影響を評価し、出典付きグラフ、事業別FCFF/SOTP、逆DCF、弱気・基本・強気シナリオを作成。未開示の事業別利益率は推計と明示すること。

**Microsoft（MSFT）の分析**

> Azureの成長、AI設備投資、減価償却、ROIC、FCFと類似企業の評価を比較し、現在の株価が前提とする長期成長と利益率を逆DCFで求めること。

**上場銀行**

> 預金コスト、利鞘、不良債権、引当金、自己資本比率を分析し、P/B–ROEと残余利益モデルを優先すること。一般事業会社のFCFFを機械的に適用しないこと。

## オフラインツール

```bash
python listed-equity-research/scripts/new_project.py --company "Example Corp" --ticker DEMO --exchange NASDAQ --output research/demo
python listed-equity-research/scripts/validate_research.py research/demo
python listed-equity-research/scripts/render_charts.py research/demo
python listed-equity-research/scripts/dcf_sotp.py listed-equity-research/assets/valuation.example.json --output research/demo-valuation.json
```

**評価用のサンプル値は架空です。** プログラムは入力の構造確認と計算を行いますが、インターネット上の財務数値の真正性確認やPDF/Office文書作成はホスト側の機能に依存します。

## 使用上の注意

1. 数値には一次資料URL、公開日、会計期間、通貨、表・ページ番号を記録する。
2. 開示事実、公式統計、コンセンサス、証券会社予測、自社推計、架空例を明確に区分する。
3. 投資売却益は売上高ではなく、OCI評価益も当期利益ではない。調整後利益は自由現金とは異なる。
4. SOTPでは戦略投資、余剰現金、税金、リース、株式報酬、自社株買いと希薄化を二重計上しない。
5. 通貨を一致させた名目キャッシュフロー／割引率を用い、ターミナルバリュー依存度を開示する。
6. 重要な入力が欠ける場合は `screen-grade` / `not-decision-ready` と表示し、根拠のない精密目標株価を作らない。

詳細：[SKILL.md](listed-equity-research/SKILL.md) · [インストール](listed-equity-research/INSTALL.md) · [評価方法](listed-equity-research/references/valuation.md) · [美団事例](listed-equity-research/examples/meituan-case-methodology.md)。

[貢献](CONTRIBUTING.md) · [セキュリティ](SECURITY.md) · [MITライセンス](LICENSE)。

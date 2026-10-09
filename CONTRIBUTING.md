# Contributing / 贡献指南

Contributions are welcome for industry-specific valuation methods, data provenance, tests, charts, and translations.

## Rules

1. Preserve evidence quality: every real-company fact must reference public original sources with URL, period, currency and page/table location.
2. Treat broker extracts and proprietary research as copyrighted. Do **not** commit paid reports, confidential datasets, personal financial data, credentials or access tokens.
3. Clearly label real reported facts, consensus estimates, internal analyst estimates, calculations and fictional examples.
4. Do not silently change historical figures or model assumptions without an audit note.
5. Add synthetic tests for new financial logic and regression tests for failure cases.
6. Keep all five README translations consistent when adding or removing major features.
7. If editing the installable skill, run `python scripts/update_manifest.py` and commit the updated `MANIFEST.json`.
8. Before a pull request, run:

```bash
python listed-equity-research/scripts/verify_install.py listed-equity-research
python listed-equity-research/scripts/self_test.py
python scripts/install_skill.py --root /tmp/research-skills --test
```

## Pull request description

Explain the research or software problem, affected accounting principles, source rules, test results, and potential compatibility changes. For significant changes, discuss in an issue first.

All contributions are offered under the repository's MIT license.

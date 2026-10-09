#!/usr/bin/env python3
"""Create an EMPTY, source-auditable listed-company research workspace."""
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--company', required=True)
    p.add_argument('--ticker', required=True)
    p.add_argument('--exchange', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--language', default='zh-CN')
    args = p.parse_args()
    path = Path(args.output).resolve()
    if path.exists() and any(path.iterdir()):
        raise SystemExit(f'Refusing to overwrite nonempty directory: {path}')
    path.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    for name in ('sources.csv', 'metrics.csv', 'assumptions.csv', 'issues.csv', 'charts.json'):
        shutil.copy2(root / 'assets' / name, path / name)
    config = {
        'company': args.company, 'ticker': args.ticker, 'exchange': args.exchange,
        'language': args.language, 'project_started_utc': datetime.now(timezone.utc).isoformat(),
        'data_cutoff': '', 'report_date': '', 'price_timestamp': '',
        'statement_currency': '', 'quote_currency': '', 'mode': 'deep-dive',
        'evidence_confidence': 'unverified', 'valuation_status': 'not-decision-ready',
        'notes': 'Fill primary sources and exact source locations before analysis.'
    }
    (path / 'project.json').write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
    report = (root / 'assets' / 'report-template.md').read_text(encoding='utf-8')
    for key in ('company', 'ticker', 'report_date', 'data_cutoff', 'price_timestamp',
                'reporting_currency', 'quote_currency', 'evidence_confidence', 'valuation_status'):
        value = config.get(key, '')
        if key == 'reporting_currency':
            value = config['statement_currency']
        report = report.replace('{{' + key + '}}', str(value or f'[待填写:{key}]'))
    (path / 'report.md').write_text(report, encoding='utf-8')
    (path / 'outputs' / 'charts').mkdir(parents=True, exist_ok=True)
    print(f'Created empty research workspace at: {path}')
    print('No company financial data, market prices or consensus estimates were inferred.')


if __name__ == '__main__':
    main()

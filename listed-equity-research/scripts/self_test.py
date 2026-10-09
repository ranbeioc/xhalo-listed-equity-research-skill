#!/usr/bin/env python3
"""Local smoke tests with obviously FICTIONAL values; never financial evidence."""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
py = sys.executable
with tempfile.TemporaryDirectory() as td:
    project = Path(td) / 'FICTIONAL'
    subprocess.run([py, str(root/'scripts/new_project.py'), '--company', 'FICTIONAL DEMO',
                    '--ticker', 'TEST', '--exchange', 'NONE', '--output', str(project)], check=True)
    file = project / 'metrics.csv'
    with file.open('a', encoding='utf-8', newline='') as stream:
        w = csv.writer(stream)
        for i, (year, v) in enumerate([(2023, 12.3), (2024, 13.9), (2025, 16.4)], start=1):
            w.writerow([f'M{i:03d}', 'Fictional demo', str(year), 'Fictional revenue', v,
                        'arbitrary units', 'illustrative', '', '', '', 'Synthetic test values'])
    (project/'charts.json').write_text(json.dumps([{
        'id':'fictional-chart', 'title':'虚构数据/演示，不可引用', 'type':'line',
        'metric_ids':['M001','M002','M003'], 'series_key':'metric', 'unit':'arbitrary units',
        'source_ids':[], 'data_cutoff':'FICTIONAL', 'note':'用于测试绘图系统。'
    }], ensure_ascii=False, indent=2), encoding='utf-8')
    subprocess.run([py, str(root/'scripts/validate_research.py'), str(project)], check=True)
    try:
        import matplotlib
    except ImportError:
        print('Skipping chart rendering test (matplotlib not installed).')
    else:
        subprocess.run([py, str(root/'scripts/render_charts.py'), str(project)], check=True)
        assert (project/'outputs/charts/fictional-chart.png').is_file()
    subprocess.run([py, str(root/'scripts/dcf_sotp.py'), str(root/'assets/valuation.example.json'),
                    '--output', str(project/'valuation-result.json')], check=True)
    j = json.loads((project/'valuation-result.json').read_text(encoding='utf-8'))
    assert j['per_share_value_quote_currency'] > 0
    assert j['status'] == 'screen-grade'
    print('PASS: scaffolding, provenance validation, sourced-chart pipeline, DCF arithmetic')

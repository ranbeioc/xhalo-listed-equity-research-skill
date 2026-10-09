#!/usr/bin/env python3
"""Validate research ledgers, references, chart provenance and obvious math/data errors.

Exit 2 on structural/evidence errors. Exit 1 on warnings when --strict. Does not
verify external URLs or the underlying economic accuracy of any claim.
"""
import argparse
import csv
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

VALID_BASIS = {'reported', 'official-stat', 'consensus', 'broker', 'expert-estimate',
               'analyst-estimate', 'derived', 'illustrative', 'unknown'}
REQUIRED_PROJECT = ('company', 'ticker', 'exchange')


def rows(path, errors):
    if not path.is_file():
        errors.append(f'Missing required file: {path.name}')
        return []
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def nonempty(x):
    return bool(x is not None and str(x).strip())


def valid_date(value):
    if not value:
        return True
    try:
        date.fromisoformat(value.strip())
        return True
    except ValueError:
        return False


def separated_ids(s):
    return [part.strip() for part in re.split(r'[;,|]', s or '') if part.strip()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--strict', action='store_true', help='Treat warnings as failure')
    args = parser.parse_args()
    folder = args.project.resolve()
    err, warn = [], []
    if not (folder / 'project.json').is_file():
        raise SystemExit('Missing project.json; run new_project.py first')
    cfg = json.loads((folder / 'project.json').read_text(encoding='utf-8'))
    for field in REQUIRED_PROJECT:
        if not nonempty(cfg.get(field)):
            err.append(f'Missing project field: {field}')
    for key in ('data_cutoff', 'report_date'):
        if cfg.get(key) and not valid_date(cfg[key]):
            err.append(f'Invalid {key} (expected YYYY-MM-DD)')
        if not cfg.get(key):
            warn.append(f'Unset {key}')
    if not cfg.get('price_timestamp'):
        warn.append('No market price as-of timestamp')
    sources = rows(folder / 'sources.csv', err)
    source_ids = set()
    for i, r in enumerate(sources, start=2):
        sid = (r.get('source_id') or '').strip()
        if not sid or sid in source_ids:
            err.append(f'sources.csv:{i}: invalid/duplicate source_id {sid!r}')
        source_ids.add(sid)
        if not all(nonempty(r.get(k)) for k in ('publisher', 'document_title', 'url', 'publication_date')):
            err.append(f'sources.csv:{i}: publisher/title/url/publication_date required')
        url = urlparse((r.get('url') or '').strip())
        if url.scheme not in {'http', 'https'} or not url.netloc:
            err.append(f'sources.csv:{i}: invalid URL')
        if not valid_date(r.get('publication_date')):
            err.append(f'sources.csv:{i}: publication_date invalid')
        if not r.get('source_locator'):
            warn.append(f'sources.csv:{i}: missing page/table locator')
    if not sources:
        warn.append('No sources in sources.csv')

    metrics = rows(folder / 'metrics.csv', err)
    metric_ids, metric_details = set(), {}
    for i, r in enumerate(metrics, start=2):
        mid = (r.get('metric_id') or '').strip()
        if not mid or mid in metric_ids:
            err.append(f'metrics.csv:{i}: missing/duplicate metric_id {mid!r}')
        metric_ids.add(mid)
        metric_details[mid] = r
        for field in ('entity', 'period', 'metric', 'unit', 'basis'):
            if not nonempty(r.get(field)):
                err.append(f'metrics.csv:{i}: missing {field}')
        if r.get('basis') not in VALID_BASIS:
            err.append(f'metrics.csv:{i}: invalid basis {r.get("basis")!r}')
        value = (r.get('value') or '').strip()
        if r.get('basis') != 'unknown':
            try:
                if not math.isfinite(float(value)):
                    raise ValueError()
            except (TypeError, ValueError):
                err.append(f'metrics.csv:{i}: nonnumeric/nonfinite value')
        src = separated_ids(r.get('source_ids'))
        if not src and r.get('basis') not in {'unknown', 'illustrative'}:
            err.append(f'metrics.csv:{i}: missing source_ids')
        for sid in src:
            if sid not in source_ids:
                err.append(f'metrics.csv:{i}: unknown source_id {sid}')
        if r.get('basis') == 'derived' and not r.get('derivation'):
            err.append(f'metrics.csv:{i}: derived metric requires derivation formula')
        if r.get('basis') == 'reported' and not (r.get('source_locator') or '').strip():
            warn.append(f'metrics.csv:{i}: reported metric lacks specific source locator')
    if not metrics:
        warn.append('No measured metrics in metrics.csv')

    assumptions = rows(folder / 'assumptions.csv', err)
    for i, r in enumerate(assumptions, start=2):
        if not all(nonempty(r.get(k)) for k in ('assumption_id', 'scenario', 'driver', 'value', 'unit', 'rationale')):
            err.append(f'assumptions.csv:{i}: id/scenario/driver/value/unit/rationale required')
        for sid in separated_ids(r.get('source_ids')):
            if sid not in source_ids:
                err.append(f'assumptions.csv:{i}: unknown source_id {sid}')
    issues = rows(folder / 'issues.csv', err)
    if issues:
        open_critical = [r for r in issues if r.get('severity', '').lower() in ('critical', 'blocker') and r.get('status', '').lower() not in ('resolved', 'closed')]
        if open_critical:
            warn.append(f'{len(open_critical)} critical issue(s) remain unresolved')
    chart_file = folder / 'charts.json'
    if chart_file.is_file():
        try:
            charts = json.loads(chart_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            err.append(f'Invalid charts.json: {exc}')
            charts = []
    else:
        err.append('Missing charts.json')
        charts = []
    if not isinstance(charts, list):
        err.append('charts.json must be a JSON array')
        charts = []
    chart_ids = set()
    for c in charts:
        cid = c.get('id', '')
        if not cid or cid in chart_ids:
            err.append(f'Invalid/duplicate chart ID {cid}')
        chart_ids.add(cid)
        if c.get('type') not in {'bar', 'line', 'pie'}:
            err.append(f'{cid}: unsupported chart type')
        mids = c.get('metric_ids', [])
        if not mids:
            err.append(f'{cid}: chart without metric_ids')
        for mid in mids:
            if mid not in metric_ids:
                err.append(f'{cid}: unknown metric_id {mid}')
        expected = {sid for mid in mids if mid in metric_details
                    for sid in separated_ids(metric_details[mid].get('source_ids'))}
        chart_sources = set(c.get('source_ids') or [])
        if not expected.issubset(chart_sources):
            err.append(f'{cid}: chart missing provenance source_ids {sorted(expected - chart_sources)}')
        if not c.get('title') or not c.get('unit'):
            err.append(f'{cid}: missing title or unit')
    if not charts:
        warn.append('No chart definitions yet; complete reports should include real charts')

    report_file = folder / 'report.md'
    if not report_file.is_file():
        err.append('Missing report.md')
    else:
        report_text = report_file.read_text(encoding='utf-8')
        report_refs = set(re.findall(r'\bS\d{3,}\b', report_text))
        unknown_refs = report_refs - source_ids
        if unknown_refs:
            err.append(f'Report cites nonexistent source_ids: {sorted(unknown_refs)}')
        if '[待填写:' in report_text or '{{' in report_text:
            warn.append('Report still contains template placeholders')
        if not report_refs:
            warn.append('Report contains no S### source citations')

    if not err and not warn:
        label = 'PASS: structurally valid; substantive source checking still required'
    elif err:
        label = f'FAIL: {len(err)} error(s), {len(warn)} warning(s)'
    else:
        label = f'WARNING: {len(warn)} warning(s)'
    print(label)
    for line in err:
        print('ERROR:', line)
    for line in warn:
        print('WARN :', line)
    print(f'Checked {len(sources)} source(s), {len(metrics)} metric(s), {len(assumptions)} assumption(s), {len(charts)} chart(s).')
    if err:
        return 2
    if warn and args.strict:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

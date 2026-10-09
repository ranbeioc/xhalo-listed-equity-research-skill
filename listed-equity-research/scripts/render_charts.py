#!/usr/bin/env python3
"""Render sourced line, bar and pie charts declared in a project's charts.json.

All points come from metrics.csv. Order of metric_ids is explicit (no invented
interpolation). Chart source_ids must cover every point's source_ids.
Requires matplotlib. Output includes a provenance caption and chart_manifest.json.
"""
import argparse
import csv
import json
from collections import OrderedDict
from pathlib import Path


def source_ids(value):
    import re
    return [v.strip() for v in re.split(r'[;,|]', value or '') if v.strip()]


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('project', type=Path)
    args = a.parse_args()
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit('Matplotlib required: pip install matplotlib') from exc

    # Register a local CJK font when available; no fonts are bundled or exported.
    try:
        import subprocess
        from matplotlib import font_manager
        pth = subprocess.check_output(
            ['fc-match', '-f', '%{file}', 'Noto Sans CJK SC'],
            text=True, stderr=subprocess.DEVNULL, timeout=2).strip()
        if pth and Path(pth).is_file():
            font_manager.fontManager.addfont(pth)
            detected = font_manager.FontProperties(fname=pth).get_name()
            plt.rcParams['font.sans-serif'] = [detected, 'Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        else:
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    except (OSError, subprocess.SubprocessError):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    path = args.project
    metrics_path = path / 'metrics.csv'
    charts_path = path / 'charts.json'
    if not (metrics_path.is_file() and charts_path.is_file()):
        raise SystemExit('Project must contain metrics.csv and charts.json')
    with metrics_path.open(encoding='utf-8-sig', newline='') as f:
        metrics = {r['metric_id']: r for r in csv.DictReader(f)}
    charts = json.loads(charts_path.read_text(encoding='utf-8'))
    if not charts:
        print('No charts defined. Add data and sourced chart specs to charts.json.')
        return
    output_dir = path / 'outputs' / 'charts'
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for c in charts:
        cid = c['id']
        if not cid.replace('-', '').replace('_', '').isalnum():
            raise ValueError(f'Chart ID must be alphanumeric/hyphens: {cid}')
        pts = []
        for mid in c['metric_ids']:
            if mid not in metrics:
                raise ValueError(f'{cid}: unknown metric_id {mid}')
            r = metrics[mid]
            pts.append({'id': mid, 'x': r['period'], 'y': float(r['value']),
                        'series': r[c.get('series_key', 'metric')], 'unit': r['unit'],
                        'sources': source_ids(r.get('source_ids')), 'basis': r.get('basis', '')})
        if len({p['unit'] for p in pts}) != 1:
            raise ValueError(f'{cid}: mixed-unit plot is not allowed')
        if pts[0]['unit'] != c['unit']:
            raise ValueError(f'{cid}: chart unit {c["unit"]!r} does not equal data unit {pts[0]["unit"]!r}')
        if c['type'] == 'pie' and len({p['x'] for p in pts}) != 1:
            raise ValueError(f'{cid}: pie slices must use the same reporting period')
        required = {source for p in pts for source in p['sources']}
        if not required.issubset(set(c.get('source_ids') or [])):
            raise ValueError(f'{cid}: charts.json provenance missing {required-set(c.get("source_ids") or [])}')
        fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=160)
        fig.patch.set_facecolor('white')
        ctype = c['type']
        if ctype == 'pie':
            labels = [p['x'] + ' ' + p['series'] for p in pts]
            values = [p['y'] for p in pts]
            if any(v < 0 for v in values) or sum(values) <= 0:
                raise ValueError(f'{cid}: pie requires nonnegative parts summing > 0')
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        elif ctype in ('bar', 'line'):
            xkeys = list(OrderedDict((p['x'], None) for p in pts))
            series_names = list(OrderedDict((p['series'], None) for p in pts))
            xs = list(range(len(xkeys)))
            grouped = {(p['series'], p['x']):p['y'] for p in pts}
            if ctype == 'line':
                for name in series_names:
                    values = [grouped.get((name, key), float('nan')) for key in xkeys]
                    ax.plot(xs, values, marker='o', linewidth=2, label=name)
            else:
                bw = 0.75 / len(series_names)
                for s, name in enumerate(series_names):
                    pos = [x + (s-(len(series_names)-1)/2)*bw for x in xs]
                    values = [grouped.get((name, key), 0) for key in xkeys]
                    ax.bar(pos, values, width=bw, label=name)
            ax.set_xticks(xs, xkeys, rotation=35 if len(xs)>6 else 0, ha='right' if len(xs)>6 else 'center')
            ax.axhline(0, linewidth=.75)
            ax.grid(axis='y', alpha=.19)
            ax.set_axisbelow(True)
            ax.set_ylabel(c['unit'])
            if len(series_names)>1:
                ax.legend(loc='best', frameon=False)
        else:
            raise ValueError(f'{cid}: invalid type {ctype}')
        ax.set_title(c['title'], pad=14, fontsize=12)
        caption = ('来源: ' + ', '.join(sorted(required))) if required else '来源：无（仅用于虚构演示）'
        if any(p['basis'] == 'illustrative' for p in pts):
            caption = '演示/虚构数据，不得用于投资分析  |  ' + caption
        if c.get('data_cutoff'):
            caption += '  | 截止: ' + c['data_cutoff']
        if c.get('note'):
            caption += '\n' + c['note']
        fig.text(.065, .01, caption, fontsize=8, va='bottom', color='#565656')
        fig.subplots_adjust(bottom=.23 if c.get('note') else .16, top=.88, left=.11, right=.96)
        out = output_dir / (cid+'.png')
        fig.savefig(out, bbox_inches='tight', dpi=170)
        plt.close(fig)
        manifest.append({'chart_id': cid, 'file': str(out.relative_to(path)), 'source_ids': sorted(required),
                         'metric_ids': c['metric_ids'], 'data_cutoff': c.get('data_cutoff',''), 'title': c['title']})
        print('Wrote', out)
    (path / 'outputs' / 'chart_manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'{len(manifest)} sourced chart(s) rendered; review images and report references before publication.')


if __name__ == '__main__':
    main()

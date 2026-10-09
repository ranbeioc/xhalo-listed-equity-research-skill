#!/usr/bin/env python3
"""Deterministic SOTP of discounted FCFF streams; NOT an economic input validator.

Input segments have equally long annual streams; t=1 is next year-end. All amounts
must use the same value_unit. Terminal FCF is allowed to be negative but warned.
"""
import argparse
import json
import math
from pathlib import Path


def number(obj, key, label):
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label}: {key} must be a finite number')
    return float(value)


def compute(data):
    warnings = []
    fx = number(data, 'fx_quote_per_report', 'root')
    shares = number(data, 'diluted_shares', 'root')
    if fx <= 0 or shares <= 0:
        raise ValueError('fx_quote_per_report and diluted_shares must be positive')
    if data.get('share_unit') != 'hundred_million_shares':
        raise ValueError('share_unit must be hundred_million_shares to avoid unit mistakes')
    if data.get('value_unit') != 'hundred_million_report_currency':
        raise ValueError('value_unit must be hundred_million_report_currency')
    if not data.get('segments'):
        raise ValueError('At least one segment is required')
    first_length = len(data['segments'][0]['fcff'])
    if first_length < 3:
        warnings.append('Forecast period < 3 years; terminal dominates many cases')
    rows, total_ev, total_tv = [], 0.0, 0.0
    for seg in data['segments']:
        name = seg.get('name') or '(unnamed)'
        r, g = number(seg, 'wacc', name), number(seg, 'terminal_g', name)
        flows = seg.get('fcff')
        if not isinstance(flows, list) or not flows or len(flows) != first_length:
            raise ValueError(f'{name}: all segments must have equal-length nonempty fcff arrays')
        if r <= g or r <= -1 or g <= -1:
            raise ValueError(f'{name}: WACC must exceed g; both > -100%')
        if r > 0.5:
            warnings.append(f'{name}: unusually high WACC ({r:.1%}); check percent vs decimal')
        if g > 0.10:
            warnings.append(f'{name}: unusually high terminal growth ({g:.1%})')
        vals = []
        for j, value in enumerate(flows, start=1):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f'{name}: invalid FCFF in forecast year {j}')
            vals.append(float(value))
        npv_explicit = sum(c / ((1+r)**i) for i,c in enumerate(vals, start=1))
        terminal = vals[-1] * (1+g) / (r-g)
        terminal_pv = terminal / ((1+r)**len(vals))
        ev = npv_explicit + terminal_pv
        if vals[-1] < 0:
            warnings.append(f'{name}: negative terminal FCFF: confirm whether a continuing corporate cost or an unsustainable operating loss')
        share = terminal_pv / ev if ev > 0 else None
        if share is not None and share > 0.60:
            warnings.append(f'{name}: terminal share of PV {share:.1%} > 60%; stress ROIC/reinvestment')
        rows.append({
            'segment': name, 'wacc': r, 'terminal_g': g, 'years': len(vals),
            'pv_explicit_fcff': round(npv_explicit, 6),
            'terminal_value_at_year_n': round(terminal, 6),
            'pv_terminal': round(terminal_pv, 6), 'enterprise_value': round(ev, 6),
            'terminal_fraction_of_segment_ev': round(share, 4) if share is not None else None,
        })
        total_ev += ev
        total_tv += terminal_pv
    bridge = data.get('bridge')
    if not isinstance(bridge, dict):
        raise ValueError('bridge must be an object')
    items = {
        'excess_cash': number(bridge, 'excess_cash', 'bridge'),
        'financial_investments_after_tax': number(bridge, 'financial_investments_after_tax', 'bridge'),
        'interest_bearing_debt': -number(bridge, 'interest_bearing_debt', 'bridge'),
        'lease_liabilities': -number(bridge, 'lease_liabilities', 'bridge'),
        'minority_interest': -number(bridge, 'minority_interest', 'bridge'),
        'other_net_adjustments': number(bridge, 'other_net_adjustments', 'bridge'),
    }
    if not data.get('double_counting_reviewed'):
        warnings.append('Bridge double-counting has NOT been independently reviewed')
    if data.get('sbc_method') not in {'economic_cost_in_fcff', 'dynamic_diluted_shares'}:
        warnings.append('SBC handling is not specified as one of the two consistent methods')
    if 'ILLUSTRATIVE' in str(data.get('label', '')):
        warnings.append('Illustrative example, not a real company valuation')
    equity = total_ev + sum(items.values())
    if equity <= 0:
        warnings.append('Equity value nonpositive; price per share is not informative')
    price = equity * fx / shares
    return {
        'label': data.get('label', ''), 'method': 'FCFF SOTP using year-end discounting',
        'valuation_currency': data.get('report_currency'), 'share_currency': data.get('quote_currency'),
        'fx_quote_per_report': fx, 'diluted_shares_hundred_million': shares,
        'value_unit': 'hundred million reporting currency',
        'segments': rows,
        'enterprise_value': round(total_ev, 6),
        'bridge_sign_adjusted': {k: round(v, 6) for k,v in items.items()},
        'equity_value': round(equity, 6),
        'per_share_value_quote_currency': round(price, 6),
        'aggregate_terminal_fraction': round(total_tv / total_ev, 4) if total_ev>0 else None,
        'status': 'screen-grade',
        'warnings': warnings,
        'important': 'Mathematics only. Source authenticity, forecasts, inflation/currency, ROIC, taxes, leases and SBC require analyst audit.',
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    data = json.loads(a.input.read_text(encoding='utf-8'))
    result = compute(data)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(rendered+'\n', encoding='utf-8')
        print('Wrote', a.output)
    else:
        print(rendered)
    print('Equity per share:', round(result['per_share_value_quote_currency'], 4),
          result['share_currency'], '| status:', result['status'])
    for msg in result['warnings']:
        print('WARNING:', msg)


if __name__ == '__main__':
    main()

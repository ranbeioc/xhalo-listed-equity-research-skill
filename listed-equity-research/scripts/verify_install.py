#!/usr/bin/env python3
"""Verify every file in the distributed listed-equity-research skill.

Run: python scripts/verify_install.py [skill_directory]
No network access and no third-party libraries required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    p = argparse.ArgumentParser(description='Verify installed skill files against MANIFEST.json')
    p.add_argument('directory', nargs='?', default=str(Path(__file__).resolve().parent.parent))
    args = p.parse_args()
    root = Path(args.directory).expanduser().resolve()
    manifest_path = root / 'MANIFEST.json'
    if not manifest_path.is_file():
        print(f'ERROR: Missing manifest: {manifest_path}', file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    missing, mismatched = [], []
    for item in manifest['files']:
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            mismatched.append((str(rel), 'invalid path'))
            continue
        path = root / rel
        if not path.is_file():
            missing.append(str(rel))
            continue
        buf = path.read_bytes()
        if hashlib.sha256(buf).hexdigest() != item['sha256'] or len(buf) != item['bytes']:
            mismatched.append((str(rel), 'digest/size mismatch'))
    for item in missing:
        print('MISSING:', item)
    for item, msg in mismatched:
        print('INVALID:', item, msg)
    for required in ('SKILL.md', 'README.md', 'references', 'assets', 'scripts', 'examples'):
        if not (root / required).exists():
            print('REQUIRED COMPONENT MISSING:', required)
            missing.append(required)
    if missing or mismatched:
        print(f'FAIL: missing={len(missing)}, mismatched={len(mismatched)}')
        return 1
    print(f"PASS: {manifest['name']} v{manifest['version']} | {len(manifest['files'])} files verified")
    return 0


if __name__ == '__main__':
    sys.exit(main())

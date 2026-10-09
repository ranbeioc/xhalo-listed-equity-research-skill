#!/usr/bin/env python3
"""Safely install the complete local skill without network access."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Install listed-equity-research from this checkout")
    parser.add_argument("--root", required=True, help="Parent directory for all agent skills")
    parser.add_argument("--test", action="store_true", help="Run offline synthetic smoke test after copying")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / "listed-equity-research"
    verifier = source / "scripts" / "verify_install.py"
    subprocess.run([sys.executable, str(verifier), str(source)], check=True)
    parent = Path(args.root).expanduser().resolve()
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / "listed-equity-research"
    if target.exists():
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = parent / f"listed-equity-research.backup-{now}"
        counter = 1
        while backup.exists():
            backup = parent / f"listed-equity-research.backup-{now}-{counter}"
            counter += 1
        target.rename(backup)
        print("Backed up old installation:", backup)
    shutil.copytree(source, target)
    subprocess.run([sys.executable, str(target / "scripts" / "verify_install.py"), str(target)], check=True)
    if args.test:
        subprocess.run([sys.executable, str(target / "scripts" / "self_test.py")], check=True)
    print("Skill installed:", target)
    print("Restart or refresh the host Agent skill index if necessary.")

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("INSTALL FAILED:", exc, file=sys.stderr)
        sys.exit(1)

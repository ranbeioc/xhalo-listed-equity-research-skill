#!/usr/bin/env python3
"""Regenerate the SHA-256 manifest for a modified skill distribution."""
import hashlib
import json
from pathlib import Path

skill = Path(__file__).resolve().parent.parent / "listed-equity-research"
manifest_path = skill / "MANIFEST.json"
old = json.loads(manifest_path.read_text("utf-8")) if manifest_path.exists() else {}
entries = []
for item in sorted(skill.rglob("*")):
    if not item.is_file() or item.name == "MANIFEST.json" or "__pycache__" in item.parts or item.suffix == ".pyc":
        continue
    raw = item.read_bytes()
    entries.append({"path": item.relative_to(skill).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
data = {"name": "listed-equity-research", "version": old.get("version", "1.0.1"), "files": entries}
manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Manifest updated:", len(entries), "files")

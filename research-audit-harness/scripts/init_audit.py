#!/usr/bin/env python3
"""Initialize audit tables for a research direction without silent overwrites."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from audit import PROTOCOL_PROFILES


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("direction", type=Path, help="Existing or new research-direction directory")
    parser.add_argument("--force", action="store_true", help="Replace existing audit template files")
    parser.add_argument("--profile", choices=sorted(PROTOCOL_PROFILES), default="finance", help="Protocol profile for new metadata (default: finance)")
    args = parser.parse_args()

    direction = args.direction.resolve()
    template_dir = Path(__file__).resolve().parent.parent / "templates" / "audit"
    target_dir = direction / "audit"
    direction.mkdir(parents=True, exist_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    for source in sorted(template_dir.iterdir()):
        if not source.is_file():
            continue
        destination = target_dir / source.name
        if destination.exists() and not args.force:
            print(f"SKIP existing: {destination}")
            skipped += 1
            continue
        if source.name == "project.json":
            project = json.loads(source.read_text(encoding="utf-8"))
            project["audit_profile"] = args.profile
            project["protocol"] = dict.fromkeys(PROTOCOL_PROFILES[args.profile], False)
            destination.write_text(json.dumps(project, indent=2) + "\n", encoding="utf-8")
        else:
            shutil.copy2(source, destination)
        print(f"COPY: {destination}")
        copied += 1

    print(f"Initialized {copied} file(s); skipped {skipped} existing file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())


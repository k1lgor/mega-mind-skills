#!/usr/bin/env python
"""Sync .agent/ (development source) -> src/mega_mind/assets/ (distribution source).

Runs manifest generation and doc rendering BEFORE copying, so both trees carry
byte-identical generated output. After the copy, every file is verified by
content hash — a count match is no longer enough.

Usage:
    python scripts/sync-assets.py            # generate, copy, verify
    python scripts/sync-assets.py --check    # verify sync state without copying
"""

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = ROOT / ".agent"
ASSETS_DIR = ROOT / "src" / "mega_mind" / "assets"


def run_step(name: str, cmd: list[str]) -> None:
    print(f"  {name}...")
    result = subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)
    if result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            print(f"    {line}")
    if result.returncode != 0:
        if result.stderr.strip():
            for line in result.stderr.strip().splitlines():
                print(f"    {line}", file=sys.stderr)
        sys.exit(f"[ERROR] {name} failed with exit code {result.returncode}")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_files(directory: Path) -> dict[str, Path]:
    """Map relative path -> file, excluding pycache and local-only dirs."""
    files = {}
    for item in sorted(directory.rglob("*")):
        if item.is_dir():
            continue
        rel = item.relative_to(directory)
        parts = rel.parts
        if any(part in ("__pycache__", ".pytest_cache") for part in parts):
            continue
        # instincts/ and evals/ are local session state (gitignored), not shipped
        if parts[0] in ("instincts", "evals"):
            continue
        files[str(rel).replace("\\", "/")] = item
    return files


def verify_sync() -> list[str]:
    """Return a list of drift descriptions (empty == fully in sync)."""
    drift = []
    agent_files = collect_files(AGENT_DIR)
    asset_files = collect_files(ASSETS_DIR)

    for rel, src in agent_files.items():
        dest = ASSETS_DIR / rel
        if rel not in asset_files:
            drift.append(f"missing in assets/: {rel}")
        elif sha256_of(src) != sha256_of(dest):
            drift.append(f"content drift: {rel}")
    for rel in asset_files:
        if rel not in agent_files and not rel.startswith("hooks/"):
            drift.append(f"extra in assets/ (not in .agent/): {rel}")
    return drift


def main() -> int:
    check_only = "--check" in sys.argv
    print("Syncing .agent/ -> src/mega_mind/assets/")
    print("=" * 50)

    if not check_only:
        # 1. Regenerate the manifest so it reflects current content
        run_step("building skills manifest", ["scripts/build-manifest.py"])
        # 2. Re-render generated doc regions from the manifest
        run_step("rendering generated docs", ["scripts/render-skills.py"])
        # 3. Copy the tree
        shutil.copytree(AGENT_DIR, ASSETS_DIR, dirs_exist_ok=True)
        print("  tree copied")

    drift = verify_sync()
    if drift:
        print(f"\n[DRIFT] {len(drift)} issue(s):")
        for d in drift:
            print(f"  - {d}")
        return 1
    print("\n[OK] .agent/ and assets/ are byte-identical (content-hash verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

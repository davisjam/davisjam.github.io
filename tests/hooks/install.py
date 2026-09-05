#!/usr/bin/env python3
"""Install the repository's git hooks. Run once per clone."""
import pathlib
import shutil
import stat

root = pathlib.Path(__file__).resolve().parent.parent.parent
for src in (root / "tests/hooks").glob("pre-*"):
    dst = root / ".git/hooks" / src.name
    shutil.copy2(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IEXEC)
    print(f"  installed {src.name}")

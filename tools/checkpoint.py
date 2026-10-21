#!/usr/bin/env python3
"""Session checkpoint: makes "the code is the truth, the status file is the map" mechanical.

    python tools/checkpoint.py                    START of a session: what changed since the last checkpoint?
    python tools/checkpoint.py --write "label"    END of a session, after the checks pass: record a new checkpoint

Verify mode (read-only) does four things:
  1. Compares every tracked text file with the fingerprints saved in CHECKPOINT.json (line endings are ignored).
  2. Rebuilds the pages in a scratch copy and confirms the saved root .html files match
     (catches hand-edits to generated files, or a builder change that was never rebuilt).
  3. Runs tools/check-links.py.
  4. Prints the git state, if git is available.
It exits 0 when everything matches and 1 when something differs. The lists say exactly what.

Not covered here (separate steps): the accessibility scan (tools/a11y-check.py, needs axe-core) and anything that
can only be judged by eye. Images and fonts are tracked by file name only, because the copy on a computer can
differ in size from the cloud workspace copy (an invisible provenance tag is added when Claude saves images).
"""
import datetime
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
MANIFEST = ROOT / "CHECKPOINT.json"

TEXT_GLOBS = ["*.html", "*.md", "css/*.css", "js/*.js", "tools/*.py", "tools/pages/*.html", "research/*.md"]
ASSET_GLOBS = ["images/*", "fonts/*", "research/photos/**/*"]
SPRITE = "tools/pages/_sprite.html"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_pages", TOOLS / "build-pages.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fingerprint(path, builder):
    data = path.read_bytes()
    if path.relative_to(ROOT).as_posix() == SPRITE:
        # Saving this SVG partial to a computer can add a provenance <metadata> block. Fingerprint what the pages use.
        data = builder.clean_sprite(data.decode("utf-8")).encode("utf-8")
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()[:16]


def tracked_text():
    found = set()
    for pattern in TEXT_GLOBS:
        found.update(p for p in ROOT.glob(pattern) if p.is_file())
    return sorted(found)


def tracked_assets():
    found = set()
    for pattern in ASSET_GLOBS:
        found.update(p for p in ROOT.glob(pattern) if p.is_file())
    return sorted(p.relative_to(ROOT).as_posix() for p in found)


def git(*args):
    if not shutil.which("git") or not (ROOT / ".git").exists():
        return None
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def compare_to_manifest(builder):
    problems = []
    if not MANIFEST.exists():
        print("  No CHECKPOINT.json yet (this is the first checkpoint). Nothing to compare against.")
        return problems
    saved = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(f"  Last checkpoint: #{saved['checkpoint']} \"{saved['label']}\" ({saved['written']})")
    now = {p.relative_to(ROOT).as_posix(): fingerprint(p, builder) for p in tracked_text() if p.name != "CHECKPOINT.json"}
    old = saved["text"]
    changed = sorted(k for k in now if k in old and now[k] != old[k])
    added = sorted(k for k in now if k not in old)
    removed = sorted(k for k in old if k not in now)
    assets_now, assets_old = set(tracked_assets()), set(saved.get("assets", []))
    a_added, a_removed = sorted(assets_now - assets_old), sorted(assets_old - assets_now)
    for label, items in (("CHANGED since the checkpoint", changed), ("NEW (not in the checkpoint)", added),
                         ("MISSING (in the checkpoint, not on disk)", removed),
                         ("NEW images/fonts", a_added), ("MISSING images/fonts", a_removed)):
        if items:
            problems.append(label)
            print(f"  {label}:")
            for k in items:
                print(f"     - {k}")
    if not problems:
        print(f"  OK: all {len(now)} tracked files and {len(assets_now)} images/fonts match the checkpoint.")
    return problems


def rebuild_matches():
    """Build the site in a scratch folder and compare with the saved root pages."""
    problems = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="glp-rebuild-"))
    try:
        shutil.copytree(TOOLS, tmp / "tools", ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
        r = subprocess.run([sys.executable, str(tmp / "tools" / "build-pages.py")], cwd=tmp, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            print("  FAILED: the page builder stopped with an error:")
            print("     " + (r.stderr or r.stdout).strip().replace("\n", "\n     "))
            return ["page builder error"]
        built = sorted(p for p in tmp.glob("*.html"))
        for p in built:
            saved = ROOT / p.name
            if not saved.exists():
                problems.append(f"{p.name} is missing from the project (rebuild would create it)")
            elif p.read_bytes().replace(b"\r\n", b"\n") != saved.read_bytes().replace(b"\r\n", b"\n"):
                problems.append(f"{p.name} differs from a fresh build (edited by hand, or the builder changed and pages were not rebuilt)")
        if problems:
            print("  PROBLEM: the saved pages are not what the builder produces:")
            for x in problems:
                print(f"     - {x}")
            print("     Fix: run  python tools/build-pages.py  (or edit tools/pages/*.html instead of the root pages).")
        else:
            print(f"  OK: a fresh build reproduces all {len(built)} saved pages exactly.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return problems


def links_ok():
    r = subprocess.run([sys.executable, str(TOOLS / "check-links.py")], cwd=ROOT, capture_output=True, text=True, timeout=60)
    lines = [ln for ln in (r.stdout + r.stderr).strip().splitlines() if ln.strip()]
    if r.returncode == 0:
        print("  OK: " + (lines[0] if lines else "links checked") + "; " + (lines[-1] if lines else ""))
        return []
    print("  PROBLEM: link check failed:")
    for ln in lines:
        print("     " + ln)
    return ["link check"]


def show_git():
    head = git("rev-parse", "--short", "HEAD")
    if head is None:
        print("  (git not available here. On your computer, use Source Control in VS Code to see uncommitted changes.)")
        return
    msg = git("log", "-1", "--format=%s") or ""
    status = git("status", "--short") or ""
    n = len([ln for ln in status.splitlines() if ln.strip()])
    print(f"  Repository: {ROOT}")
    print(f"  Last commit: {head} \"{msg}\"")
    print(f"  Working tree: {'clean (nothing uncommitted)' if n == 0 else str(n) + ' file(s) changed or new since that commit'}")


def verify():
    builder = load_builder()
    print("1. Files vs. the last checkpoint")
    problems = compare_to_manifest(builder)
    print("2. Generated pages vs. a fresh build")
    problems += rebuild_matches()
    print("3. Links, anchors, images, scripts")
    problems += links_ok()
    print("4. Git")
    show_git()
    print()
    if problems:
        print("RESULT: differences found (see above). Decide which side is right before changing anything.")
        return 1
    print("RESULT: clean. The code matches the last checkpoint.")
    return 0


def write(label, force=False):
    builder = load_builder()
    print("Checking before recording a checkpoint...")
    problems = rebuild_matches() + links_ok()
    if problems and not force:
        print("\nNot recorded: fix the problems above first (or use --force if you know why).")
        return 1
    number = 1
    if MANIFEST.exists():
        number = json.loads(MANIFEST.read_text(encoding="utf-8"))["checkpoint"] + 1
    now = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    data = {
        "checkpoint": number,
        "label": label,
        "written": now,
        "git_head_when_written": git("rev-parse", "--short", "HEAD"),
        "note": "Written just before the files for this checkpoint are committed, so the commit that contains it comes after git_head_when_written.",
        "text": {p.relative_to(ROOT).as_posix(): fingerprint(p, builder) for p in tracked_text() if p.name != "CHECKPOINT.json"},
        "assets": tracked_assets(),
    }
    MANIFEST.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nCheckpoint #{number} recorded in CHECKPOINT.json ({len(data['text'])} files, {len(data['assets'])} images/fonts).")
    print(f"Next: add it to the session log in PROJECT_STATUS.md, commit, and Sync. Suggested commit message:")
    print(f'   Checkpoint {number}: {label}')
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--write"]:
        text = [a for a in args[1:] if a != "--force"]
        if not text:
            sys.exit('Usage: python tools/checkpoint.py --write "short label" [--force]')
        sys.exit(write(" ".join(text), force="--force" in args))
    if args:
        sys.exit(__doc__)
    sys.exit(verify())

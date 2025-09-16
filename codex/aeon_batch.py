#!/usr/bin/env python3
import argparse, glob, json, os, subprocess, sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))

def aeon_version_of(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    v = data.get("aeon_version")
    if not v and isinstance(data, dict) and "vault_bridge" in data:
        v = data["vault_bridge"].get("aeon_version")
    return str(v or "vX")

def run(cmd):
    print("+", " ".join(cmd), flush=True)
    p = subprocess.run(cmd, cwd=ROOT)
    if p.returncode != 0:
        sys.exit(p.returncode)

def main():
    ap = argparse.ArgumentParser(description="Batch-run AEON bridges")
    ap.add_argument("--glob", default="bridges/*.json",
                    help="glob for bridge files (default: bridges/*.json)")
    ap.add_argument("--step", choices=["all","load","init","seal","build","audit"], default="all")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    bridges = sorted(glob.glob(os.path.join(ROOT, args.glob)))
    if not bridges:
        print("no bridges found", file=sys.stderr); sys.exit(1)

    for b in bridges:
        name = os.path.splitext(os.path.basename(b))[0]
        ver  = aeon_version_of(b)
        out  = os.path.join("dist", ver, name)
        steps = ["load","init","seal","build","audit"] if args.step=="all" else [args.step]

        # always gate with load if later steps are selected
        if args.step != "load":
            run([sys.executable, "codex/aeon_cli.py", "--aeon", b, "--out", out, "load"])
        for s in steps:
            if s == "seal":
                tag = args.tag or f"CI: build {name} {ver}"
                run([sys.executable, "codex/aeon_cli.py", "--aeon", b, "--out", out, "seal", tag])
            else:
                run([sys.executable, "codex/aeon_cli.py", "--aeon", b, "--out", out, s])

if __name__ == "__main__":
    main()
"""Builds, tests, times and measures every Part 3 implementation; writes data/cross_language.csv.

Run from A12/:  python3 Part3/run_all.py [problem-dir-prefix ...]
Rules (also in README.md):
- Production files = everything except the test runner (Runner.java, test_runner.py,
  testRunner.js, test_runner.cpp). Tests are kept separate and are not measured.
- source_loc = lizard NLOC of the production files (excludes blank lines and comments).
- max_function_cc = largest lizard cyclomatic complexity of any production function.
- Timing: compile first (not timed), 1 warm-up run, then 5 measured runs of the test command
  on the same machine; median wall-clock milliseconds of the whole process (runtime start-up,
  reading the shared cases.tsv and all cases). Raw times go to Part3/evidence/timings.csv.
"""
import csv
import glob
import os
import statistics
import subprocess
import sys
import time

import lizard

ROOT = os.path.dirname(os.path.abspath(__file__))
TEAM = os.path.dirname(ROOT)
LANGS = {
    "Java": dict(dir="java", runner="Runner.java", prod="*.java",
                 build=["javac", "-d", "build", "*.java"], cmd=["java", "-cp", "build", "Runner", "../test-cases/cases.tsv"]),
    "Python": dict(dir="python", runner="test_runner.py", prod="*.py",
                   build=None, cmd=["python3", "test_runner.py", "../test-cases/cases.tsv"]),
    "JavaScript": dict(dir="javascript", runner="testRunner.js", prod="*.js",
                       build=None, cmd=["node", "testRunner.js", "../test-cases/cases.tsv"]),
    "C++": dict(dir="cpp", runner="test_runner.cpp", prod="*.hpp",
                build=["g++", "-std=c++17", "-O2", "-Wall", "-o", "build/test_runner", "test_runner.cpp"],
                cmd=["./build/test_runner", "../test-cases/cases.tsv"]),
}


def version(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True)
    text = (out.stdout + out.stderr).splitlines()
    return next(l for l in text if l and "JAVA_TOOL_OPTIONS" not in l).strip()


RUNTIMES = {
    "Java": version(["javac", "-version"]) + " / " + version(["java", "-version"]),
    "Python": version(["python3", "--version"]),
    "JavaScript": "Node.js " + version(["node", "--version"]),
    "C++": version(["g++", "--version"]) + " -std=c++17 -O2",
}
NOTES = {}  # filled from each problem's notes.csv (language, note)


def measure(prod_files):
    nloc, maxcc, top = 0, 0, ""
    for f in prod_files:
        info = lizard.analyze_file(f)
        nloc += info.nloc
        for fn in info.function_list:
            if fn.cyclomatic_complexity > maxcc:
                maxcc, top = fn.cyclomatic_complexity, fn.name
    return nloc, maxcc, top


def main(prefixes):
    problems = sorted(d for d in os.listdir(ROOT) if d[:2].isdigit() and os.path.isdir(os.path.join(ROOT, d)))
    if prefixes:
        problems = [p for p in problems if any(p.startswith(x) for x in prefixes)]
    ev = os.path.join(ROOT, "evidence")
    os.makedirs(ev, exist_ok=True)
    rows, timings = [], []
    for prob in problems:
        meta = dict(csv.reader(open(os.path.join(ROOT, prob, "test-cases", "meta.csv"))))
        notes = {r[0]: r[1] for r in csv.reader(open(os.path.join(ROOT, prob, "test-cases", "notes.csv")))}
        for lang, cfg in LANGS.items():
            wd = os.path.join(ROOT, prob, cfg["dir"])
            prod = sorted(f for f in glob.glob(os.path.join(wd, cfg["prod"])) if os.path.basename(f) != cfg["runner"])
            log = os.path.join(ev, f"{prob}_{cfg['dir']}.log")
            result, median = "not_run", ""
            with open(log, "w") as lg:
                if cfg["build"]:
                    os.makedirs(os.path.join(wd, "build"), exist_ok=True)
                    b = cfg["build"]
                    if "*.java" in b:
                        b = b[:-1] + [os.path.basename(f) for f in glob.glob(os.path.join(wd, "*.java"))]
                    r = subprocess.run(b, cwd=wd, capture_output=True, text=True)
                    lg.write(f"$ {' '.join(b)}\n{r.stdout}{r.stderr}")
                    if r.returncode:
                        result = "failed (compile error)"
                if result == "not_run":
                    times, out = [], None
                    for i in range(6):
                        t0 = time.perf_counter()
                        out = subprocess.run(cfg["cmd"], cwd=wd, capture_output=True, text=True)
                        dt = (time.perf_counter() - t0) * 1000
                        if i:
                            times.append(dt)
                        timings.append([prob, lang, "warmup" if i == 0 else f"run{i}", f"{dt:.2f}"])
                    lg.write(f"$ {' '.join(cfg['cmd'])}\n{out.stdout}{out.stderr}exit={out.returncode}\n")
                    last = (out.stdout.strip().splitlines() or ["?"])[-1]
                    result = last.replace(" passed", "") if out.returncode == 0 else f"failed {last}"
                    median = f"{statistics.median(times):.1f}"
            nloc, maxcc, top = measure(prod)
            rows.append({
                "pattern_name": meta["pattern_name"], "instance_name": meta["instance_name"], "language": lang,
                "snippet_path": "; ".join(os.path.relpath(f, TEAM) for f in prod),
                "source_loc": nloc, "max_function_cc": maxcc, "runtime_compiler": RUNTIMES[lang],
                "test_command": f"cd {os.path.relpath(wd, TEAM)} && {' '.join(cfg['cmd'])}"
                                + (f"  (build: {' '.join(cfg['build'])})" if cfg["build"] else ""),
                "test_result": result, "median_process_ms": median,
                "language_notes": notes.get(lang, "") + (f" Max-CC function: {top}." if top else ""),
            })
            print(f"{prob:48} {lang:10} {result:10} {median:>8} ms  loc={nloc:<4} cc={maxcc}")
    out_csv = os.path.join(TEAM, "data", "cross_language.csv")
    keep = []
    if prefixes and os.path.exists(out_csv):  # partial run: keep other problems' rows
        names = {r["instance_name"] for r in rows}
        keep = [r for r in csv.DictReader(open(out_csv, encoding="utf-8")) if r["instance_name"] not in names]
    cols = ["pattern_name", "instance_name", "language", "snippet_path", "source_loc", "max_function_cc",
            "runtime_compiler", "test_command", "test_result", "median_process_ms", "language_notes"]
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(sorted(keep + rows, key=lambda r: (r["snippet_path"].split("/")[1], list(LANGS).index(r["language"]))))
    tpath = os.path.join(ev, "timings.csv")
    old = []
    if prefixes and os.path.exists(tpath):
        done = {t[0] for t in timings}
        old = [r for r in csv.reader(open(tpath)) if r and r[0] not in done and r[0] != "problem"]
    with open(tpath, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["problem", "language", "run", "wall_ms"])
        w.writerows(sorted(old + timings))


if __name__ == "__main__":
    main(sys.argv[1:])

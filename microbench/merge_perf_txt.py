#Written by ChatGPT
import sys
import re
from collections import defaultdict

THRESHOLD = 0.01  # percent

# Remove template arguments and keep only the final function name
def canonicalize(func):
    # Remove template arguments: <...>
    func = re.sub(r'<[^<>]*>', '', func)
    # Remove nested templates (repeat until stable)
    while '<' in func and '>' in func:
        func = re.sub(r'<[^<>]*>', '', func)

    # Remove qualifiers (everything before last ::)
    if '::' in func:
        func = func.split('::')[-1]

    # Remove trailing spaces
    return func.strip()

def parse_file(path):
    data = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"\s*([\d.]+)%\s+\S+\s+\S+\s+\[.\]\s+(.+)", line)
            if not m:
                continue
            pct = float(m.group(1))
            func = canonicalize(m.group(2).strip())
            data[func] = data.get(func, 0.0) + pct
    return data

def main(files):
    all_funcs = defaultdict(list)

    for path in files:
        run_data = parse_file(path)
        for func, pct in run_data.items():
            all_funcs[func].append(pct)

    n = len(files)
    merged = []

    for func, pcts in all_funcs.items():
        avg = sum(pcts) / n
        if avg >= THRESHOLD:
            merged.append((avg, func))

    merged.sort(reverse=True)

    print(f"# Merged perf report (average over {n} runs)")
    print(f"# Canonicalized C++ symbols, avg >= {THRESHOLD}%\n")
    print(f"{'Avg%':>8}  Function")
    print("-" * 80)
    for avg, func in merged:
        print(f"{avg:8.2f}%  {func}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: merge_perf.sh report1.txt report2.txt ...")
        sys.exit(1)
    main(sys.argv[1:])
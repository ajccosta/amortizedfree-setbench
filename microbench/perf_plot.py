#Written by ChatGPT
import sys
import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import csv

# Target symbols
MIMALLOC_FUNC = "mi_free_block_delayed_mt"
JEMALLOC_FUNCS = {
    "native_queued_spin_lock_slowpath",
    "je_malloc_mutex_lock_slow",
    "je_tcache_bin_flush_small",
    "__pthread_mutex_unlock",
}

def parse_file(path):
    """
    Returns dict: function_name -> percent
    """
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
            func = m.group(2).strip()
            data[func] = data.get(func, 0.0) + pct
    return data

def extract_allocator_ds_smr(filename):
    """
    From: perf_allocator_ds:size_smr_update%_1.data.txt
    Extract:
      allocator, ds, smr (including optional _df suffix)
    """
    base = os.path.basename(filename)
    m = re.match(r"perf_([^_]+)_([^:]+):[^_]+_([^_]+(?:_df)?)_", base)
    if not m:
        raise ValueError(f"Filename does not match expected format: {filename}")
    allocator, ds, smr = m.group(1), m.group(2), m.group(3)
    return allocator, ds, smr

def main(files):
    # allocator_family -> list of (label, value)
    grouped = defaultdict(list)
    csv_rows = []

    for path in files:
        data = parse_file(path)
        allocator, ds, smr = extract_allocator_ds_smr(path)

        label = f"{ds}_{smr}"

        # Allocator-aware filtering
        if allocator.startswith("mi"):
            value = data.get(MIMALLOC_FUNC, 0.0)
        elif allocator.startswith("je"):
            value = sum(data.get(f, 0.0) for f in JEMALLOC_FUNCS)
        else:
            continue

        grouped[allocator].append((label, value))
        csv_rows.append({
            "allocator": allocator,
            "ds": ds,
            "smr": smr,
            "label": label,
            "value": value
        })

    # Write CSV
    csv_path = "allocator_data.csv"
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = ["allocator", "ds", "smr", "label", "value"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)

    print(f"Saved CSV: {csv_path}")

    # Generate one plot per allocator
    for allocator, entries in grouped.items():
        entries.sort(key=lambda x: x[0])
        labels = [e[0] for e in entries]
        values = [e[1] for e in entries]

        x = range(len(labels))

        plt.figure()
        plt.bar(x, values)
        plt.xticks(x, labels, rotation=45, ha="right", fontsize=6)
        plt.ylabel("Percentage of runtime")
        plt.title(f"Allocator: {allocator}")
        plt.tight_layout()

        png_path = "perf_plot.png"
        pdf_path = "perf_plot.pdf"

        plt.savefig(png_path, dpi=300)
        plt.savefig(pdf_path)
        plt.close()

        print(f"Saved: {png_path}, {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 perf_plot.py perf_*.data.txt")
        sys.exit(1)
    main(sys.argv[1:])

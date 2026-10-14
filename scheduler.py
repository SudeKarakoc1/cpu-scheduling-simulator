#!/usr/bin/env python3
"""CENG 301 - Process Scheduling Simulator (Python 3)

Examples:
  python scheduler.py --input processes.txt --algo FCFS
  python scheduler.py --input processes.txt --algo RR --quantum 4
  python scheduler.py --input processes.txt --algo ALL --quantum 4
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt

from scheduler.utils.parser import parse_processes
from scheduler.utils.gantt import print_ascii_gantt
from scheduler.utils.statistics import compute_per_process, compute_averages, format_table

from scheduler.algorithms import fcfs, sjf, srtf, rr, priority_np, priority_p

ALGO_MAP = {
    "FCFS": lambda procs, q: fcfs.run(procs),
    "SJF": lambda procs, q: sjf.run(procs),
    "SRTF": lambda procs, q: srtf.run(procs),
    "RR": lambda procs, q: rr.run(procs, q),
    "PRIO_NP": lambda procs, q: priority_np.run(procs),
    "PRIO_P": lambda procs, q: priority_p.run(procs),
}
ALGO_ORDER = ["FCFS", "SJF", "SRTF", "RR", "PRIO_NP", "PRIO_P"]

def ensure_dirs() -> None:
    Path("logs").mkdir(exist_ok=True)
    Path("graphs").mkdir(exist_ok=True)

def save_log(algo_name: str, lines: List[str]) -> str:
    ensure_dirs()
    path = Path("logs") / f"{algo_name}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)

def print_run_report(algo_name: str, result: Dict) -> Dict[str, float]:
    print("\n" + "=" * 80)
    print(f"Algorithm: {algo_name}")
    print("=" * 80)

    print("\n[1] ASCII Gantt Chart")
    print_ascii_gantt(result["segments"])

    print("\n[2] Execution Log (also saved to logs/)")
    for line in result["log"]:
        print(line)
    log_path = save_log(algo_name, result["log"])
    print(f"\nLog saved to: {log_path}")

    print("\n[3] Per-Process Statistics")
    rows = compute_per_process(result["processes"])
    print(format_table(rows))

    avgs = compute_averages(rows)
    print("\nAverages:")
    print(f"  Average Turnaround Time: {avgs['avg_turnaround']:.3f}")
    print(f"  Average Waiting Time   : {avgs['avg_waiting']:.3f}")
    print(f"  Average Response Time  : {avgs['avg_response']:.3f}")
    print(f"  Context Switches       : {result['context_switches']}")
    return {**avgs, "context_switches": float(result["context_switches"])}

def print_comparison_table(summary: Dict[str, Dict[str, float]], rr_q: int) -> None:
    print("\n" + "=" * 80)
    print("Algorithm Comparison Summary")
    print("=" * 80)

    headers = ["Algorithm", "Avg_TAT", "Avg_WT", "Avg_RT", "Context_Switches"]
    rows = []
    for algo in ALGO_ORDER:
        label = f"RR(q={rr_q})" if algo == "RR" else algo
        s = summary[algo]
        rows.append([label, f"{s['avg_turnaround']:.3f}", f"{s['avg_waiting']:.3f}", f"{s['avg_response']:.3f}", f"{int(s['context_switches'])}"])

    colw = [max(len(headers[i]), max(len(r[i]) for r in rows)) for i in range(len(headers))]
    print("  ".join(headers[i].ljust(colw[i]) for i in range(len(headers))))
    print("  ".join("-" * colw[i] for i in range(len(headers))))
    for r in rows:
        print("  ".join(r[i].ljust(colw[i]) for i in range(len(headers))))

def make_graphs(summary: Dict[str, Dict[str, float]], rr_q: int) -> None:
    ensure_dirs()
    labels = []
    waiting = []
    turnaround = []
    for algo in ALGO_ORDER:
        labels.append(f"RR(q={rr_q})" if algo == "RR" else algo)
        waiting.append(summary[algo]["avg_waiting"])
        turnaround.append(summary[algo]["avg_turnaround"])

    plt.figure()
    plt.bar(labels, waiting)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Waiting Time")
    plt.title("Average Waiting Time vs. Algorithm")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(Path("graphs") / "waiting.png")
    plt.close()

    plt.figure()
    plt.bar(labels, turnaround)
    plt.xlabel("Algorithm")
    plt.ylabel("Average Turnaround Time")
    plt.title("Average Turnaround Time vs. Algorithm")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(Path("graphs") / "turnaround.png")
    plt.close()

    print("\nGraphs saved to:")
    print("  graphs/waiting.png")
    print("  graphs/turnaround.png")

def validate_args(args: argparse.Namespace) -> None:
    algo = args.algo.upper()
    valid = list(ALGO_MAP.keys()) + ["ALL"]
    if algo not in valid:
        raise SystemExit(f"Invalid --algo '{args.algo}'. Choose: {', '.join(valid)}")
    if algo == "RR" and args.quantum is None:
        raise SystemExit("--quantum is required when --algo RR")
    if args.quantum is not None and args.quantum <= 0:
        raise SystemExit("--quantum must be a positive integer")

def main() -> None:
    parser = argparse.ArgumentParser(description="CPU Process Scheduling Simulator (CENG 301)")
    parser.add_argument("--input", required=True, help="Path to processes.txt")
    parser.add_argument("--algo", required=True, help="FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P, or ALL")
    parser.add_argument("--quantum", type=int, default=None, help="Time quantum for RR (required for RR; optional for ALL)")
    args = parser.parse_args()
    validate_args(args)

    procs = parse_processes(args.input)
    algo = args.algo.upper()
    rr_q = args.quantum if args.quantum is not None else 4

    if algo != "ALL":
        if algo == "RR":
            result = ALGO_MAP[algo](procs, rr_q)
            print_run_report(f"RR(q={rr_q})", result)
        else:
            result = ALGO_MAP[algo](procs, rr_q)
            print_run_report(algo, result)
        return

    summary: Dict[str, Dict[str, float]] = {}
    for a in ALGO_ORDER:
        if a == "RR":
            result = ALGO_MAP[a](procs, rr_q)
            summary[a] = print_run_report(f"RR(q={rr_q})", result)
        else:
            result = ALGO_MAP[a](procs, rr_q)
            summary[a] = print_run_report(a, result)

    print_comparison_table(summary, rr_q)
    make_graphs(summary, rr_q)

if __name__ == "__main__":
    main()

"""Statistics computation and formatted printing."""

from __future__ import annotations
from typing import Dict, List
from .common import pid_key
from .parser import Process


def compute_per_process(processes: List[Process]) -> List[Dict]:
    rows: List[Dict] = []
    for p in processes:
        if p.completion is None or p.first_start is None:
            raise ValueError(f"Process {p.pid} has incomplete simulation fields.")
        tat = p.completion - p.arrival
        wt = tat - p.burst
        rt = p.first_start - p.arrival
        rows.append(
            {
                "PID": p.pid,
                "Arr": p.arrival,
                "Burst": p.burst,
                "Prio": p.priority,
                "Compl": p.completion,
                "TAT": tat,
                "WT": wt,
                "RT": rt,
            }
        )
    rows.sort(key=lambda r: pid_key(r["PID"]))
    return rows


def compute_averages(rows: List[Dict]) -> Dict[str, float]:
    n = len(rows)
    return {
        "avg_turnaround": sum(r["TAT"] for r in rows) / n,
        "avg_waiting": sum(r["WT"] for r in rows) / n,
        "avg_response": sum(r["RT"] for r in rows) / n,
    }


def format_table(rows: List[Dict]) -> str:
    headers = ["PID", "Arr", "Burst", "Prio", "Compl", "TAT", "WT", "RT"]
    colw = {h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers}
    out = []
    out.append("  ".join(h.rjust(colw[h]) for h in headers))
    out.append("  ".join("-" * colw[h] for h in headers))
    for r in rows:
        out.append("  ".join(str(r[h]).rjust(colw[h]) for h in headers))
    return "\n".join(out)

"""ASCII Gantt chart and segment helpers.

Segment: (start, end, pid), where end is exclusive.
"""

from __future__ import annotations
from typing import List, Tuple

Segment = Tuple[int, int, str]


def add_segment(segments: List[Segment], start: int, end: int, pid: str) -> None:
    if start >= end:
        return
    if segments and segments[-1][2] == pid and segments[-1][1] == start:
        s0, _, p0 = segments[-1]
        segments[-1] = (s0, end, p0)
    else:
        segments.append((start, end, pid))


def print_ascii_gantt(segments: List[Segment]) -> None:
    if not segments:
        print("No execution segments.")
        return
    start = segments[0][0]
    end = segments[-1][1]
    print("Time : " + " ".join(str(t) for t in range(start, end + 1)))
    cells: List[str] = []
    for s, e, pid in segments:
        for _ in range(s, e):
            cells.append(pid)
    print("CPU  : |" + "|".join(cells) + "|")
    print("Segments:", ", ".join([f"{pid}[{s},{e})" for s, e, pid in segments]))

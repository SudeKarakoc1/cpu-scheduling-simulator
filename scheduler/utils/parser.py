"""Input parser for processes.txt.

Format: pid arrival_time burst_time priority
- Lines starting with # are ignored.
- Fields separated by whitespace.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int
    remaining: int
    first_start: Optional[int] = None
    completion: Optional[int] = None


def parse_processes(path: str) -> List[Process]:
    processes: List[Process] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 4:
                raise ValueError(f"Invalid line (expected 4 fields): {raw!r}")
            pid, a, b, pr = parts
            arrival = int(a)
            burst = int(b)
            priority = int(pr)
            if arrival < 0 or burst <= 0:
                raise ValueError(f"arrival must be >=0 and burst must be >0: {raw!r}")
            processes.append(Process(pid, arrival, burst, priority, remaining=burst))
    return processes

"""Common helpers shared across the scheduler project.

Tie-breaking:
- Deterministic ties by PID order (numeric suffix if present, else lexicographic).

Priority convention:
- Smaller integer value => higher priority.

Context switch counting:
- Count when CPU changes from one process to another (PID changes),
  excluding IDLE transitions and excluding initial dispatch.
"""

from __future__ import annotations
from typing import Tuple, Optional


def pid_key(pid: str) -> Tuple[int, str]:
    digits = "".join(ch for ch in pid if ch.isdigit())
    if digits:
        return (int(digits), pid)
    return (10**9, pid)


def is_idle(pid: Optional[str]) -> bool:
    return pid is None or pid == "IDLE"


def count_context_switch(prev_pid: Optional[str], next_pid: Optional[str]) -> int:
    if prev_pid is None:
        return 0
    if is_idle(prev_pid) or is_idle(next_pid):
        return 0
    return 1 if prev_pid != next_pid else 0

"""SJF (Shortest Job First) - non-preemptive."""

from __future__ import annotations
from typing import Dict, List, Optional
from copy import deepcopy

from ..utils.common import pid_key, count_context_switch
from ..utils.gantt import add_segment
from ..utils.parser import Process


def run(processes: List[Process]) -> Dict:
    procs = deepcopy(processes)
    procs.sort(key=lambda p: (p.arrival, pid_key(p.pid)))

    t = 0
    i = 0
    n = len(procs)

    ready: List[Process] = []
    segments = []
    log: List[str] = []
    context = 0
    current: Optional[str] = None

    def arrivals(upto: int) -> None:
        nonlocal i
        while i < n and procs[i].arrival <= upto:
            log.append(f"t={procs[i].arrival}: {procs[i].pid} arrives")
            ready.append(procs[i])
            i += 1

    while i < n or ready:
        arrivals(t)

        if not ready:
            next_t = procs[i].arrival
            add_segment(segments, t, next_t, "IDLE")
            t = next_t
            continue

        ready.sort(key=lambda p: (p.burst, p.arrival, pid_key(p.pid)))
        p = ready.pop(0)

        context += count_context_switch(current, p.pid)
        current = p.pid

        if p.first_start is None:
            p.first_start = t

        log.append(f"t={t}: {p.pid} starts running (SJF)")

        start = t
        t += p.remaining
        p.remaining = 0
        p.completion = t
        add_segment(segments, start, t, p.pid)

        log.append(f"t={t}: {p.pid} completes")

        arrivals(t)

    procs.sort(key=lambda p: pid_key(p.pid))
    return {"segments": segments, "log": log, "processes": procs, "context_switches": context}

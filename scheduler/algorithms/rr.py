"""Round Robin (RR) with quantum q."""

from __future__ import annotations
from typing import Dict, List, Optional
from copy import deepcopy
from collections import deque

from ..utils.common import pid_key, count_context_switch
from ..utils.gantt import add_segment
from ..utils.parser import Process


def run(processes: List[Process], quantum: int) -> Dict:
    if quantum <= 0:
        raise ValueError("Quantum must be positive.")

    procs = deepcopy(processes)
    procs.sort(key=lambda p: (p.arrival, pid_key(p.pid)))
    n = len(procs)

    t = 0
    i = 0
    ready = deque()

    segments = []
    log: List[str] = []

    context = 0
    current: Optional[str] = None

    def add_arrivals_up_to(time_inclusive: int) -> None:
        nonlocal i
        while i < n and procs[i].arrival <= time_inclusive:
            log.append(f"t={procs[i].arrival}: {procs[i].pid} arrives")
            ready.append(procs[i])
            i += 1

    if n > 0 and procs[0].arrival > 0:
        add_segment(segments, 0, procs[0].arrival, "IDLE")
        t = procs[0].arrival

    add_arrivals_up_to(t)

    while ready or i < n:
        if not ready:
            next_t = procs[i].arrival
            add_segment(segments, t, next_t, "IDLE")
            t = next_t
            add_arrivals_up_to(t)
            continue

        p = ready.popleft()

        context += count_context_switch(current, p.pid)
        current = p.pid

        if p.first_start is None:
            p.first_start = t

        log.append(f"t={t}: {p.pid} starts/resumes running (RR, q={quantum})")

        run_time = min(quantum, p.remaining)
        add_segment(segments, t, t + run_time, p.pid)
        t += run_time
        p.remaining -= run_time

        add_arrivals_up_to(t)

        if p.remaining == 0:
            p.completion = t
            log.append(f"t={t}: {p.pid} completes")
        else:
            log.append(f"t={t}: quantum expired for {p.pid}, re-queued (remaining={p.remaining})")
            ready.append(p)

    procs.sort(key=lambda p: pid_key(p.pid))
    return {"segments": segments, "log": log, "processes": procs, "context_switches": context}

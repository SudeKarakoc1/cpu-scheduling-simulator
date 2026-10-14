"""SRTF (Shortest Remaining Time First) - preemptive tick simulation."""

from __future__ import annotations
from typing import Dict, List, Optional
from copy import deepcopy

from ..utils.common import pid_key, count_context_switch
from ..utils.gantt import add_segment
from ..utils.parser import Process


def run(processes: List[Process]) -> Dict:
    procs = deepcopy(processes)
    procs.sort(key=lambda p: (p.arrival, pid_key(p.pid)))
    n = len(procs)

    t = 0
    i = 0
    ready: List[Process] = []
    segments = []
    log: List[str] = []

    context = 0
    current: Optional[str] = None
    running: Optional[Process] = None
    completed = 0

    def push_arrivals(time: int) -> None:
        nonlocal i
        while i < n and procs[i].arrival == time:
            log.append(f"t={time}: {procs[i].pid} arrives")
            ready.append(procs[i])
            i += 1

    if n > 0 and procs[0].arrival > 0:
        add_segment(segments, 0, procs[0].arrival, "IDLE")
        t = procs[0].arrival

    while completed < n:
        if running is None and not ready and i < n and procs[i].arrival > t:
            add_segment(segments, t, procs[i].arrival, "IDLE")
            t = procs[i].arrival

        push_arrivals(t)

        candidates = ready[:]
        if running is not None:
            candidates.append(running)

        if not candidates:
            t += 1
            continue

        candidates.sort(key=lambda p: (p.remaining, p.arrival, pid_key(p.pid)))
        chosen = candidates[0]

        if running is None:
            context += count_context_switch(current, chosen.pid)
            current = chosen.pid
            if chosen.first_start is None:
                chosen.first_start = t
            log.append(f"t={t}: {chosen.pid} starts running (SRTF)")
        elif chosen.pid != running.pid:
            context += count_context_switch(current, chosen.pid)
            log.append(f"t={t}: {chosen.pid} starts running (preempts {running.pid})")
            current = chosen.pid
            if chosen.first_start is None:
                chosen.first_start = t
            ready.append(running)

        if chosen in ready:
            ready.remove(chosen)
        running = chosen

        add_segment(segments, t, t + 1, running.pid)
        running.remaining -= 1
        t += 1

        if running.remaining == 0:
            running.completion = t
            log.append(f"t={t}: {running.pid} completes")
            completed += 1
            running = None

    procs.sort(key=lambda p: pid_key(p.pid))
    return {"segments": segments, "log": log, "processes": procs, "context_switches": context}

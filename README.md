# Process Scheduling Simulator (Python)

## 1. Project Information
- Project: CPU Process Scheduling Simulator
- Name: Rabia Sude KARAKOÇ

## 2. Environment and Dependencies
- Programming Language: Python 3
- Tested Python Version: Python 3.10+
- Compatibility: Python 3.10+
- External Libraries:
  - matplotlib (used for generating comparison graphs)

Installation of required library:
```bash
pip install matplotlib
```

## 3. Project Structure
```text
cpu-scheduling-simulator/
├── scheduler.py
├── processes.txt
├── README.md
├── scheduler/
│   ├── algorithms/
│   │   ├── fcfs.py
│   │   ├── sjf.py
│   │   ├── srtf.py
│   │   ├── rr.py
│   │   ├── priority_np.py
│   │   └── priority_p.py
│   └── utils/
│       ├── parser.py
│       ├── gantt.py
│       ├── statistics.py
│       └── common.py
├── logs/
└── graphs/
```

## 4. How to Run the Simulator
 - Run all algorithms and generate comparison graphs:
 ```bash
 python scheduler.py --input processes.txt --algo ALL --quantum 4
 ```

 - Run a single algorithm (example: Round Robin):
 ```bash
 python scheduler.py --input processes.txt --algo RR --quantum 4
 ```

## 5. Implemented Scheduling Algorithms
 - FCFS (First-Come First-Served)

A non-preemptive scheduling algorithm where processes are executed in the order of their arrival times.

 - SJF (Shortest Job First – Non-preemptive)

Selects the process with the shortest CPU burst time among the ready processes. This algorithm minimizes average waiting time but may cause starvation.

 - SRTF (Shortest Remaining Time First – Preemptive)

A preemptive version of SJF. At every time unit, the process with the smallest remaining execution time is selected, allowing frequent preemptions.

 - Round Robin (RR)

A preemptive scheduling algorithm where each process is assigned a fixed time quantum. This approach improves fairness and response time for interactive systems.

 - Priority Scheduling (Non-preemptive)

Processes are scheduled based on priority values. Lower numerical values represent higher priorities.

 - Priority Scheduling (Preemptive)

A preemptive variant where the currently running process may be preempted if a higher-priority process arrives.

## 6. Experimental Results and Discussion

Based on the experimental results obtained from the given input workload:

 - SRTF achieved the lowest average waiting and turnaround times, as it always prioritizes the process with the shortest remaining execution time.

 - Round Robin provided better response times but resulted in a higher number of context switches due to frequent preemptions.

 - FCFS performed worst in terms of average waiting time, especially when long processes arrived early.

 - Priority-based algorithms showed expected behavior but may suffer from starvation for low-priority processes.

Overall, the results align with theoretical expectations discussed in operating systems literature.

## 7. Output Files
- `logs/`: execution logs for each scheduling algorithm
- `graphs/waiting.png`: Average Waiting Time vs Algorithm
- `graphs/turnaround.png`: Average Turnaround Time vs Algorithm

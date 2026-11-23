#!/usr/bin/env bash
# List (read-only) the night queue's processes: PID, PPID, command.
ps -eo pid,ppid,etimes,args | grep -E 'night_queue|night_nx|bth.benchrun|stall_watch_wsl2|gate_alarm|_worker' | grep -v -E 'grep|night_pids'

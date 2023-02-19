import re
import sys
import subprocess

N_STEP_MAX = 2

WALLEE_NAMES = [
    "robot", "runbot", "wall-e", "wall e", "wally", "wallee", "walee", "well-e",
    "wolly", "wolee", "wole-e", "wal-hee", "roll e", "vol-e", "volee", "volky",
    "wargill", "woggy", "vul-e", "mulkey", "well, e", "walghee", "vaul t",
    "volity", "valee", "while e", "ball-he", "wall key", "wal-i", "mulhee",
    "wole", "wallie", "woly", "all e", "wali", "well-eat", "wollief", "molly",
    "borry"
    ]


n = 0
lines = []
for line in sys.stdin:
    lines.append(line.rstrip()[:40])
    sys.stderr.write(line + '\n')
        
    # Join last four lines.
    l = len(lines)
    joined = ""
    for i in range(max(0, l - 4), l):
        joined = joined + " " + lines[i]
    joined = joined.lstrip()

    found = False
    for name in WALLEE_NAMES:
        if joined.lower().find(name) > -1:
            found = True
            break
    if found:
        print(joined)

    n += 1
    if n >= N_STEP_MAX:
        exit(0)

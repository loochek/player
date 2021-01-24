#!/usr/bin/python3

# Roll keypresser for Windows and Linux

import time, sys, os
from common import EVENT_SLEEP, EVENT_KEY_PRESS, EVENT_KEY_RELEASE

if os.name == 'posix':
    from keypresser_linux import type_letter
if os.name == 'nt':
    from keypresser_windows import type_letter

def play(roll_file_name):
    roll_file = open(roll_file_name, "r")

    roll = []

    for event in roll_file:
        event = event.split()
        event_type = int(event[0])
        event_arg  = event[1]
        if event_type == EVENT_SLEEP:
            roll.append([EVENT_SLEEP, float(event_arg)])
        elif event_type == EVENT_KEY_PRESS:
            roll.append([EVENT_KEY_PRESS, event_arg])
        elif event_type == EVENT_KEY_RELEASE:
            roll.append([EVENT_KEY_RELEASE, event_arg])

    roll_file.close()

    print("Now focus on virtualpiano.net!")
    time.sleep(5)

    for event_type, event_arg in roll:
        if event_type == EVENT_SLEEP:
            time.sleep(event_arg)
        elif event_type == EVENT_KEY_PRESS:
            print(event_arg)
            for c in event_arg:
                type_letter(c)


def main():
    if len(sys.argv) == 1:
        print("Usage: player.py <roll file name>")
        return
    
    roll_file_name = sys.argv[1]

    play(roll_file_name)

main()
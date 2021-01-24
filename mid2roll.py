#!/usr/bin/python3

# This script translates MIDI piano file to key press roll for virtualpiano.net

import mido, json, sys
from common import EVENT_SLEEP, EVENT_KEY_PRESS, EVENT_KEY_RELEASE

# not my code, i couldn't remember where i took this
# but it translates MIDI note number to virtualpiano.net keys
# i'm not musician, so it's black box for me :(

VIRTUAL_PIANO_SCALE = "1!2@34$5%6^78*9(0qQwWeErtTyYuiIoOpPasSdDfgGhHjJklLzZxcCvVbBnm"

def note_to_key(midi_note):
    
    kk = midi_note - 23 - 12 - 1
    while (kk >= len(VIRTUAL_PIANO_SCALE)):
        kk -= 12
    while (kk < 0):
        kk += 12
    return VIRTUAL_PIANO_SCALE[kk]

# end of borrowed code <3

def mid2roll(midi_file_name, roll_file_name):
    roll = []

    midi_file = mido.MidiFile(midi_file_name)

    keys_to_press   = ""
    keys_to_release = ""

    for msg in midi_file:
        # flush key buffers if time delta from last message is present, then sleep this time delta
        if msg.time != 0:
            if len(keys_to_release) != 0:
                roll.append([EVENT_KEY_RELEASE, keys_to_release])
                keys_to_release = ""

            if len(keys_to_press) != 0:
                roll.append([EVENT_KEY_PRESS, keys_to_press])
                keys_to_press = ""

            roll.append([EVENT_SLEEP, msg.time])

        # note that NOTE_ON with zero velocity is equal to NOTE_OFF

        if msg.type == 'note_on' and msg.velocity != 0:
            keys_to_press += note_to_key(msg.note)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            keys_to_release += note_to_key(msg.note)

    # flush last unflushed message

    if len(keys_to_release) != 0:
        roll.append([EVENT_KEY_RELEASE, keys_to_release])
        keys_to_release = ""

    if len(keys_to_press) != 0:
        roll.append([EVENT_KEY_PRESS, keys_to_press])
        keys_to_press = ""

    # write roll to the file

    roll_file = open(roll_file_name, "w")
    
    for event_type, arg in roll:
        print(event_type, arg, file=roll_file)

    roll_file.close()

def main():
    if len(sys.argv) == 1:
        print("Usage: mid2roll.py <midi file name> [<output file name>]")
        return
    
    midi_file_name = sys.argv[1]
    roll_file_name = midi_file_name + ".roll"

    if len(sys.argv) >= 3:
        roll_file_name = sys.argv[2]

    mid2roll(midi_file_name, roll_file_name)

main()
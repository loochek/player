import csv, sys, json, time

magic = -1
tempo = 120

def calculateTime(time):
    return time * (tempo / magic / 1000000)

def comp(a):
    return int(a[1].strip())

def midi2key(kk):
    kk = kk - 21
    while (kk >= len(virtualPianoScale)):
        kk -= 12
    return kk
	
virtualPianoScale = "1!2@34$5%6^78*9(0qQwWeErtTyYuiIoOpPasSdDfgGhHjJklLzZxcCvVbBnm"

if len(sys.argv) < 3:
    print("Usage: py prg.py <csv file> <output file>")
else:
    with open(sys.argv[1], "r") as f_obj:
        csvFile = csv.reader(f_obj)
        events = []
        for row in csvFile:
            events.append(row)
        events.sort(key=comp)
        timeline = []
        lastTime = 0
        pressBuffer = ""
        releaseBuffer = ""
        for row in events:
            if int(row[1].strip()) != lastTime:
                timeline.append((1, releaseBuffer))
                timeline.append((2, pressBuffer))
                pressBuffer = ""
                releaseBuffer = ""
                timeline.append((0, calculateTime(int(row[1].strip()) - lastTime)))
                lastTime = int(row[1].strip())
            if 'Note_on_c' in row[2].strip():
                if int(row[5].strip()) == 0:
                    releaseBuffer += virtualPianoScale[midi2key(int(row[4].strip()))]
                else:
                    pressBuffer += virtualPianoScale[midi2key(int(row[4].strip()))]
            elif 'Note_off_c' in row[2].strip():
                releaseBuffer += virtualPianoScale[midi2key(int(row[4].strip()))]
            elif 'Header' in row[2].strip():
                magic = int(row[5].strip())
            elif 'Tempo' in row[2].strip():
                tempo = int(row[3].strip())
        f = open(sys.argv[2], 'w')
        f.write(json.dumps(timeline, indent=4))
        f.close()

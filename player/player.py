import time, json, sys, keypresser, os

print("""
    Usage:
    1. Go to virtualpiano.net
    2. Select file to play
    3. Set focus to the browser window. You have 4 seconds
    3. Listen
    Note: In shitty Google Chrome Browser sound may be bad, use godlike Firefox
    """)
files = os.listdir()
print("Choose file:")
c = 1
jfiles = []
for i in files:
    if i.split('.')[-1] == "json":
        jfiles.append(i)
        print(str(c) + ". " + i)
        c += 1
sel = int(input("Your choice:"))
f = open(jfiles[sel - 1], 'r')
timeline = json.loads(f.read())
time.sleep(4)
for i in timeline:
    if i[0] == 0:
        time.sleep(float(i[1]))
    else:
        print(i[1])
        keypresser.typer(i[1])
time.sleep(1)
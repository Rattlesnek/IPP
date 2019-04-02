import sys

i = 0
for line in sys.stdin:
    if i == 0:
        print('.IFJcode18')
    else:
        print(line, end='')
    i += 1
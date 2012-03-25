# Modified after tips from
# http://codereview.stackexchange.com/a/10322/12097
# from Winston Ewert
import sys
import re
import math

SCRIPTTITLE="PYTHON SIMPLE PROCESSOR (regex parsing, optimization v1)"

linecount=0
commentary=0
unknownline=0
data={}

pattern_data=re.compile(r"^(\d+)\s+(\S+)\s+(\S+)\s+(\d+(?:\.\d+)?)")

print("#",SCRIPTTITLE,"\n#TRANSFORMED INPUT",sep='')

for line in sys.stdin:
    linecount += 1
    if line.startswith("#"):
        commentary += 1
        continue
    line = line.replace(',','')
    m = pattern_data.match(line)
    if m:
        i,k1,k2,value = m.groups()
        i=int(i)
        value=float(value)
        try:
            row = data[k1]
        except KeyError:
            row = data[k1] = {}
        try:
            row[k2] += value
        except KeyError:
            row[k2] = value
        sys.stdout.write("{0},{1:.0f},{2},{3}\n".format(i,value,k2,k1))
    else:
        unknownline+=1

print("#DATADUMP")

keystat=0

for k1, subkeys in sorted(data.items()):
    sys.stdout.write(k1+':')
    for k2,v in sorted(subkeys.items()):
        keystat+=1
        sys.stdout.write(' ({0}:{1:d})'.format(k2,math.trunc(v)))
    sys.stdout.write("\n")

report="#{0}\n#{1}\nparsed line: {2}, commentary line: {3}, unknown line: {4}, keystat: {5}.".format(
               SCRIPTTITLE, sys.version.replace("\n"," "), linecount, commentary, unknownline, keystat)

print("#REPORT\n"+report,file=sys.stdout)
print(report,file=sys.stderr)

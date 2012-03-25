import sys
import re

scripttitle="PYTHON SIMPLE PROCESSOR (regex parsing)"

linecount=0
commentary=0
unknownline=0
DATA={}

pattern_data=re.compile(r"^(\d+)\s+(\S+)\s+(\S+)\s+(\d+(?:\.\d+)?)")

print("#",scripttitle,"\n#TRANSFORMED INPUT",sep='')

for line in sys.stdin:
    linecount+=1
    if line.startswith("#"):
        commentary+=1
        continue
    line=line.replace(',','')
    m=re.match(pattern_data,line)
    if m:
        i,k1,k2,value = m.group(1,2,3,4)
        i=int(i)
        value=float(value)
        try:
            DATA[k1][k2]+=value
        except KeyError:
            if k1 not in DATA: # Can't automaticaly create missing key and do the insert?
                DATA[k1]={}
            if k2 not in DATA[k1]:
                DATA[k1][k2]=value
            else:
                DATA[k1][k2]+=value
        print("{0},{1:.0f},{2},{3}".format(i,value,k2,k1))
    else:
        unknownline+=1

print("#DATADUMP")

keystat=0

for k1 in sorted(DATA):
    print(k1,':',sep='',end='')
    for k2 in sorted(DATA[k1]):
        keystat+=1
        print(' (',k2,':',int(DATA[k1][k2]),')',sep='',end='')
    print()

report="#{0}\n#{1}\nparsed line: {2}, commentary line: {3}, unknown line: {4}, keystat: {5}.".format(
               scripttitle, sys.version.replace("\n"," "), linecount, commentary, unknownline, keystat)

print("#REPORT\n"+report,file=sys.stdout)
print(report,file=sys.stderr)

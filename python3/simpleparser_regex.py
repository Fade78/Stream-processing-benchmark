import sys
import re

scripttitle="PYTHON (Simple Parser Regex)"
linecount=0
commentary=0
unknownline=0

pattern_data=re.compile(r"^(\d+)\s+(\S+)\s+(\S+)\s+(\d+(?:\.\d+)?)")

for line in sys.stdin:
    linecount+=1
    if line.startswith("#"):
        commentary+=1
        continue
    #line=line.replace(',','')
    m=re.match(pattern_data,line)
    if m:
        print(*m.group(1,4,3,2),sep=',')
    else:
        unknownline+=1

report="#{0}\n#{1}\nparsed line: {2}, commentary line: {3}, unknown line: {4}.".format(
               scripttitle, sys.version.replace("\n"," "), linecount, commentary, unknownline)

print(report)



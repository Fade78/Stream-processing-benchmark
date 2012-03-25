import sys

scripttitle="PYTHON (Simple Parser String)"

linecount=0
commentary=0
unknownline=0

for line in sys.stdin:
    linecount+=1
    if line.startswith("#"):
        commentary+=1
        continue
    ts, server, counter, value=line.rstrip().replace(',','').split('\t')
    print(ts,value,counter,server,sep=',')

report="#{0}\n#{1}\nparsed line: {2}, commentary line: {3}, unknown line: {4}.".format(
               scripttitle, sys.version.replace("\n"," "), linecount, commentary, unknownline)

print(report)

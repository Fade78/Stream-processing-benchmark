# Modified after tips from
# http://codereview.stackexchange.com/a/10322/12097
# from Winston Ewert
import sys
import re
import math

SCRIPTTITLE="PYTHON SIMPLE PROCESSOR (regex parsing, optimization v2)"

def main():
    linecount=0
    commentary=0
    unknownline=0
    data={}

    write = sys.stdout.write

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
            value=float(value)
            try:
                row = data[k1]
            except KeyError:
                row = data[k1] = {}
            try:
                row[k2] += value
            except KeyError:
                row[k2] = value
            write(",".join([i, '{0:.0f}'.format(value), k2, k1])+"\n")
        else:
            unknownline+=1

    print("#DATADUMP")

    keystat=0

    for k1 in sorted(data):
        subkeys = data[k1]
        write(k1+':')
        keystat += len(subkeys)
        for k2 in sorted(subkeys):
            v = subkeys[k2]
            write(''.join([' (',k2,':',str(math.trunc(v)),')']))
        write("\n")

    report="#{0}\n#{1}\nparsed line: {2}, commentary line: {3}, unknown line: {4}, keystat: {5}.".format(
                   SCRIPTTITLE, sys.version.replace("\n"," "), linecount, commentary, unknownline, keystat)

    print("#REPORT\n"+report,file=sys.stdout)
    print(report,file=sys.stderr)

main()

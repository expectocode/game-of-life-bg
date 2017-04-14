#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
        description="Turn an RLE description of a GOL pattern into a series of coordinates. For some reason, sometimes the $ in input are lost. Try a different style of quotes.")
parser.add_argument(
            '-i', '--input-rle',
            help='The RLE string you want to decode.')

gli = parser.parse_args().input_rle

#tuplist = []
#for yindex,line in enumerate(gli.split("$")):
#    lastmult=-100
#    for index,x in enumerate(line):
#        if x.isdigit() and not line[index+1].isdigit():
#            if lastmult == index: #this is 2nd digit
#                print(int(line[index-2:index])*line[index+1],end='')
#                tuplist.extend([(index+th,yindex) for th in range(int(x))])
#            else:
#                lastmult = index
#                print(int(x)*line[index+1],end='')
#                tuplist.extend([(index+th,yindex) for th in range(int(x))])
#        elif x.isdigit() and line[index+1].isdigit():
#            lastmult = index + 1
#            continue
#        elif index - lastmult != 1:
#            if x == 'o':
#                print(x,end='')
#                tuplist.append((index,yindex))
#            else:
#                print(" ",end='')
#
#    print("")
#
#print(tuplist)
def run_length_decode(rle):

    ''' Expand the series of run-length encoded characters.

'''

    run = ''

    for c in rle:

        if c in '0123456789':

            run += c

        else:

            run = int(run or 1) # if the run isn't explicitly coded, it has length 1

            v = c if c in 'bo$' else 'b' # treat unexpected cells as dead ('b')

            for _ in range(run):

                yield v

            run = ''

instr = gli
outstr= ""
tups = []
for x in run_length_decode(instr):
    outstr += x

print(outstr.split("$"))

for yind,line in enumerate(outstr.split("$")):
    for xind,c in enumerate(line):
        if 'o' == c:
            print("#",end='')
            tups.append((xind,yind))
        else:
            print(" ",end='')
    print("")

print(tups)

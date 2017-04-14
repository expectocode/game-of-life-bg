#!/usr/bin/env python3
str = """.OO
.OO.................O
...................O.O............O.O
....................O............O
OO.......OO.......................O..O
OO.O.....OO.......................O.O.O
...O.......................O.......O..O
...O.......................OO.......OO
O..O.................OO.....O
.OO..................O
.....................OOO
....................................OO
....................................OO
.OO
O..O
O.O.O................O.O....OO.....OO
.O..O.................OO....OO.....OO.O
.....O............O...O...............O
..O.O............O.O..................O
..................O................O..O
....................................OO"""
#this program is not meant to be used seriously. just edit the above string when you need to use it.
tups = []
for yindex,line in enumerate(str.split("\n")):
    for xindex,char in enumerate(line):
        if("o" == char.lower()):
            tups.append((xindex,yindex))

print(sorted(tups))

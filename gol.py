#!/usr/bin/env python3
#inspired by https://f.0x52.eu/blog/game_of_life
from collections import Counter
from PIL import Image,ImageDraw
from time import sleep
import subprocess as sub
from math import sin,cos,radians
import patterns as p #my patterns file

width = round(1366/8)
height = round(768/8)

#if the y coord of a live cell is 0, 3 neighbours have y coord (height - 1)
#-1%50 = 49

def getneighbours(coords):
    return [((coords[0])%width,(coords[1]+1)%height),
            ((coords[0])%width,(coords[1]-1)%height),
            ((coords[0]+1)%width,(coords[1]+1)%height),
            ((coords[0]+1)%width,(coords[1])%height),
            ((coords[0]+1)%width,(coords[1]-1)%height),
            ((coords[0]-1)%width,(coords[1]+1)%height),
            ((coords[0]-1)%width,(coords[1])%height),
            ((coords[0]-1)%width,(coords[1]-1)%height)]

#translate coords
def trans(coordlist,x,y):
    return [((tup[0]+x)%width,(tup[1]+y)%height) for tup in coordlist]

def y_flip(coordlist):
    return [(tup[0],tup[1]*-1) for tup in coordlist]

def x_flip(coordlist):
    return [(tup[0]*-1,tup[1]) for tup in coordlist]

def rotate2d(degrees,point,origin):
    """
    A rotation function that rotates a point around a point
    to rotate around the origin use (0,0)
    https://ubuntuforums.org/showthread.php?t=975315
    """
    x = point[0] - origin[0]
    yorz  = point[1] - origin[1]
    newx = (x*cos(radians(degrees))) - (yorz*sin(radians(degrees)))
    newyorz  = (x*sin(radians(degrees))) + (yorz*cos(radians(degrees)))
    newx += origin[0]
    newyorz  += origin[1]
    return (round(newx),round(newyorz))

def rotate(coordlist,degrees):
    centercoord = (round(sum([tup[0] for tup in coordlist])/len(coordlist)),
        round(sum([tup[1] for tup in coordlist])/len(coordlist)))
    return [rotate2d(degrees,coord,centercoord) for coord in coordlist]

DEAD = (44, 62, 80) #RGB
ALIVE = (224, 224, 224) #RGB

def main():
    #gen1_alivecells = trans(p.copperhead,85-6,48-4,)
    #gun,middle
    #gen1_alivecells = trans(p.gospergun,round(width/2)-17,round(height/2)-4)
    #gun
    #gen1_alivecells = trans(p.gospergun,3,3)
    #race
    #gen1_alivecells = rotate(trans(p.weekender,round(width/2)-9,60),90) + trans(x_flip(p.lwss),round(width/2)-2,40) + trans(p.copperhead,round(width/2)-6,20)
    #gen1_alivecells = rotate(trans(p.weekender,round(width/2)-9,52),90) + trans(x_flip(p.lwss),round(width/2)-2,32)
    gen1_alivecells = trans(x_flip(p.lwss),round(width/2)-2,round(height/2)-2-20) + trans(p.copperhead,round(width/2)-6,round(width/2)-4-30)
    #gen1_alivecells = trans(p.shick,round(width/2)-10,round(height/2)-4)
    #gen1_alivecells = rotate(trans(b52,round(width/2)-20,round(height/2)-10),90)
    #gen1_alivecells = trans(p.blinkership1,round(width/2)-11,round(height/2)-6)
    #glider formation
    #gen1_alivecells = []
    #for x in range(5):
    #    for y in range(5):
    #        gen1_alivecells.extend(trans(p.glider,62+9*x,32+6*y))

    #main loop
    while True:
        im = Image.new('RGB', (width,height),color=DEAD)
        gen1_neighbours_list = []
        gen2_alivecells = []
        for cell in gen1_alivecells:
            gen1_neighbours_list.extend(getneighbours(cell))
        gen1_neighbours_dict = Counter(gen1_neighbours_list)
        for key,value in gen1_neighbours_dict.items():
            if key in gen1_alivecells and (3 == value or 2 == value):
                #print(key,value)
                gen2_alivecells.append(key)
            elif key not in gen1_alivecells and 3 == value:
                #print(key,value)
                gen2_alivecells.append(key)
        gen1_alivecells = gen2_alivecells
        draw = ImageDraw.Draw(im)
        draw.point(gen1_alivecells,fill=ALIVE)
        del draw
        #print(gen1_alivecells)

        scale_factor = 8
        im2 = im.resize((im.width * scale_factor, im.height * scale_factor))
        #save to /tmp because this is in RAM not on disk
        #alternative is to use a program that supports reading from stdin
        #feh has this but @uncleleech says this saves to disk at some point
        #there's also https://linux.die.net/man/1/xloadimage
        #but i trust /tmp the most to actually do what i want it to
        im2.save('/tmp/gol.png')
        sleep(1)
        sub.run(['feh', '--bg-fill', '/tmp/gol.png'],stdout=sub.PIPE,stderr=sub.PIPE)

if __name__ == "__main__":
    main()

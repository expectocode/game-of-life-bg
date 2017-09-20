#!/usr/bin/env python3
#inspired by https://f.0x52.eu/blog/game_of_life
from PIL import Image,ImageDraw
import patterns as p #my patterns file
import subprocess as sub
from math import sin,cos,radians
from time import sleep
from collections import Counter

# These numbers essentially control cell size
# Use a multiple of your aspect ratio for square cells
width = round(16 * 11)
height = round(9 * 11)

# Set your dead and alive cell colours. (R,G,B)

DEAD = (44, 62, 80)
ALIVE = (224, 224, 224)

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

def is_x_running():
    p = sub.Popen(["xset", "-q"], stdout=sub.PIPE, stderr=sub.PIPE)
    p.communicate()
    return p.returncode == 0
    # Honestly not sure if this works, created it because
    # the script didn't die when X did.

def main():
    # Try these starting cells if you're stuck for inspiration
    # gen1_alivecells = trans(p.copperhead,85-6,48-4,)
    # gen1_alivecells = trans(p.gospergun,round(width/2)-17,round(height/2)-4)
    # gen1_alivecells = rotate(trans(p.weekender,round(width/2)-9,52),90) + trans(x_flip(p.lwss),round(width/2)-2,32)
    # gen1_alivecells = trans(x_flip(p.lwss),round(width/2)-2,round(height/2)-2-20) + trans(p.copperhead,round(width/2)-6,round(width/2)-4-30)
    # gen1_alivecells = trans(p.shick,round(width/2)-10,round(height/2)-4)
    # gen1_alivecells = rotate(trans(b52,round(width/2)-20,round(height/2)-10),90)
    # gen1_alivecells = trans(p.blinkership1,round(width/2)-11,round(height/2)-6)
    # glider formation
    gen1_alivecells = []
    for x in range(3):
       for y in range(3):
           gen1_alivecells.extend(trans(p.glider,62+7*x,32+6*y))

    #main loop
    while True:
        if not is_x_running():
            exit();
        im = Image.new('RGB', (width,height),color=DEAD)
        gen1_neighbours_list = []
        gen2_alivecells = []
        for cell in gen1_alivecells:
            gen1_neighbours_list.extend(getneighbours(cell))
        gen1_neighbours_dict = Counter(gen1_neighbours_list)
        for key,value in gen1_neighbours_dict.items():
            if key in gen1_alivecells and (3 == value or 2 == value):
                gen2_alivecells.append(key)
            elif key not in gen1_alivecells and 3 == value:
                gen2_alivecells.append(key)
        gen1_alivecells = gen2_alivecells
        draw = ImageDraw.Draw(im)
        draw.point(gen1_alivecells,fill=ALIVE)
        del draw # Is this needed?

        #save to /tmp because this is in RAM not on disk
        #alternative is to use a program that supports reading from stdin
        #feh has this but @uncleleech says this saves to disk at some point
        #there's also https://linux.die.net/man/1/xloadimage
        #but i trust /tmp the most to actually do what i want it to
        im.save('/tmp/gol.png')
        sub.run(['feh', '--bg-scale', '--no-fehbg','--force-aliasing','/tmp/gol.png'],
                stdout=sub.PIPE,stderr=sub.PIPE)
        # Using --force-aliasing means we don't scale the image ourselves,
        # since feh is probably better for that.
        sleep(1)

if __name__ == "__main__":
    main()

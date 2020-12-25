#!/usr/bin/env python3

import cairo
from math import pi, sin, cos, tan

#####################################################################
############################################################## inputs

filename = 'circle2bezier.pdf'
d = 100.0
n = 4

#####################################################################
############################################################# helpers

def circ2bezier (x, y, r, n, a0=0, a1=2*pi):
    if a0==a1: return []
    
    l = []
    astep = (a1 - a0)/n
    step = r*4.0/3*tan(pi/(2*n)/(2*pi)*(a1-a0))
    
    for i in range(n):
        ai = a0 + i*astep
        ao = ai + astep
        
        p0 = (x+r*cos(ai), y+r*sin(ai))
        p3 = (x+r*cos(ao), y+r*sin(ao))
        p1 = (p0[0] - step*sin(ai), p0[1] + step*cos(ai))
        p2 = (p3[0] + step*sin(ao), p3[1] - step*cos(ao))
        
        l.append([p0, p1, p2, p3])
    
    return l

#####################################################################
################################################################ main

# calculations
r = d/2
height = d*1.2
width = height/9*16
cx = width/2
cy = height/2
#beziers = circ2bezier(cx, cy, r, n)
#beziers = circ2bezier(cx, cy, r, n, pi/3, 1.5*pi)
#beziers = circ2bezier(cx, cy, r, n, pi/3)
#beziers = circ2bezier(cx, cy, r, n, 1.5*pi, pi/3)
beziers = circ2bezier(cx, cy, r, n, pi/3, -.5*pi)

# canvas
surface = cairo.PDFSurface(filename, width*2, height*2)
ctx = cairo.Context(surface)

# draw circle
ctx.save()
ctx.arc(cx, cy, r, 0, 2*pi)
ctx.stroke()
ctx.restore()

# draw control points
for bezier in beziers:
    for point in bezier:
        ctx.save()
        ctx.arc(point[0], point[1], 2, 0, 2*pi)
        ctx.set_source_rgb(0, 1, 0)
        ctx.fill()
        ctx.restore()

# draw beziers
ctx.save()
origin = beziers[0][0]
ctx.move_to(origin[0], origin[1])
for bezier in beziers:
    p1 = bezier[1]
    p2 = bezier[2]
    p3 = bezier[3]
    ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
ctx.set_line_width(1)
ctx.set_source_rgb(1, 0, 0)
ctx.stroke()
ctx.restore()


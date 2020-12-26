#!/usr/bin/env python3

import bezier.curve as bcurve
import cairo
from math import pi
import numpy as np

#####################################################################
############################################################## inputs

filename = 'intersections.pdf'
width = 1920
height = width*9/16
b = 100 # border
config = (3,2)
w = width /config[0]-2*b
h = height/config[1]-2*b

data = [
    {
        'offset': (0,0),
        'c1': [(b,b+h/2), (b+b,b), (w,b+h), (b+w,b+h/2)],
        'c2': [(b,b), (b+w/2,b), (b+w/2,b+h), (b+w,b+h)],
    },
    {
        'offset': (1,0),
        'c1': [(b,b+h/2), (b+b,b), (w,b+h), (b+w,b+h/2)],
        'c2': [(b,b+h), (b+w,b), (b,b), (b+w,b+h)],
    },
    {
        'offset': (2,0),
        'c1': [(b,b+h/2), (b+b,b), (w,b+h), (b+w,b+h/2)],
        'c2': [(b,b+h), (b+w+w,b), (b-w,b), (b+w,b+h)],
    },
    {
        'offset': (0,1),
        'c1': [(b,h/2+b), (b+w,b), (b+w,b+h), (b,h/2-b)],
        'c2': [(b,b), (b+w/2,b), (b+w/2,b+h), (b+w,b+h)],
    },
    {
        'offset': (1,1),
        'c1': [(b,h/2+b), (b+w,b), (b+w,b+h), (b,h/2-b)],
        'c2': [(b,b+h), (b+w,b), (b,b), (b+w,b+h)],
    },
    {
        'offset': (2,1),
        'c1': [(b,h/2+b), (b+w,b), (b+w,b+h), (b,h/2-b)],
        'c2': [(b,b+h), (b+w+w,b), (b-w,b), (b+w,b+h)],
    },
]

#####################################################################
############################################################# helpers

def draw_grid (ctx):
    # horizontal
    ctx.save()
    for i in range(1, config[0]):
        x = width*i/config[0]
        ctx.move_to(x, b)
        ctx.line_to(x, height-b)
    ctx.set_line_width(1)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()
    ctx.restore()
    
    # vertical
    ctx.save()
    for i in range(1, config[1]):
        y = height*i/config[1]
        ctx.move_to(b, y)
        ctx.line_to(width-b, y)
    ctx.set_line_width(1)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()
    ctx.restore()

def draw_control_points (ctx, bezier):
    for point in bezier:
        ctx.save()
        ctx.arc(point[0], point[1], 4, 0, 2*pi)
        ctx.set_source_rgb(0, 1, 0)
        ctx.fill()
        ctx.restore()

def draw_bezier (ctx, bezier):
    ctx.save()
    origin = bezier[0]
    ctx.move_to(origin[0], origin[1])
    p1 = bezier[1]
    p2 = bezier[2]
    p3 = bezier[3]
    ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
    ctx.set_line_width(2)
    ctx.set_source_rgb(1, 0, 0)
    ctx.stroke()
    ctx.restore()

def draw_intersections(ctx, points):
    for point in points:
        ctx.save()
        ctx.arc(point[0], point[1], 4, 0, 2*pi)
        ctx.set_source_rgb(0, 0, 1)
        ctx.fill()
        ctx.restore()

def to_np (c):
    nodes = np.asfortranarray([
        [c[0][0], c[1][0], c[2][0], c[3][0]],
        [c[0][1], c[1][1], c[2][1], c[3][1]]
    ])
    return nodes

def intersections (c1, c2):
    l = []
    
    b1 = bcurve.Curve(to_np(c1), 3)
    b2 = bcurve.Curve(to_np(c2), 3)
    
    i = b1.intersect(b2)
    for t in i[0]:
        p = b1.evaluate(t)
        l.append((p[0], p[1]))
    
    return l

#####################################################################
################################################################ main

# canvas
surface = cairo.PDFSurface(filename, width, height)
ctx = cairo.Context(surface)

draw_grid(ctx)

for i in range(len(data)):
    datum = data[i]
    offset = datum['offset']
    c1 = datum['c1']
    c2 = datum['c2']
    i = intersections(c1, c2)
    
    ctx.save()
    ctx.translate(width *(offset[0]%config[0])/config[0],
                  height*(offset[1]%config[1])/config[1])
    
    draw_control_points(ctx, c1)
    draw_bezier(ctx, c1)
    draw_control_points(ctx, c2)
    draw_bezier(ctx, c2)
    draw_intersections(ctx, i)
    ctx.restore()
    


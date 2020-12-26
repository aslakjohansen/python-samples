#!/usr/bin/env python3

import bezier as b
import cairo
from math import pi

#####################################################################
############################################################## inputs

filename = 'intersections.pdf'
width = 1920
height = width*9/16

bezier = [(100,540), (400,640), (1520,440), (1820,540)]

#####################################################################
############################################################# helpers

def draw_control_points (ctx, bezier):
    for point in bezier:
        ctx.save()
        ctx.arc(point[0], point[1], 2, 0, 2*pi)
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
    ctx.set_line_width(1)
    ctx.set_source_rgb(1, 0, 0)
    ctx.stroke()
    ctx.restore()

#####################################################################
################################################################ main

# canvas
surface = cairo.PDFSurface(filename, width, height)
ctx = cairo.Context(surface)

draw_control_points(ctx, bezier)
draw_bezier(ctx, bezier)


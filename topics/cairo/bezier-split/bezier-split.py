#!/usr/bin/env python3

import cairo
from math import pi


#####################################################################
############################################################## inputs

filename = 'beziercut.pdf'
width = 1920.0
height = width*9/16
border = 100
bezier = [(border,height/2),
          (width/2,border),
          (3*width/4,height-border),
          (width-border,height/2)]

#####################################################################
############################################################# helpers

def draw_control_points (ctx, bezier, radius=4, color=(0.0, 1.0, 0.0)):
    for point in bezier:
        ctx.save()
        ctx.arc(point[0], point[1], radius, 0, 2*pi)
        ctx.set_source_rgb(color[0], color[1], color[2])
        ctx.fill()
        ctx.restore()

def draw_bezier (ctx, bezier, width=2, color=(0.0, 0.0, 0.0)):
    ctx.save()
    origin = bezier[0]
    ctx.move_to(origin[0], origin[1])
    p1 = bezier[1]
    p2 = bezier[2]
    p3 = bezier[3]
    ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
    ctx.set_line_width(width)
    ctx.set_source_rgb(color[0], color[1], color[2])
    ctx.stroke()
    ctx.restore()

def interpolate (a, b, t):
    return a+(b-a)*t

def bezier_split (bezier, t):
    p1x = bezier[0][0]
    p1y = bezier[0][1]
    p2x = bezier[1][0]
    p2y = bezier[1][1]
    p3x = bezier[2][0]
    p3y = bezier[2][1]
    p4x = bezier[3][0]
    p4y = bezier[3][1]
    
    i1x = interpolate(p1x, p2x, t)
    i1y = interpolate(p1y, p2y, t)
    i2x = interpolate(p2x, p3x, t)
    i2y = interpolate(p2y, p3y, t)
    i3x = interpolate(p3x, p4x, t)
    i3y = interpolate(p3y, p4y, t)
    
    ii1x = interpolate(i1x, i2x, t)
    ii1y = interpolate(i1y, i2y, t)
    ii2x = interpolate(i2x, i3x, t)
    ii2y = interpolate(i2y, i3y, t)
    
    iii1x = interpolate(ii1x, ii2x, t)
    iii1y = interpolate(ii1y, ii2y, t)
    
    return [[(p1x,p1y),(i1x,i1y),(ii1x,ii1y),(iii1x,iii1y)],
            [(iii1x,iii1y),(ii2x,ii2y),(i3x,i3y),(p4x,p4y)]]

#####################################################################
################################################################ main

# canvas
surface = cairo.PDFSurface(filename, width, height)
ctx = cairo.Context(surface)

#draw_control_points(ctx, bezier)
draw_bezier(ctx, bezier, 8)

subs = bezier_split(bezier, 3.0/4)
draw_control_points(ctx, subs[0], 8, (0,1,0))
draw_bezier(ctx, subs[0], 4, (0,1,0))
#draw_control_points(ctx, subs[1], 8, (1,0,1))
#draw_bezier(ctx, subs[1], 4, (1,0,1))


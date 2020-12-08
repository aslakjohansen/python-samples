#!/usr/bin/env python3

from subprocess import Popen, STDOUT, PIPE
from os import linesep

import cairo
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg as rsvg

prefix = 'prefix'

latex = '''
$
f(n) = \sqrt{n^2}
$
'''
#$
#f(n) =
#\\begin{cases}
#  n/2 , & \\text{if }n\\text{ is even} \\\\
#  3n+1, & \\text{if }n\\text{ is odd}
#\end{cases}
#$


# paths
tex_filename      = '%s.tex' % prefix
pdf_filename      = '%s.pdf' % prefix
pdf_crop_filename = '%s_crop.pdf' % prefix
svg_crop_filename = '%s_crop.svg' % prefix
output_filename   = '%s_result.pdf' % prefix

#####################################################################
############################################################# helpers

def system (command, err=STDOUT, out=PIPE):
    p = Popen(command, shell=True, stderr=err, stdout=out)
    output = p.communicate()[0]
    return output.decode('utf-8') 

def write_file (filename, lines):
    with open(filename, 'w') as fo:
        fo.writelines(lines)

#####################################################################
############################################################### steps

def generate_latex_file (filename, contents):
    lines = [
        '\\documentclass{article}',
        '\\usepackage[utf8]{inputenc}',
        '\\usepackage{amsmath,amssymb,amsfonts,amsthm}',
        '\\begin{document}',
        '\\thispagestyle{empty}',
        contents,
        '\\end{document}',
    ]
    write_file(filename, map(lambda line: line+linesep, lines))

def latex2pdf (ifilename, ofilename):
    system('pdflatex %s' % ifilename)
    tfilename = '.'.join(ifilename.split('.')[:-1])+'.pdf'
    system('cp %s %s' % (tfilename, ofilename))

def crop_pdf (ifilename, ofilename):
    system('pdfcrop %s %s' % (ifilename, ofilename))

def pdf2svg (ifilename, ofilename):
    system('pdf2svg %s %s' % (ifilename, ofilename))

def embed_svg (ifilename, ofilename):
    handle = rsvg.Handle()
    svg = handle.new_from_file(ifilename)
    dims = svg.get_dimensions()
    
    surface = cairo.PDFSurface(ofilename, dims.width, dims.height)
    ctx = cairo.Context(surface)
    svg.render_cairo(ctx)
    
    ctx.move_to(0,0)
    ctx.line_to(dims.width, dims.height)
    ctx.set_source_rgb(1, 0, 0)
    ctx.stroke()

#####################################################################
################################################################ main

generate_latex_file(tex_filename, latex)
latex2pdf(tex_filename, pdf_filename)
crop_pdf(pdf_filename, pdf_crop_filename)
pdf2svg(pdf_crop_filename, svg_crop_filename)
embed_svg(svg_crop_filename, output_filename)


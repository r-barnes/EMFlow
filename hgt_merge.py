#!/usr/bin/env python

#Creates a seamless, rectangular, square, 2-byte signed integer representation
#of the input files.

import sys
import re

if len(sys.argv)==1:
  print("Syntax: {0} <OUTPUT FILE> <DIMENSION> <SRTM1 FILE> [SRTM1 FILE] [SRTM1 FILE]".format(sys.argv[0]))
  print("SRTM1 files have dimensions 3601x3601")
  print("DIMENSION is the requested size of the NxN output.")
  sys.exit(-1)

outputname = sys.argv[1]
DIMENSION  = int(sys.argv[2])
files      = sys.argv[3:]

xmin = 9999999999999
xmax = -99999999999999
ymin = 999999999999999
ymax = -999999999999999

#Get dimensions of grid of files
for f in files:
  try:
    x = int(re.match('.*N([0-9][0-9])W[0-9][0-9][0-9].hgt', f).group(1))
    y = int(re.match('.*N[0-9][0-9]W([0-9][0-9][0-9]).hgt', f).group(1))
  except:
    print("Invalid filename '{0}' detected".format(f))
    sys.exit(-1)
  xmin = min(xmin,x)
  xmax = max(xmax,x)
  ymin = min(ymin,y)
  ymax = max(ymax,y)

height = ymax-ymin+1
width  = xmax-xmin+1

print("Found width={0}, height={1} files.".format(width,height))

if width*3601<DIMENSION:
  print("There are not enough files along the X dimension to satisfy DIMENSION.")
  sys.exit(-1)

if height*3601<DIMENSION:
  print("There are not enough files along the Y dimension to satisfy DIMENSION.")
  sys.exit(-1)

filegrid = [[None]*width for y in range(height)]

for f in files:
  try:
    x = int(re.match('.*N([0-9][0-9])W[0-9][0-9][0-9].hgt', f).group(1))-xmin
    y = int(re.match('.*N[0-9][0-9]W([0-9][0-9][0-9]).hgt', f).group(1))-ymin
  except:
    print("Invalid filename '{0}' detected".format(f))
    sys.exit(-1)
  filegrid[y][x] = open(f,'rb')

fout = open(outputname, 'wb')

#Big-endian representation of the SRTM no-data value. A whole row of them.
missing_val = b'\x80\x00'

for y in range(DIMENSION):
  for x in range(0,DIMENSION,3601):
    f          = filegrid[y/3601][x/3601]
    this_width = min(3601,DIMENSION-x)
    if f is None:
      fout.write(missing_val*this_width)
    else:
      rowbytes = f.read(2*this_width)
      fout.write(rowbytes)

fout.close()
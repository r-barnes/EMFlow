#!/usr/bin/env python

#Creates a seamless, rectangular, 2-byte signed integer representation of the
#input files

import sys

if len(sys.argv)==1:
  print("Syntax: {0} <OUTPUT FILE> <SRTM1 FILE> [SRTM1 FILE] [SRTM1 FILE]".format(sys.argv[0]))
  print("SRTM1 files have dimensions 3601x3601")
  sys.exit(-1)

files = sys.argv[2:]

#Get dimensions of grid of files
yvals  = map(lambda x: int(x[1:3]), files)
ymin   = min(yvals)
ymax   = max(yvals)
height = ymax-ymin+1

#Get dimensions of grid of files
xvals = map(lambda x: int(x[4:7]), files)
xmin  = min(xvals)
xmax  = max(xvals)
width = xmax-xmin+1

filegrid = [[None]*width for y in range(height)]

for f in files:
  y = int(f[1:3])-ymin
  x = int(f[4:7])-xmin
  filegrid[y][x] = open(f,'rb')

fout = open(sys.argv[1], 'wb')

#Big-endian representation of the SRTM no-data value. A whole row of them.
missing_row = b'\x80\x00'*3601

for y in filegrid:                 #Iterate over each row of files
  for row in range(3601):          #For each row, iterate over each line of each file
    for x in y:                    #Looking at each file for each line
      if x is None:                #If there is no file here
        fout.write(missing_row)    #Insert a row of missing data values
      else:
        rowbytes = x.read(2*3601)  #Otherwise, insert the appropriate line from the appropriate file
        fout.write(rowbytes)

fout.close()
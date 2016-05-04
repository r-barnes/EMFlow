#!/usr/bin/env python

#Creates a seamless, rectangular, square, 2-byte signed integer representation
#of the HGT input files.

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

#Initial values for xmin, xmax, ymin, ymax ensure any actual numbers get used
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

#Calculate height and width. They are inclusive ranges, so add 1.
height = ymax-ymin+1
width  = xmax-xmin+1

print("Found width={0}, height={1} files.".format(width,height))

#Sanity check
if width*3601<DIMENSION:
  print("There are not enough files along the X dimension to satisfy DIMENSION.")
  sys.exit(-1)

if height*3601<DIMENSION:
  print("There are not enough files along the Y dimension to satisfy DIMENSION.")
  sys.exit(-1)

#Create grid to hold input files
filegrid = [[None]*width for y in range(height)]

#Load input files into the grid
for f in files:
  try:
    x = int(re.match('.*N([0-9][0-9])W[0-9][0-9][0-9].hgt', f).group(1))-xmin
    y = int(re.match('.*N[0-9][0-9]W([0-9][0-9][0-9]).hgt', f).group(1))-ymin
  except:
    print("Invalid filename '{0}' detected".format(f))
    sys.exit(-1)
  filegrid[y][x] = open(f,'rb')

#Open an output file
fout = open(outputname, 'wb')

#Big-endian representation of the SRTM no-data value. Used for places where
#there was no input file avilable. This allows for irregular boundaries for the
#combined dataset.
missing_val = b'\x80\x00'

#Go through each column
for y in range(DIMENSION):
  #Step by 3601 so we can read in a whole row from a file at a time. This makes
  #things much faster
  for x in range(0,DIMENSION,3601):
    f          = filegrid[y/3601][x/3601] #What file is this in?
    this_width = min(3601,DIMENSION-x)    #Do we want all or part of this row?
    if f is None:                         #There is no file
      fout.write(missing_val*this_width)  #So write a row of missing data
    else:
      rowbytes = f.read(2*this_width)     #Read in the appropriate amount of the row
      fout.write(rowbytes)                #Write it out again

fout.close()                              #Close output file
EMFlow
======
Compute the drainage network on digital elevation models stored in external memory.

Compilation
-----------
To compile, run **make** or use:

    g++ -O3 -o EMFlow hydrogEmFillFlow.cpp lz4.c

Running
-------
To run, the following changes need to be made:

 * Set the amount of memory available in MB on Line 77 of hydrogEmFillFlow.cpp
 * Set the tiled block size on Line 76 of hydrogEmFillFlow.cpp
 * Set the amount of memory available in MB on Line 44 of flow.cpp
 * Set the tiled block size on Line 43 of flow.cpp.

    ./EMFlow nrows terrain_name.hgt

Generating Input Data
---------------------
The program reads its data from a single file which represents terrain as a
two-byte, big-endian, signed integer. The data in such a file can be drawn from
Shuttle Radar Topography Mission SRTM3 files. An attached script `hgt_merge.py`
will read in a number of these files and produce an output suitable for
processing.


About the Script
----------------
* .creat folder tiles to store temporary tiles, the tiles folder is necessary for the program operation
* .creat folder tempos to store the running time
* .Run the program for several instances and stores the runtime

Output
------
As a result it is given a file named flow.hgt containing the accumulated flow with 2 bytes.

Bibliography
------------
This program is described by the publication

Thiago L. Gomes, Salles V. G. Magalhães, Marcus V. A. Andrade, W. Randolph Franklin, and Guilherme C. Pena. 2012. Computing the drainage network on huge grid terrains. In Proceedings of the 1st ACM SIGSPATIAL International Workshop on Analytics for Big Geospatial Data (BigSpatial '12). ACM, New York, NY, USA, 53-60. DOI=10.1145/2447481.2447488 http://doi.acm.org/10.1145/2447481.2447488 ([Download](http://dx.doi.org/10.1145/2447481.2447488))

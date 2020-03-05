#!/bin/bash

gdalbuildvrt brasilNDVIq.vrt *.tif -srcnodata 0 -vrtnodata 0
gdal_translate brasilNDVIq.vrt brasilNDVIq.tif -co COMPRESS=LZW -co BIGTIFF=YES -co TILED=YES -a_nodata 0
gdaladdo -ro brasilNDVIq.tif 2 4 8

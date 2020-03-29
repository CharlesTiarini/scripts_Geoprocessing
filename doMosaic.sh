#!/bin/sh

NOME='totalNDVIqV3'

gdalbuildvrt $NOME.vrt *.tif -srcnodata 0 -vrtnodata 0
gdal_translate $NOME.vrt $NOME.tif -co COMPRESS=LZW -co BIGTIFF=YES -co TILED=YES -a_nodata 0
gdaladdo -ro $NOME.tif 2 4 8

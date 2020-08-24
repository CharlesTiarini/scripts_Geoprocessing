#!/bin/bash

for NOME in '1500_1_99_NDVIq' '1500_1_99_CVP' '1500_5_95_NDVIq' '1500_5_95_CVP' '1500_10_90_NDVIq' '1500_10_90_CVP' '1500_percentil' '2400_1_99_NDVIq' '2400_1_99_CVP' '2400_5_95_NDVIq' '2400_5_95_CVP' '2400_10_90_NDVIq' '2400_10_90_CVP' '2400_percentil';
do
    echo $NOME
	gdalbuildvrt $NOME.vrt $NOME*.tif -srcnodata 0 -vrtnodata 0
	gdal_translate $NOME.vrt $NOME.tif -co COMPRESS=LZW -co BIGTIFF=YES -co TILED=YES -a_nodata 0
	#gdaladdo -ro $NOME.tif 2 4 8
	echo $NOME 'is done'
done


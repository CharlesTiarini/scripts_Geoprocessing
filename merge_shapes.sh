#!/bin/bash
#Created by charlestiarini@gmail.com

file="./nascentes_cerrado.shp"

for i in $(ls *.shp*)
do

      if [ -f "$file" ]
      then
           ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4326 -update -append $file $i -nln nascentes_cerrado
      else
           echo "merging……"
           ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4326 $file $i
fi
done

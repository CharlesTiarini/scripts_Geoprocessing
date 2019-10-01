# -*- coding: utf-8 -*-
import sys
import json
import ee

ee.Initialize()

MATOPIBA_PATHROW = ee.FeatureCollection("users/charlestiarini/matopibaProdes")
PATHROW_LIST = ['218069', '218070', '219062', '219063', '219064', '219065', '219066', '219067', '219068', '219069', '219070', '220062', '220063', '220064', '220065', '220066', '220067', '220068', '220069', '220070', '220071', '221062', '221063', '221064', '221065', '221066', '221067', '221068', '221069', '222064', '222065', '222066', '222067', '222068', '222069', '223064', '223065', '223066', '223067', '223068', '223069']
BANDS = ['B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11' ]

def inter(img, result):
  band = img.select(band_name).rename([img.get('DATE_ACQUIRED')])
  return ee.Image(result).addBands([band])

for pathrow in PATHROW_LIST:
	
  print(pathrow)
  pathrow_limit = MATOPIBA_PATHROW.filter(ee.Filter.eq('PathRow',pathrow))
	
  scene = pathrow_limit.first()
  sceneGeometry = scene.geometry()

  startDt = ee.String(scene.get('Inicio'))
  endDt = ee.String(scene.get('Fim'))
	
  imgs = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterBounds(scene.geometry().centroid()).filterDate(startDt, endDt)  
  print(imgs.size().getInfo())

  for band_name in BANDS:

    first = ee.Image()
    b4Stack = imgs.iterate(inter, first)

    b4Stack = ee.Image(b4Stack)
    b4Stack = b4Stack.multiply(10000)
    b4Stack = b4Stack.toInt16()
    b4Stack = b4Stack.clip(sceneGeometry)
    
    boundary = ee.Feature(scene).geometry().bounds().getInfo()['coordinates']

    task_config = {
      'fileNamePrefix': str(pathrow)+"_"+str(band_name),
      'scale': 30,
      'maxPixels': 1e13,
      'fileFormat': 'GeoTIFF',
      'skipEmptyTiles': True,
      'region': boundary ,
      'folder': 'CuboBandas'
      }

    task = ee.batch.Export.image.toDrive(b4Stack, str(pathrow)+"_"+str(band_name), **task_config)

    task.start()

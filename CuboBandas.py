# -*- coding: utf-8 -*-
import sys
import json
import ee

ee.Initialize()

PRODES_ANTROPICO = ee.Image("users/charlestiarini2/prodesAntropico")
MATOPIBA_PATHROW = ee.FeatureCollection("users/charlestiarini2/matopibaAnos2")
PATHROW_LIST = ['218069', '218070', '219062', '219063', '219064', '219065', '219066', '219067', '219068', '219069', '219070', '220062', '220063', '220064', '220065', '220066', '220067', '220068', '220069', '220070', '220071', '221062', '221063', '221064', '221065', '221066', '221067', '221068', '221069', '222064', '222065', '222066', '222067', '222068', '222069', '223064', '223065', '223066', '223067', '223068', '223069']
BANDS = ['B1','B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11' ]

def inter(img, result):
  band = img.select(band_name).rename([img.get('DATE_ACQUIRED')])
  return ee.Image(result).addBands([band])


Anos = [15, 16, 17]

for Inicio in Anos:

  Fim = str(Inicio+1)

  agua = PRODES_ANTROPICO.mask(PRODES_ANTROPICO.gt(96))
  agua = agua.divide(agua)
  agua = agua.unmask()

  accu = PRODES_ANTROPICO.mask(PRODES_ANTROPICO.lte(Inicio))
  accu = accu.add(1)accu
  accu = accu.divide(accu)
  accu = accu.unmask()

  mask = accu.add(agua)

  for pathrow in PATHROW_LIST:
    
    print(pathrow)
    pathrow_limit = MATOPIBA_PATHROW.filter(ee.Filter.eq('PathRow',pathrow))
    
    scene = pathrow_limit.first()
    sceneGeometry = scene.geometry()

    startDt = ee.String(scene.get(str(Inicio)))
    endDt = ee.String(scene.get(str(Fim)))
    
    imgs = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterBounds(scene.geometry().centroid()).filterDate(startDt, endDt)  
    #print(imgs.size().getInfo())

    for band_name in BANDS:

      first = ee.Image()
      bands_stack = imgs.iterate(inter, first)

      bands_stack = ee.Image(bands_stack)
      bands_stack = bands_stack.multiply(10000)
      bands_stack = bands_stack.toInt16()
      bands_stack = bands_stack.clip(sceneGeometry)

      bands_stack = bands_stack.mask(mask.eq(0))
      
      boundary = ee.Feature(scene).geometry().bounds().getInfo()['coordinates']

      task_config = {
        'fileNamePrefix': str(Inicio)+"_"+str(pathrow)+"_"+str(band_name),
        'scale': 30,
        'maxPixels': 1e13,
        'fileFormat': 'GeoTIFF',
        'skipEmptyTiles': True,
        'region': boundary ,
        'folder': 'CuboBandas_'+str(Inicio)
        }

      task = ee.batch.Export.image.toDrive(bands_stack, "20"+str(Inicio+1)+"_"+str(pathrow)+"_"+str(band_name), **task_config)

      task.start()

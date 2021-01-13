# -*- coding: utf-8 -*-
###### charlestiarini@gmail.com #####
import sys
import json
import ee

ee.Initialize()

MATOPIBA_PATHROW = ee.FeatureCollection("users/charlestiarini/matopibaProdes")
PATHROW_LIST = ['218069']#, '218070', '219062', '219063', '219064', '219065', '219066', '219067', '219068', '219069', '219070', '220062', '220063', '220064', '220065', '220066', '220067', '220068', '220069', '220070', '220071', '221062', '221063', '221064', '221065', '221066', '221067', '221068', '221069', '222064', '222065', '222066', '222067', '222068', '222069', '223064', '223065', '223066', '223067', '223068', '223069']
BANDS = ['B1']#, 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11' ]

def clipCollection(img):
  pathrow = ee.Number(img.get('WRS_PATH')).format().cat(ee.Number(img.get('WRS_ROW')).format())
  gridSelect = MATOPIBA_PATHROW.filter(ee.Filter.eq('PathRow',pathrow))
  return img.clip(gridSelect)

def inter(img, result):
  band_name = img.select(band).rename([img.get('DATE_ACQUIRED')])
  return ee.Image(result).addBands([band_name])

for pathrow in PATHROW_LIST:

 print("Start: "+pathrow)

 pathrow_limit = MATOPIBA_PATHROW.filter(ee.Filter.eq('PathRow',pathrow))

 scene = pathrow_limit.first()

 date = ee.Date(scene.get('Inicio'))

 collection = []
   
 for i in range(26): 
  img = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
          .filterBounds(scene.geometry().centroid()) \
          .filterDate(date, date.advance(1, 'day')) \
          .map(clipCollection)
            
  if (img.size().getInfo()):
    collection.append(ee.Image(img.first()))
  else: 
    flag = ee.Image() \
             .set('DATE_ACQUIRED', date.format('YYYY-MM-dd')) \
             .rename(BANDS) \
             .clip(scene.geometry())
              #.addBands([0]) \
      ##, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) \
    collection.append(flag)
  date = date.advance(16, 'day')

 collection = ee.ImageCollection(collection)

 for band in BANDS:

  print(band+" of "+pathrow)

  first = ee.Image().clip(scene.geometry()) 
  bands_stack = collection.iterate(inter, first)
  bands_stack = ee.Image(bands_stack) \
                  .multiply(10000) \
                  .toInt16() 

  boundary = ee.Feature(scene).geometry().bounds().getInfo()['coordinates']
  nameTask = str(pathrow)+"_"+str(band)
  folder = 'BandasTranspostas'

  task = ee.batch.Export.image.toDrive(
    image = bands_stack, 
    description = nameTask,
    fileNamePrefix = nameTask,
    folder = folder,
    region = boundary,
    skipEmptyTiles = True,
    fileFormat = 'GeoTIFF',
    maxPixels = 1e13,
    scale = 30
  )
  
  task.start()

print("FIM")


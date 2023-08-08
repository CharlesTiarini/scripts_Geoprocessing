!pip install git+https://github.com/urbanogilson/SICAR.git install git+https://github.com/urbanogilson/SICAR.git
!pip install matplotlib geopandas
!pip install 'SICAR[paddle] @  git+https://github.com/urbanogilson/SICAR'
!sudo apt install tesseract-ocr

from SICAR import Sicar
from SICAR.drivers import Tesseract
import pprint

# Create Sicar instance
car = Sicar(email = "charlestiarini@gmail.com", driver=Tesseract)

# Get cities codes in state
cities_codes = car.get_cities_codes(state='GO')

#pprint.pprint(cities_codes)

car.download_state(state='GO', folder='SICAR/GO')

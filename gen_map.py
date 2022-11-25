from shapely.geometry import Point, Polygon
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

data = pd.read_csv('gustav/dff.csv')

data = data['Institution']

institutions = []

new = []

for i in data:
    if i not in institutions:
        institutions.append(str(i))

for data in institutions:
    new.append(data.split())


new = sorted(new)
institutions = sorted(institutions)
    
    





def map_box(data, backup_data):

    locations = data

    map_data = map_data = pd.DataFrame({'location': [], 'lat': [], 'lon': []})  

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    

    try:

        for data in locations:
            location = geolocator.geocode(data)

            lat = location.latitude
            lon = location.longitude
            map_data = map_data.append({'location': [data], 'lat': [lat], 'lon': [lon]}, ignore_index=True)
    
    except AttributeError:
        
        map_data = map_data.append({'location': [data], 'lat': ['Not found'], 'lon': ['Not found']}, ignore_index=True)

    return map_data

map_data = map_box(institutions, new)

map_data.to_csv('lat_lon.csv', index=False)
import pandas as pand
from math import sin, cos, sqrt, atan2, radians

dt = pand.read_csv("test2.csv")
dt['tanggal_jam'] = pand.to_datetime(dt['tanggal_jam'], format='%d-%m-%Y %H:%M')

def getJarakFromLatLonInKm(lat1,lon1,lat2,lon2):
	R = 6371
	dLat = radians(lat2-lat1)
	dLon = radians(lon2-lon1)
	rLat1 = radians(lat1)
	rLat2 = radians(lat2)
	a = sin(dLat/2) * sin(dLat/2) + cos(rLat1) * cos(rLat2) * sin(dLon/2) * sin(dLon/2) 
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	d = R * c # Distance in km
	return d

def hitung_v(dist_km, time_start, time_end):
	"""Return 0 if time_start == time_end, avoid dividing by 0"""
	return dist_km / (time_end - time_start).seconds if time_end > time_start else 0

dt = dt.sort_values(by=['nama_kapal', 'tanggal_jam'])
dt['lat0'] = dt.groupby('nama_kapal')['lat'].transform(lambda x: x.iat[0])
dt['lon0'] = dt.groupby('nama_kapal')['lng'].transform(lambda x: x.iat[0])
dt['t0'] = dt.groupby('nama_kapal')['tanggal_jam'].transform(lambda x: x.iat[0])

dt['dist_km'] = dt.apply(
    lambda row: getJarakFromLatLonInKm(
        lat1=row['lat'],
        lon1=row['lng'],
        lat2=row['lat0'],
        lon2=row['lon0']
    ),
    axis=1
)

# create a new column for velocity
dt['velocity_kmps'] = dt.apply(
    lambda row: hitung_v(
        dist_km=row['dist_km'],
        time_start=row['t0'],
        time_end=row['tanggal_jam']
    ),
    axis=1
)

print(dt[['nama_kapal', 'tanggal_jam', 'lat', 'lng', 'dist_km', 'velocity_kmps']])
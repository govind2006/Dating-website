from geopy.geocoders import Nominatim
from geopy import distance
import math
def findistance(c1,c2):
	geolocater  = Nominatim(user_agent="geoapiExercises")
	l1 = geolocater.geocode(c1)
	l2 = geolocater.geocode(c2)
	loc1 = (l1.latitude,l1.longitude)
	loc2 = (l2.latitude,l2.longitude)
	d = math.ceil(distance.distance(loc1,loc2).km)
	return d
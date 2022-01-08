from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    """ Distance in kilometers beetween two coordinate points on Earth"""
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

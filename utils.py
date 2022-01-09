from math import cos, asin, sqrt, pi
import requests
import json

def distance(lat1, lon1, lat2, lon2):
    """ Distance in kilometers beetween two coordinate points on Earth"""
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...


def route_by_foot(lat_1, lon_1, lat_2, lon_2):
    """ API docs: http://project-osrm.org/docs/v5.5.1/api/#tile-service """
    #f_str = f"http://router.project-osrm.org/route/v1/foot/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false"
    f_str = f"https://routing.openstreetmap.de/routed-foot/route/v1/driving/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false"
    print(f"Querying... {f_str}")
    r = requests.get(f_str)
    routes = json.loads(r.content)
    distance = routes.get("routes")[0]["distance"]
    duration_seconds = routes.get("routes")[0]["duration"]
    return distance, duration_seconds

def sec_to_min(secs: int, return_secs=False):
    minutes = int(secs) // 60
    remaind = int(secs) % 60
    if return_secs:
        return f"{minutes} min"
    else:
        return f"{minutes} min, {remaind} s"

if __name__ == "__main__":
    dist, dur = route_by_foot(-27.597313, -48.527230, -27.597167, -48.525964)
    print(f"It takes {dur} seconds to walk {dist} meters.")
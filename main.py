#! /usr/bin/python
from geopy import Nominatim #, distance
import pandas as pd
from utils import distance, route_by_foot
import folium

addresses = pd.read_csv(filepath_or_buffer="inputs/addresses.csv", sep=";")
work_address = pd.read_csv(filepath_or_buffer="inputs/work_coordinates.csv", sep=";")
print("Loaded work at coordinates:\n", work_address)
work_latitude:str = work_address["Latitude"].to_string(index=False)
work_longitude:str = work_address["Longitude"].to_string(index=False)
locator = Nominatim(user_agent="myGeocoder")

addresses["LocationsObj"] = addresses["Address"].apply(lambda x:locator.geocode(x))
addresses["Latitude"] = addresses["LocationsObj"].apply(lambda x:x.latitude)
addresses["Longitude"] = addresses["LocationsObj"].apply(lambda x:x.longitude)
# addresses["FullAddress"] = addresses["LocationsObj"].apply(lambda x:x.address)
addresses["DistanceTimeByFoot"] = addresses["LocationsObj"].apply(
    lambda this: route_by_foot(
        work_latitude, 
        work_longitude,
        this.latitude,
        this.longitude
    )
)

addresses["DistanceByFoot(m)"] = addresses["DistanceTimeByFoot"][0]
addresses["DurationByFoot(s)"] = addresses["DistanceTimeByFoot"][1]
addresses.drop(columns=["LocationsObj", "DistanceTimeByFoot"], inplace=True)

map = folium.Map(location=[work_latitude, work_longitude], zoom_start=15)

folium.Marker(
    location=[
        work_latitude, 
        work_longitude
    ],
    icon=folium.Icon(color="red", icon="briefcase")
).add_to(map)

addresses.apply(
    lambda row:folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ], 
    ).add_to(map), 
    axis=1
)

print(addresses)

OUTPUT_MAP="outputs/map.html"
print(f"Saving map to {OUTPUT_MAP}...")
map.save(OUTPUT_MAP)


# print(f"Latitude = {location.latitude}, Longitude = {location.longitude}")
#! /usr/bin/python
from geopy import Nominatim #, distance
import pandas as pd
from utils import distance
# import geopy as gp

addresses = pd.read_csv(filepath_or_buffer="input/addresses.csv", sep=";")
work_address = pd.read_csv(filepath_or_buffer="input/work_coordinates.csv", sep=";")
print("Loaded work at coordinates:\n", work_address)
locator = Nominatim(user_agent="myGeocoder")

addresses["LocationsObj"] = addresses["Address"].apply(lambda x:locator.geocode(x))
addresses["Latitude"] = addresses["LocationsObj"].apply(lambda x:x.latitude)
addresses["Longitude"] = addresses["LocationsObj"].apply(lambda x:x.longitude)
# addresses["FullAddress"] = addresses["LocationsObj"].apply(lambda x:x.address)
addresses["Distance"] = addresses["LocationsObj"].apply(
    lambda this: distance(
        work_address["Latitude"], 
        work_address["Longitude"],
        this.latitude,
        this.longitude
    )
)
addresses.drop(columns="LocationsObj", inplace=True)

work_address



print(addresses)
# print(f"Latitude = {location.latitude}, Longitude = {location.longitude}")
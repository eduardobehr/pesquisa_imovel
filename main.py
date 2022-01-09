#! /usr/bin/python
from folium.map import Popup
from geopy import Nominatim
from numpy import number #, distance
import pandas as pd
from utils import route_by_foot, sec_to_min
import folium
from folium import plugins

import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

addresses: pd.DataFrame = pd.read_csv(filepath_or_buffer="inputs/addresses.csv", sep=";")
work_address = pd.read_csv(filepath_or_buffer="inputs/work_coordinates.csv", sep=";")
print("Loaded work at coordinates:\n", work_address)
work_latitude:str = work_address["Latitude"].to_string(index=False)
work_longitude:str = work_address["Longitude"].to_string(index=False)
locator = Nominatim(user_agent="myGeocoder")

def get(obj, attr):
    try:
        return obj.__getattribute__(attr)
    except Exception as exc:
        print(exc.args)
        return 0

def get_coordinates(address):
    print(f"Getting coordinates of '{address}'...")
    try:
        coord = locator.geocode(address)
        print(f" Found {coord.latitude}, {coord.longitude}")
        return coord 
    except Exception as exc:
        print(f" Failed to get coordinates of {address}", exc.args)
        return 0

def thread_get_coordinates(df_index):
    addresses["LocationsObj"].iloc[df_index] = get_coordinates(addresses["Address"].iloc[df_index])


# API geographic request

addresses["LocationsObj"] = addresses["Address"].apply(lambda x:get_coordinates(x))
addresses["Latitude"] = addresses["LocationsObj"].apply(lambda x:get(x,"latitude"))
addresses["Longitude"] = addresses["LocationsObj"].apply(lambda x:get(x,"longitude"))

# Create column with tuple: (distance, duration) returned by 'route_by_foot'
addresses["DistanceTimeByFoot"] = addresses["LocationsObj"].apply(
    lambda this: route_by_foot(
        work_latitude, 
        work_longitude,
        get(this, "latitude"),
        get(this, "longitude")
    )
)

# Extract corresponding distance and duration
addresses["DistanceByFoot(m)"] = addresses["DistanceTimeByFoot"].str.get(0)
addresses["DurationByFoot(s)"] = addresses["DistanceTimeByFoot"].str.get(1)

# Clean DataFrame
addresses.drop(columns=["LocationsObj", "DistanceTimeByFoot"], inplace=True)

# Create map
map = folium.Map(location=[work_latitude, work_longitude], zoom_start=15)

# Add marker to work place
folium.Marker(
    location=[
        work_latitude, 
        work_longitude
    ],
    icon=folium.Icon(color="red", icon="briefcase")
).add_to(map)

# Add markers to rental addresses
addresses.apply(
    lambda row:folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        tooltip=f'<p>Aluguel: R$ {row["Rent"]}</p>\
        <p>Distância a pé: {row["DistanceByFoot(m)"]} m</p> \n\
        Duração: {sec_to_min(row["DurationByFoot(s)"])}',
        popup=f'<a href={row["URL"]}>{row["URL"]}</a>',
        icon=folium.DivIcon(html=f"""<div style="font-size:large;font-weight: bold;font-family: courier new; color: {'green' if row["Rent"] < 901 else 'blue' if row["Rent"] <1201 else 'red'}">{"{:.0f}".format(row["Rent"])}</div>""")
    ).add_to(map), 
    axis=1
)

heat_data = [[row['Latitude'],row['Longitude']] for index, row in addresses.iterrows()]

map.add_child(plugins.HeatMap(data=heat_data, radius=60, blur=100,max_zoom=15, min_opacity=0.99))

print(addresses)

OUTPUT_MAP="outputs/map.html"
print(f"Saving map to {OUTPUT_MAP}...")
map.save(OUTPUT_MAP)


# print(f"Latitude = {location.latitude}, Longitude = {location.longitude}")
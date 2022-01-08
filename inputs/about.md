# How to use
## Addresses
Place addresses in file `addresses.csv` inside this subdirectory with the following format:

```csv
Address;Region
Rua José, 95;
Rua Maria, 2022;Downtown
```

**Note:** It must be `;` separated

## Work Coordinates
Place the coordinates in `work_coordinates.csv` to be able to compute the distance beetween this location and those from the addresses previously given. The coordinates inside the file must be given as follows:

```csv
Latitude;Longitude
27.000000;48.000000
```
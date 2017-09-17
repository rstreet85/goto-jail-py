# GoTo Jail
**Updated 09-16-2017**

Find all airports, prisons, and police stations in an area. This Python script uses the `requests` and `json` modules to query the USGS National Map Structures service layers to find [police stations](https://services.nationalmap.gov/arcgis/rest/services/structures/MapServer/9/query), [prison & jails](https://services.nationalmap.gov/arcgis/rest/services/structures/MapServer/11/query) and [airports](https://services.nationalmap.gov/arcgis/rest/services/transportation/MapServer/34/query) for a user-specified area. Prints lat/lon coordinates of all discovered structures to a file.

Input: `coordinates.txt`

Output: `jail.txt`

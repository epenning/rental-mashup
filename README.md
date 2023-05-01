# Rental Mashup

A Python script which searches information about rental properties by scraping information from Zillow and Google Fiber, as well as commute data and crime from APIs.

Filters are available as command line arguments, see `main.py`. Example:

```
python main.py -sort cheapest -minrent 500 -maxrent 1000 -minsqft 500 -maxsqft 1500 -work "1000 Main St" --fiber -traveltime 30 -crimeradius 2
```

Output is in `.csv` format with these columns:

`['address', 'postal_code', 'url', 'fiber_ready', 'transit_time', 'rent', 'lat', 'long', 'crimes']`

Example row in output:

'15 Rental St.', '55555', 'https://...', True, 15, 800, 33.333, 33.333, 2


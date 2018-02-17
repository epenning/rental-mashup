import googlemaps
from googlemaps import directions

gmaps = googlemaps.Client(key="AIzaSyDB7-DQ3AeMOwS-fsCOM7eINsk7NxNSlm4")


def travel_time(rental, mode, work):
    origin = rental['address'] + ' ' + rental['postal_code']

    try:
        routes = directions.directions(gmaps, origin, work, mode)
        return round(routes[0]['legs'][0]['duration']['value']/60)
    except (KeyError, IndexError):
        return None
    except Exception as e:
        print(e)
        return None

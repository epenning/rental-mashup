import googlemaps
from googlemaps import directions
from datetime import datetime

gmaps = googlemaps.Client(key="AIzaSyDB7-DQ3AeMOwS-fsCOM7eINsk7NxNSlm4")


def travel_time(rental, mode, work):
    origin = rental['address'] + ' ' + rental['postal_code']
    arrival_time = datetime.strptime('Feb 21 2018  10:00AM', '%b %d %Y %I:%M%p')

    try:
        routes = directions.directions(gmaps, origin, work, mode, arrival_time=arrival_time)
        return round(routes[0]['legs'][0]['duration']['value']/60)
    except (KeyError, IndexError):
        return None
    except Exception as e:
        print(e)
        return None

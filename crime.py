import spotcrime


def get_crimes(rental, radius):
    crimes = spotcrime.SpotCrime((float(rental['lat']), float(rental['long'])), radius/100, None, ['Other'], days=365)
    return crimes.get_incidents()

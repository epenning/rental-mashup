import unicodecsv as csv
import time
import zillow
import google_fiber
import travel

output_filename = "properties-Austin-TX.csv"
output_fieldnames = ['address', 'postal_code', 'url', 'fiber_ready', 'driving_time', 'transit_time', 'bicycling_time']


def find_rentals(filters, work):
    for page in range(1, 20):
        try:
            rentals = zillow.parse_page(filters, page)

            for rental in rentals:
                process(rental, work)

        except zillow.PageException:
            print("Failed to process page {0}".format(page))
            break


def process(rental, work):
    # zillow.get_details(rental)
    rental['fiber_ready'] = google_fiber.fiber_ready(rental)

    if work:
        rental['driving_time'] = travel.travel_time(rental, 'driving', work)
        rental['transit_time'] = travel.travel_time(rental, 'transit', work)
        rental['bicycling_time'] = travel.travel_time(rental, 'bicycling', work)

    print("Writing data to output file...")
    with open(output_filename, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames)
        writer.writerow(rental)

    time.sleep(2)

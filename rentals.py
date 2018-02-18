import unicodecsv as csv
import time
import zillow
import google_fiber
import travel

output_filename_base = "properties-Austin-TX"
output_filename_extension = ".csv"
output_fieldnames = ['address', 'postal_code', 'url', 'fiber_ready', 'driving_time', 'transit_time', 'bicycling_time']


def find_rentals(filters, work):
    for page in range(1, 100):
        try:
            rentals = zillow.parse_page(filters, page)

            for rental in rentals:
                start = time.time()
                process(rental, work, filters)
                if (time.time() - start) < 1:
                    time.sleep(1)

        except zillow.PageException:
            print("Failed to process page {0}".format(page))
            break


def process(rental, work, filters):
    # zillow.get_details(rental)
    rental['fiber_ready'] = google_fiber.fiber_ready(rental)

    if work:
        rental['driving_time'] = travel.travel_time(rental, 'driving', work)
        rental['transit_time'] = travel.travel_time(rental, 'transit', work)
        rental['bicycling_time'] = travel.travel_time(rental, 'bicycling', work)

    if not is_mismatch(rental, filters):
        print(rental['url'])

    with open(output_filename(rental, filters), 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames)
        writer.writerow(rental)


def output_filename(rental=None, filters=None, mismatch=False):
    if mismatch or is_mismatch(rental, filters):
        return output_filename_base + "-mismatch" + output_filename_extension

    return output_filename_base + output_filename_extension


def is_mismatch(rental, filters):
    return (filters and rental and ((filters.fiber and not rental['fiber_ready']) or
            (filters.traveltime and
             (rental['driving_time'] and rental['driving_time'] > filters.traveltime) and
             (rental['transit_time'] and rental['transit_time'] > filters.traveltime) and
             (rental['bicycling_time'] and rental['bicycling_time'] > filters.traveltime))))

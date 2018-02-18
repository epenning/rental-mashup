import time
import zillow
import google_fiber
import travel
import output


def find_rentals(filters, work):
    output.start_file("match")
    output.start_file("nofiber")
    output.start_file("mismatch")

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
    rental['fiber_ready'] = google_fiber.fiber_ready(rental)

    if work:
        rental['driving_time'] = travel.travel_time(rental, 'driving', work)
        rental['transit_time'] = travel.travel_time(rental, 'transit', work)

    output.append_file(get_output_filename(rental, filters), rental)


def get_output_filename(rental, filters):
    if traveltime_filter(rental, filters):
        return "mismatch"

    if fiber_filter(rental, filters):
        return "nofiber"

    return "match"


def traveltime_filter(rental, filters):
    return (filters.traveltime and
            (rental['driving_time'] and rental['driving_time'] > filters.traveltime) and
            (rental['transit_time'] and rental['transit_time'] > filters.traveltime))


def fiber_filter(rental, filters):
    return filters.fiber and not rental['fiber_ready']

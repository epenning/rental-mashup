import time
import zillow
import google_fiber
import travel
import output


def get_rentals(filters, work):
    results = {
        'match': output.read_csv('match'),
        'nofiber': output.read_csv('nofiber'),
        'mismatch': output.read_csv('mismatch')
    }

    find_rentals(results, filters, work)
    output_results(results)


def find_rentals(results, filters, work):
    for page in range(1, 100):
        try:
            process_page(results, filters, work, page)
        except zillow.PageException:
            print("Failed to process page {0}".format(page))
            break


def process_page(results, filters, work, page):
    start = time.time()

    rentals = zillow.parse_page(filters, page)
    process_rentals(rentals, results, filters, work)

    end = time.time()
    if (end - start) < 1:
        time.sleep(1)


def process_rentals(rentals, results, filters, work):
    for rental in rentals:
        address = rental['address']

        if address in results['match']:
            results['match'][address].update(rental)
        elif address in results['nofiber']:
            results['nofiber'][address].update(rental)
        elif address in results['mismatch']:
            results['mismatch'][address].update(rental)
        else:
            process_rental(rental, work)
            results[get_result(rental, filters)][address] = rental


def process_rental(rental, work):
    start = time.time()

    rental['fiber_ready'] = google_fiber.fiber_ready(rental)

    if work:
        rental['transit_time'] = travel.travel_time(rental, 'transit', work)

    end = time.time()
    if (end - start) < 1:
        time.sleep(1)


def get_result(rental, filters):
    if traveltime_filter(rental, filters):
        return 'mismatch'

    if fiber_filter(rental, filters):
        return 'nofiber'

    return 'match'


def traveltime_filter(rental, filters):
    return (filters.traveltime and
            (not rental['transit_time'] or
                (rental['transit_time'] and rental['transit_time'] > filters.traveltime)))


def fiber_filter(rental, filters):
    return filters.fiber and not rental['fiber_ready']


def output_results(results):
    init_files(results)
    for key, value in results.items():
        for address, rental in value.items():
            output.append_file(key, rental)


def init_files(results):
    for key in results:
        output.start_file(key)

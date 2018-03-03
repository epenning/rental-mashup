import time
import zillow
import google_fiber
import travel
import output
import crime


def get_rentals(filters):
    results = {
        'match': output.read_csv('match'),
        'nofiber': output.read_csv('nofiber'),
        'mismatch': output.read_csv('mismatch')
    }

    find_rentals(results, filters)
    output_results(results)


def find_rentals(results, filters):
    for page in range(1, 100):
        try:
            process_page(results, filters, page)
        except zillow.PageException:
            print("Failed to process page {0}".format(page))
            break


def process_page(results, filters, page):
    start = time.time()

    rentals = zillow.parse_page(filters, page)
    process_rentals(rentals, results, filters)

    end = time.time()
    if (end - start) < 2:
        time.sleep(2)


def process_rentals(rentals, results, filters):
    for rental in rentals:
        rental = update_results(rental, results)
        process_rental(rental, filters)
        results[get_result(rental, filters)][rental['address']] = rental


def update_results(rental, results):
    address = rental['address']

    for key, value in results.items():
        if address in value:
            results[key][address].update(rental)
            return results[key][address]

    return rental


def process_rental(rental, filters):
    start = time.time()
    did_request = False

    if 'fiber_ready' not in rental or rental['fiber_ready'] is False:
        rental['fiber_ready'] = google_fiber.fiber_ready(rental)
        did_request = True

    if filters.work and 'transit_time' not in rental:
        rental['transit_time'] = travel.travel_time(rental, 'transit', filters.work)
        did_request = True

    if filters.crimeradius and ('crimes' not in rental or not rental['crimes']):
        rental['crimes'] = len(crime.get_crimes(rental, filters.crimeradius))
        did_request = True

    end = time.time()
    if did_request and (end - start) < 1:
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
                (rental['transit_time'] and int(rental['transit_time']) > filters.traveltime)))


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

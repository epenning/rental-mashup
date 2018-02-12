import unicodecsv as csv
import time
import zillow

output_filename = "properties-Austin-TX.csv"
output_fieldnames = ['address', 'postal_code']


def find_rentals(filters):
    for page in range(1, 20):
        try:
            rentals = zillow.parse_page(filters, page)

            for rental in rentals:
                process(rental)

            time.sleep(2)
        except:
            print("Failed to process page {0}".format(page))
            break


def process(rental):
    print("Writing data to output file...")
    with open(output_filename, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames)
        writer.writerow(rental)

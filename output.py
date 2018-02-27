import unicodecsv as csv
import os

filename_base = "properties-Austin-TX"
filename_extension = ".csv"
fieldnames = ['address', 'postal_code', 'url', 'fiber_ready', 'transit_time', 'rent', 'lat', 'long', 'crimes']


def start_file(type, extension=filename_extension):
    with open(filename_base + "-" + type + extension, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def append_file(type, row, extension=filename_extension):
    with open(filename_base + "-" + type + extension, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writerow(row)


def read_csv(type, extension=filename_extension):
    if os.path.isfile(filename_base + "-" + type + extension):
        with open(filename_base + "-" + type + extension, 'rb') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            next(reader)
            return {
                row['address']: {k: v for k, v in row.items()}
                for row in reader
            }

    return {}

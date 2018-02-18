import unicodecsv as csv

filename_base = "properties-Austin-TX"
filename_extension = ".csv"
fieldnames = ['address', 'postal_code', 'lat', 'long', 'url', 'fiber_ready', 'transit_time', 'rent']


def start_file(type, extension=filename_extension):
    with open(filename_base + "-" + type + extension, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def append_file(type, row, extension=filename_extension):
    with open(filename_base + "-" + type + extension, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writerow(row)

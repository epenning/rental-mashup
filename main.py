import unicodecsv as csv
import argparse
import rentals

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """
    argparser.add_argument('sort', nargs='?', help=sortorder_help)
    args = argparser.parse_args()
    sort = args.sort

    with open(rentals.output_filename, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rentals.output_fieldnames)
        writer.writeheader()

    rentals.find_rentals(sort)

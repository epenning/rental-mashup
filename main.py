import unicodecsv as csv
import argparse
import rentals


def main():
    argparser = init_argparser()
    args = argparser.parse_args()
    sort = args.sort
    beds = args.beds

    with open(rentals.output_filename, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rentals.output_fieldnames)
        writer.writeheader()

    rentals.find_rentals(sort, beds)


def init_argparser():
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    sort_help = "newest : Latest property details,\ncheapest : Properties with cheapest price"
    argparser.add_argument('-sort', nargs='?', help=sort_help)

    beds_help = "minimum number of beds"
    argparser.add_argument('-beds', choices=range(1, 7), type=int, help=beds_help)

    return argparser


if __name__ == "__main__":
    main()

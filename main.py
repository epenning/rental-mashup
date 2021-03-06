import argparse
import rentals


def main():
    argparser = init_argparser()
    args = argparser.parse_args()
    rentals.get_rentals(args)


def init_argparser():
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    sort_help = "newest : Latest property details,\ncheapest : Properties with cheapest price"
    argparser.add_argument('-sort', nargs='?', help=sort_help)

    beds_help = "minimum number of beds"
    argparser.add_argument('-beds', choices=range(1, 7), type=int, help=beds_help)

    min_rent_help = "minimum rent"
    argparser.add_argument('-minrent', type=int, help=min_rent_help)

    max_rent_help = "maximum rent"
    argparser.add_argument('-maxrent', type=int, help=max_rent_help)

    min_sq_feet_help = "minimum rent"
    argparser.add_argument('-minsqft', type=int, help=min_sq_feet_help)

    max_sq_feet_help = "maximum rent"
    argparser.add_argument('-maxsqft', type=int, help=max_sq_feet_help)

    work_help = "work address"
    argparser.add_argument('-work', default=None, help=work_help)

    fiber_help = "google fiber ready"
    argparser.add_argument('--fiber', action="store_true", help=fiber_help)

    traveltime_help = "maximum travel time"
    argparser.add_argument('-traveltime', type=int, help=traveltime_help)

    crimeradius_help = "radius in miles to find close crime incidents"
    argparser.add_argument('-crimeradius', type=float, help=crimeradius_help)

    return argparser


if __name__ == "__main__":
    main()

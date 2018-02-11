from lxml import html
import requests
import unicodecsv as csv
import argparse
import time

output_filename = "properties-Austin-TX.csv"
output_fieldnames = ['address', 'postal_code']


def process(rental):
    print("Writing data to output file...")
    with open(output_filename, 'ab') as csv_file:
        writer = csv.DictWriter(csv_file, output_fieldnames)
        writer.writerow(rental)


def process_rentals(filter=None):
    base_url = "https://www.zillow.com/homes/for_rent/Austin-TX"
    newest_filter = "/days_sort"
    cheapest_filter = "/paymenta_sort"

    url = base_url

    if filter == "newest":
        url += newest_filter
    elif filter == "cheapest":
        url += cheapest_filter

    for page in range(1, 20):
        paged_url = url + "/{0}_p".format(page)
        print("Fetching data for page {0}...".format(page))
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
            response = requests.get(paged_url, headers=headers)
            parser = html.fromstring(response.text)
            search_results = parser.xpath("//div[@id='search-results']//article")

            for properties in search_results:
                raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
                raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")

                address = ' '.join(' '.join(raw_address).split()) if raw_address else None
                postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None

                if address:
                    rental = {
                        'address': address,
                        'postal_code': postal_code
                    }

                    process(rental)

            time.sleep(2)
        except:
            print("Failed to process page {0}:".format(page), paged_url)


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

    with open(output_filename, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_fieldnames)
        writer.writeheader()

    process_rentals(sort)

from lxml import html
import requests


def parse_page(sort, beds, page):
    print("Fetching data for page {0}...".format(page))

    url = build_url(sort, beds, page)
    response = make_request(url)

    if any(history.status_code == 302 for history in response.history):
        raise ValueError("Page number {0} does not exist".format(page))

    parser = html.fromstring(response.text)
    search_results = parser.xpath("//div[@id='search-results']//article")

    rentals = []
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

            rentals.append(rental)

    return rentals


def build_url(sort, beds, page):
    url = "https://www.zillow.com/homes/for_rent/Austin-TX"

    if sort == "newest":
        url += "/days_sort"
    elif sort == "cheapest":
        url += "/paymenta_sort"

    if beds:
        url += "/{0}-_beds".format(beds)

    url += "/{0}_p".format(page)

    return url


def make_request(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    return requests.get(url, headers=headers)

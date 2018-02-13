from lxml import html
from lxml import etree
import request


def parse_page(filters, page):
    print("Fetching data for page {0}...".format(page))

    url = build_url(filters, page)
    response = request.make_web_request(url)

    if any(history.status_code == 302 for history in response.history):
        raise PageException()

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


def get_details(rental):
    params = {
        'zws-id': 'X1-ZWz1g8owfualfv_aau4b',
        'address': rental.get('address'),
        'citystatezip': rental.get('postal_code')
    }

    response = request.make_soap_request("http://www.zillow.com/webservice/GetDeepSearchResults.htm", params)

    root = etree.XML(response.content)
    print(root.xpath('response/results/result/zpid')[0].text)
    return root


def build_url(filters, page):
    url = "https://www.zillow.com/homes/for_rent/Austin-TX"

    if filters.sort == "newest":
        url += "/days_sort"
    elif filters.sort == "cheapest":
        url += "/paymenta_sort"

    url += "/{0}-_beds".format(filters.beds)
    url += "/{0}-{1}_mp".format(filters.minrent, filters.maxrent)
    url += "/{0}-{1}_size".format(filters.minsqft, filters.maxsqft)

    url += "/{0}_p".format(page)

    return url

class PageException(Exception):
    """This page does not exist"""
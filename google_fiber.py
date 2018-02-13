import request
import re
import binascii
import json


def fiber_ready(rental):
    params = get_params(rental)

    if params:
        response = request.make_web_request('https://fiber.google.com/address/', params)

        if any(history.status_code == 302 for history in response.history):
            return True
        # or if address already has a google fiber account!

    return False


def get_params(rental):
    params = {
        'street_address': rental['address'],
        'zip_code': rental['postal_code']
    }

    response = request.make_web_request('https://fiber.google.com/address/', params)

    if any(history.status_code == 302 for history in response.history):
        return params

    preloaded_fields = re.search("gf\.preload = '(.*?)'", response.text)

    if preloaded_fields:
        preloaded_fields = re.sub("\\\\x[0-9a-fA-F]{2}", replace_hex, preloaded_fields.group(1))
        preloaded_fields = json.loads(preloaded_fields)

        try:
            address = preloaded_fields['1']['5']['2']

            new_params = {
                'street_address': address['1'],
                'unit_number': address['2'],
                'zip_code': address['5']
            }

            return new_params
        except KeyError:
            return


def replace_hex(hex_match):
    hex_match = hex_match.group()
    hex_match = re.sub('\\\\x', '', hex_match)
    return binascii.unhexlify(hex_match).decode("utf-8")

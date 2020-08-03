import requests
import cryptography


def post(endpoint, data, *a, **kw):
    encoded_json = data
    # todo: use PKE and a salt to encrypt this json
    return requests.post(endpoint, json={'data': encoded_json}, *a, **kw)

from .response import parse_response

import requests


DEFAULT_URL = 'https://wsbvw.htichina.com.cn/HTIWebGateway/'


class Endpoint(object):
    def __init__(self, transaction_id, url=None):
        self.url = url if url else DEFAULT_URL
        self.transaction_id = transaction_id

    def send(self, request):
        url = ''.join((self.url, request.endpoint))
        response = requests.post(url, request.render(self.transaction_id))
        if response.status_code != 200:
            raise Exception(
                "ERROR: Server returned an error\n"
                "Request: {} with params {}\n"
                "Response: Error {}: {}".format(
                    request.__class__.__name__, request.params,
                    response.status_code, response.content
                )
            )
        return parse_response(response)

from .endpoint import Endpoint
from .requests import (
    AuthRequest,
    StatusRequest,
    PairingRequest,
    ConfirmPairingRequest,
)

from random import choice
from string import ascii_letters, digits


def random_id():
    alphabet = ascii_letters+digits
    return ''.join(choice(alphabet) for i in range(24))


class Api(object):
    def __init__(self, account_id, pin, account_info=None,
                 transaction_id=None, url=None):
        self.account_id = account_id
        self.pin = pin
        self.account_info = account_info
        self.code = None
        if transaction_id is None:
            transaction_id = random_id()
        self.endpoint = Endpoint(transaction_id, url)

    @property
    def transaction_id(self):
        return self.endpoint.transaction_id

    @property
    def is_authenticated(self):
        return self.vin and self.tcuid

    @property
    def vin(self):
        try:
            return self.account_info['Vehicle']['VIN']
        except Exception:
            return None

    @property
    def tcuid(self):
        try:
            return self.account_info['Vehicle']['TCUID']
        except Exception:
            return None

    @property
    def transaction_id(self):
        try:
            return self.account_id['TransactionId']
        except Exception:
            return None

    def clear_authentication(self):
        self.account_info = None

    def authenticate(self):
        request = AuthRequest(self.account_id, self.pin)
        status, data = self.endpoint.send(request)
        if status != 'FAILURE':
            self.account_info = data
            if not self.is_authenticated:
                raise Exception(
                    'Unable to find VIN and TCUID in '
                    'response: {}'.format(data)
                )
            return self.account_info
        else:
            self.account_info = None
            raise Exception("Invalid credentials")

    def request_pairing(self):
        if not self.is_authenticated:
            self.authenticate()
        phone = self.account_info.get('phone')
        request = PairingRequest(self.account_id, phone)
        status, data = self.endpoint.send(request)
        return status != 'FAILURE'

    def confirm_pairing(self, code):
        request = ConfirmPairingRequest(self.account_id, self.pin, code)
        status, data = self.endpoint.send(request)
        if status != 'FAILURE':
            self.code = code
            return True
        return False

    def status(self, retry=True):
        """Get vehicle status.

        If retry=True, it will try to re-authenticate if status call
        fails due to expired authentication.
        """
        if not self.is_authenticated:
            self.authenticate()
            retry = False

        request = StatusRequest(self.account_id, self.tcuid, self.vin)
        status, data = self.endpoint.send(request)
        if status != 'Success':
            if retry:
                # Our authentication might have expired. Retry clearing
                # authentication so it will re-authenticate
                self.clear_authentication()
                return self.status()
            else:
                raise Exception('Unable to retrieve status')

        return data
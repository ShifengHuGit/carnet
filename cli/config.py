from carnet import Api

import click
import json
import os
import functools


class Config(object):
    local_vars = ('file', 'json', 'verbose', 'config', 'dirty')

    def __init__(self, file, json, verbose):
        self.file = os.path.realpath(os.path.expanduser(file))
        self.json = json
        self.verbose = verbose
        self.config = {}
        self.dirty = False
        self.read()

    def __del__(self):
        self.write()

    def __getattr__(self, item):
        try:
            return self.config[item]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        if key in self.local_vars:
            super(Config, self).__setattr__(key, value)
        else:
            self.config[key] = value
            self.dirty = True

    def __delattr__(self, item):
        del self.config[item]
        self.dirty = True

    @property
    def auth_credentials(self):
        account_id = self.config.get('account_id')
        pin = self.config.get('pin')
        if not account_id or not pin:
            return None
        return account_id, pin

    def read(self):
        try:
            with open(self.file) as fd:
                self.config = json.load(fd)
        except FileNotFoundError:
            self.config = {}
        self.dirty = False

    def write(self):
        if self.dirty:
            oldmask = os.umask(0o077)
            with open(self.file, 'w+') as fd:
                fd.write(json.dumps(self.config, sort_keys=True, indent=4))
            os.umask(oldmask)
            self.dirty = False


def api_from_config(config):
    auth_credentials = config.auth_credentials
    if auth_credentials is None:
        raise click.ClickException(
            'Unable to build Api from config: No credentials found')
    account_id, pin = auth_credentials
    info = getattr(config, 'info', None)
    transaction_id = getattr(config, 'transaction_id', None)
    return Api(account_id, pin, info, transaction_id)


pass_config = click.make_pass_decorator(Config)


def require_auth(fn):
    @functools.wraps(fn)
    def wrapper(config, *args, **kwargs):
        if config.auth_credentials is None:
            raise click.ClickException("Credentials not found. Run setup first")
        return fn(config, *args, **kwargs)
    return wrapper

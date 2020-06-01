from carnet import Api, random_id
from cli.config import (
    Config,
    pass_config,
    require_auth,
    api_from_config,
)
from cli.util import (
    print_vehicle_info,
    print_status_info,
    pretty_json,
)


import click
import sys


@click.group()
@click.option('--config-file', '-c', default='~/.carnet.cfg',
              help='Use alternative config file (default ~/.car-net.cfg).')
@click.option('--json', is_flag=True,
              help='Print json rather than pretty-print')
@click.option('--verbose', '-v', is_flag=True,
              help='Enables verbose mode.')
@click.pass_context
def main(ctx, config_file, json, verbose):
    config = Config(file=config_file, json=json, verbose=verbose)
    config.verbose = verbose
    ctx.obj = config


@main.command()
@click.option('--account-id', prompt="Account ID",
              help="The car-net account id")
@click.option('--pin', prompt="PIN",
              help="The car-net PIN")
@pass_config
def setup(config, account_id, pin):
    """Setup the initial config.

    Your account ID and PIN numbers are needed for
    authentication. They will be stored in the
    ini file for later reusage.
    """

    click.echo('Verifying credentials...', file=sys.stderr)
    api = Api(account_id, pin)
    try:
        info = api.authenticate()
    except Exception as e:
        raise click.ClickException(str(e))

    config.account_id = info['Account']['AccountInfo']['AccountID']
    config.pin = pin
    config.info = info
    config.transaction_id = api.transaction_id
    click.echo(click.style('Success!', fg='red'), file=sys.stderr)
    if config.json:
        print(pretty_json(status))
    else:
        print_vehicle_info(info)


@main.command()
@pass_config
@require_auth
def info(config):
    if config.json:
        print(pretty_json(config.info))
    else:
        print_vehicle_info(config.info)


@main.command()
@pass_config
@click.option('--details', is_flag=True,
              help="Print all details not just the summary")
@require_auth
def status(config, details):
    """Show vehicle status."""
    api = api_from_config(config)

    try:
        info = api.status(retry=False)
    except Exception:
        click.echo("Auth expired. Authenticating and retrying...",
                   file=sys.stderr)
        try:
            config.info = api.authenticate()
            info = api.status(retry=False)
        except Exception as e:
            raise click.ClickException(str(e))

    if config.json:
        print(pretty_json(info))
    else:
        click.echo(click.style('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄',fg='yellow'))
        print_vehicle_info(config.info)
        #print(info)
        print_status_info(info, details)
        click.echo(click.style('▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀',fg='yellow'))


@main.command()
@pass_config
@require_auth
def pair(config):
    """Pair to your account.

    This is still useless, but will be needed for
    certain remore commands on the vehicle.
    """
    api = api_from_config(config)

    if not api.request_pairing():
        raise click.ClickException("Unable to request pairing")
    click.echo(
        "A Pairing code has been requested to your phone."
        "Please enter it below!")

    code = click.prompt('Registration Code', type=int)

    if api.confirm_pairing(code):
        raise click.ClickException("Error pairing client")
    click.echo(click.style("Pairing sucessfull!", fg='green'))

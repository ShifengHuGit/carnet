import click
import json


def print_vehicle_info(info):
    vehicle = info.get('Vehicle')
    click.echo(
        "---- Vehicle information -------------------\n"
        "  Model: {Make} {Model} ({ModelYear})\n"
        "  Color: {ExteriorColor}\n"
        "  VIN:   {VIN}\n"
        "  TCUID: {TCUID}\n"
        "".format(**vehicle))
    click.echo(
        "---- Owner information ---------------------\n"
        "  Phone: {phone}\n"
        "  Email: {email}\n"
        "".format(**info))


def print_status_info(status, details=False):
    click.echo("---- Main Status ---------------------------")
    service_data = status.get('ServiceData')
    if service_data:
        click.echo(
            "  Mileage: {OverallMileage} Km\n"
            "".format(**service_data))
    battery = status.get('ChargingData')
    if battery and battery.get('BatteryChargeState'):
        click.echo(
            "  Battery:  {StateOfCharge}%\n"
            "  Charging: {BatteryChargeState}\n"
            "  Range:    {CruisingRange} Km\n"
            "".format(**battery))
    elif service_data:
        click.echo(
            "  Fuel:   {FuelLevel}/{FuelCapacity} L"
            "".format(**service_data))
        click.echo(
            "  Range:    {CruisingRange} Km\n"
            "".format(**battery))

    location = status.get('VehicleLocation')
    if location:
        click.echo(
            "  Location: ({Latitude}, {Longitude})\n"
            "            http://www.latlong.net/c/?lat={Latitude}&long={Longitude}\n"
            "".format(**location))

    if details:
        click.echo("---- Detailed Status -----------------------")
        click.echo(pretty_json(status))


def pretty_json(data):
    return json.dumps(data, sort_keys=True, indent=4)

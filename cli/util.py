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


def print_battery_status(info):
    plug_state = info.get('PlugConnectionState')
    charging_state = info.get('BatteryChargeState')
    remaining_charge_time = int(info.get('RemainingChargingTime'))
    charge_pct = info.get('StateOfCharge')
    battery_range = info.get('CruisingRange')

    if plug_state == 'connected' and charging_state == 'charging':
        charging_state = '{}, charging  ({}h {}m untill full)'.format(
            plug_state, remaining_charge_time//60, remaining_charge_time%60
        )
    elif plug_state == 'disconnected':
        charging_state = 'disconnected'
    else:
        charging_state = '{}, {}'.format(
            plug_state, charging_state
        )

    return "  Battery:  {}%\n  Range:    {} Km\n  Charging: {}\n".format(
        charge_pct, battery_range, charging_state)


def print_status_info(status, details=False):
    click.echo("---- Main Status ---------------------------")
    service_data = status.get('ServiceData')
    if service_data:
        click.echo(
            "  Mileage: {OverallMileage} Km\n"
            "".format(**service_data))
    battery = status.get('ChargingData')
    if battery and battery.get('BatteryChargeState'):
        click.echo(print_battery_status(battery))
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

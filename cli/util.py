import click
import json
import time
import datetime

def print_vehicle_info(info):
    Account= info.get('Account').get('AccountInfo')
    vehicle = info.get('Account').get('VehicleDetails')
    Feature = info.get('Account').get('Feature')
    click.echo(
        "------------ Vehicle information ------------\n"
        "  Model: {Make} {Model} ({ModelYear})\n"
        "  Color: {Color}\n"
	"  LicensePlate: {VehicleLicensePlate}\n"
	"  Platform: {DeviceType}\n"
        "".format(**vehicle))
    click.echo(
	"------------ Account Information-------------\n"
	"AccountID: {AccountID}\n"
   	"Subscription: {CreateTimestamp}\n"
    	"VIN: {VIN}\n"
    	"TCUID: {TCUID}\n"
	"".format(**Account)) 


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
    click.echo(click.style('---------- Main Information -----------',fg='yellow'))
    service_data = status.get('ServiceData')
    if service_data:
        click.echo(
            "  Mileage/总里程: {OverallMileage} Km\n"
            "".format(**service_data))
    battery = status.get('ChargingData')
    if battery and battery.get('BatteryChargeState'):
        click.echo(print_battery_status(battery))
    elif service_data:
        click.echo(
            "  Fuel/燃油:   {FuelLevel}/{FuelCapacity} L"
            "".format(**service_data))
        click.echo(
            "  Range/续航:    {CruisingRange} Km\n"
            "".format(**battery))
        Temp = float(status.get('ClimatisationData').get('OutTemp').get('measurementValue'))
        Temp = Temp/10-273.15
        click.echo(
            "  Outside Temperature/车外温度: %.2f °C \n" % Temp )

    location = status.get('VehicleLocation')
    if location:
        click.echo(
            "  Location/坐标: ({Latitude}, {Longitude})\n"
            "  Altitude/海拔: {Altitude}m  \n"
            "  Course/航向：{Course} \n"
            "            http://www.latlong.net/c/?lat={Latitude}&long={Longitude}\n"
            "".format(**location))

    if details:
        click.echo(click.style('---------- Detailed Status -----------',fg='yellow'))
        #click.echo(pretty_json(status))
        print_vehicle_Detail(status)

def print_vehicle_Detail(info):
    UpdateTime = info.get('UnifiedStatusTimestamp')
    click.echo('Last Updated: %s' %  UpdateTime)
    click.echo(click.style('-----------Doors------------',fg='blue'))
    for Door in info.get('DoorState'):
        click.echo( "%s: \t\t%s" % (Door.get('DoorId'), Door.get('DoorStatus')))
    click.echo(click.style('----------Windows-----------', fg='red'))
    for Window in info.get('WindowState'):
        click.echo( "%s: \t\t%s" % (Window.get('WindowId'), Window.get('WindowStatus')))

def pretty_json(data):
    return json.dumps(data, sort_keys=True, indent=4)

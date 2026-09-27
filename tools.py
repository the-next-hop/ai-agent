import netmiko
import os
import json
from netmiko import ConnectHandler


def obtain_credentials():
    username = os.environ["ARISTA_USERNAME"]
    password = os.environ["ARISTA_PASSWORD"]

    return username, password

def get_single_device_addr(host):
    DEVICES = {
        "SW1" : "10.0.101.11",
        "SW2" : "10.0.101.12",
    }

    return DEVICES[host]

def get_all_devices():
    DEVICES = {
        "SW1" : "10.0.101.11",
        "SW2" : "10.0.101.12",
        "SW3" : "10.0.101.13",
        "SW4" : "10.0.101.14",
        "SW5" : "10.0.101.15",
        "SW6" : "10.0.101.16",
        "SW7" : "10.0.101.17",
        "SW8" : "10.0.101.18",
    }

    return json.dumps(DEVICES)

def run_show_command(host, command):

    username, password = obtain_credentials()

    ip = get_single_device_addr(host)

    net_connect = ConnectHandler(
        device_type="arista_eos",
        host=ip,
        username=username,
        password=password,
    )

    output = net_connect.send_command(
        command
    )

    net_connect.disconnect()

    return output

def run_set_command(host, command):

    username, password = obtain_credentials()

    ip = get_single_device_addr(host)

    net_connect = ConnectHandler(
        device_type="arista_eos",
        host=ip,
        username=username,
        password=password,
    )

    output = net_connect.send_config_set(
        command
    )

    net_connect.disconnect()

    return output

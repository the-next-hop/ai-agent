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

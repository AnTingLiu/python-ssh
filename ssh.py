#!/usr/bin/env python3
import netmiko
import yaml
from pprint import pprint
from copy import deepcopy

SITE_NAME = 'HQ'
COMMANDS_LIST = [
    "show clock",
    "show version",
    "show inventory",
    "show ip interface brief"
                              ]

def read_yaml(path='inventory.yml'):
    with open(path) as file:
        yaml_content = yaml.load(file.read())
    return yaml_content

def form_connection_params_from_yaml(parsed_yaml, site='all'):
    """
        Form dictionary of netmiko connections parameters for all devices on the site
        Args:
            parsed_yaml (dict): dictionary with parsed yaml file
            site (str): name of the site. Default is 'all'
        Returns:
            dict: key is hostname, value is dictionary containing
                netmiko connection parameters for the host
        """
    parsed_yaml = deepcopy(parsed_yaml)
    result = {}
    global_params = parsed_yaml["all"]["vars"]
    site_dict = parsed_yaml["all"]["groups"].get(site)
    if site_dict is None:
       raise KeyError(
    "Site {} is not specified in inventory YAML file".format(site))
    for host in site_dict["hosts"]:
            host_dict = {}
            hostname = host.pop("hostname")
            host_dict.update(global_params)
            host_dict.update(host)
            result[hostname] = host_dict
    return result


def collect_ouput(devices, commands):
    """
    Collects commands from the dictionary of devices
    Args:
        devices (dict): dictionary, where key is the hostname, value is
            netmiko connection dictionary
        commands (list): list of commands to be executed on every device
    Returns:
        dict: key is the hostname, value is string with all outputs
    """
    for device in devices:
        hostname = device.pop("hostname")
        connection = netmiko.ConnectHandler(**device)
        device_result = ["{0} {1} {0}".format("=" * 20, hostname)]

        for command in commands:
            command_result = connection.send_command(command)
            device_result.append("{0} {1} {0}".format("=" * 20, command))
            device_result.append(command_result)

        device_result_string = "\n\n".join(device_result)
        connection.disconnect()
        yield device_result_string


# call def function
def main():
    parsed_yaml = read_yaml()
    connection_params = form_connection_params_from_yaml(parsed_yaml,site = SITE_NAME)
    pprint(connection_params)


if __name__ == "__main__":
    main()

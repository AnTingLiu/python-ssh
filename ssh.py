#!/usr/bin/env python3
import netmiko
import yaml

def read_yaml(path='inventory.yml'):
    with open(path) as file:
        yaml_content = yaml.load(file.read())
    return yaml_content

def main():
    print(read_yaml())



if __name__ == "__main__":
    main()
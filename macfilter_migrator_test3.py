import argparse
import ast
import yaml
import re
from netmiko import ConnectHandler

parser = argparse.ArgumentParser(description='Send command to cisco device.')
parser.add_argument('infile', metavar='input file', type=str, nargs=1, help='list of device ip addresses')

args = parser.parse_args()
infile = args.infile[0]

mac_list = []
mac_pattern = r'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]'
with open(infile) as f:
    device_list = []
    for device in (yaml.load(f)):
        device_list.append(device)

def get_mac_list(mac_list):
    for x in device_list:
        net_connect = ConnectHandler(**x)
        raw_output = net_connect.send_command('show macfilter summary')
        output_lines = raw_output.split('\n')
        for line in output_lines:
            matched = re.search(mac_pattern, line)
            if matched:
                matched_new = matched.group()
                mac_list.append(matched_new)
    return mac_list

get_mac_list(mac_list)


w_pat = "WLAN"
i_pat = "Interface"
d_pat = "Description"

mac_entry_list = []

for x in device_list:
    net_connect = ConnectHandler(**x)
    for mac in mac_list:
        command = "show macfilter detail " + mac  ###defined differently than in previous function line 23
        raw_output = net_connect.send_command(command)
        output_lines = raw_output.split('\n')






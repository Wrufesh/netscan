import glob
import netifaces
import os
import re
import subprocess

from celery.events.state import State

from netscan.celery import app
from netscan.settings import AIRODUMP_CSV_ROOT
from netscan.utils.connected_host_detail import Netscan


def get_network_interface_list():
    return netifaces.interfaces()


def get_connected_interface_name():
    try:
        return netifaces.gateways()['default'][netifaces.AF_INET][1]
    except KeyError:
        return None


def get_connected_network_detail():
    if get_connected_interface_name():
        addrs = netifaces.ifaddresses(get_connected_interface_name())

        return addrs[netifaces.AF_INET]
    else:
        return None


def get_connected_hosts_detail():
    netscan = Netscan()
    if get_connected_interface_name():
        w = netscan.parser("ifconfig")
        x = netscan.getIpMask(w)
        output_list = netscan.parser("nmap", "-O", x[1])
        if not isinstance(output_list, list):
            return output_list
        else:
            return netscan.scanResult(output_list)


def get_monitor_interface_name(line):
    m = re.search('on.\[.+\].+\)\\n', line)
    if m:
        name = m.group(0).split(']')[1].split(')')[0]
        return name
    else:
        return None


def turn_on_monitor_mode(interface):
    cmd = subprocess.Popen(
        'airmon-ng start %s' % interface,
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    output_list = []
    for line in cmd.stdout:
        if line.startswith('\t\t(') and 'enabled' in line:
            monitor_interface_name = get_monitor_interface_name(line)
            if monitor_interface_name:
                return (True, monitor_interface_name)
            else:
                break
    return (False, None)


def has_airodumps():
    for dirpath, dirnames, files in os.walk(AIRODUMP_CSV_ROOT):
        if files:
            return True
        if not files:
            return False


def kill_airodump_proc():
    app.control.revoke([
        uuid
        for uuid, _ in
        State().tasks_by_type('start_airodump')
    ])

    import os, shutil
    folder = AIRODUMP_CSV_ROOT
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

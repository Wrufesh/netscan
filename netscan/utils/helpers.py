import netifaces

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

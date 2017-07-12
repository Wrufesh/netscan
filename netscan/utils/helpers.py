import netifaces


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

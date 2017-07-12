from django.shortcuts import render

# Create your views here.
from netscan.utils.helpers import get_connected_interface_name, get_connected_network_detail, \
    get_network_interface_list, get_connected_hosts_detail


def index(request):
    context = dict()
    if get_connected_interface_name():
        context["connection_detail"] = get_connected_network_detail()

    return render(request, 'index.html', context)


def interface_list_view(request):
    context = dict()
    context["object_list"] = [(True, interface) if interface.startswith('wl') else (False, interface) for interface in
                              get_network_interface_list()]
    return render(request, 'interface_list.html', context)


def connected_hosts(request):
    context = dict()
    hosts_detail = get_connected_hosts_detail()

    if isinstance(hosts_detail, list):
        context['connected_hosts'] = hosts_detail
    else:
        context['error_message'] = hosts_detail

    return render(request, 'connected_hosts.html', context)


def scan_for_rouge(request, interface):
    context = dict()
    context['sample_to_remove'] = interface
    return render(request, 'rouge.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from netscan.utils.helpers import get_connected_interface_name, get_connected_network_detail, \
    get_network_interface_list, get_connected_hosts_detail, turn_on_monitor_mode, kill_airodump_proc, has_airodumps
from netutil.tasks import start_airodump

interface_model = {
    'interfaces': [],
    # interfaces list example
    # {
    #     'name': '',
    #     'monitor_mode':
    # }
}


def index(request):
    context = dict()
    if get_connected_interface_name():
        context["connection_detail"] = get_connected_network_detail()

    return render(request, 'index.html', context)


def kill_airodumps(request):
    kill_airodump_proc()
    return redirect('interface-list')


def interface_list_view(request):
    context = dict()
    context['has_airodumps'] = has_airodumps()
    context["object_list"] = [(True, interface) if interface.startswith('w') else (False, interface) for interface in
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
    if turn_on_monitor_mode(interface)[0]:
        start_airodump.delay(turn_on_monitor_mode(interface)[1])
        return redirect('start-monitor', monitor_interface=turn_on_monitor_mode(interface)[1])
    else:
        messages.info(
            request,
            "Monitor mode not supported for the interface '%s'" % interface
        )
        return redirect('interface-list')


def start_monitor(request, monitor_interface):
    context = dict()
    return render(request, 'rouge.html', context)

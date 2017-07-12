from django.shortcuts import render

# Create your views here.
from netscan.utils.helpers import get_connected_interface_name, get_connected_network_detail, get_network_interface_list


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

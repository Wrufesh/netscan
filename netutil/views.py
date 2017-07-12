from django.shortcuts import render


# Create your views here.
from netscan.utils.helpers import get_connected_interface_name, get_connected_network_detail


def index(request):
    # get connection info and list two options

    context = dict()
    # import ipdb
    # ipdb.set_trace()
    if get_connected_interface_name():
        context["connection_detail"] = get_connected_network_detail()


    return render(request, 'index.html', context)


def interface_list_view(request):
    return render(request, 'interface_list.html.html', {})

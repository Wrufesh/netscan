from django.shortcuts import render


# Create your views here.
def index(request):
    # get connection info and list two options
    return render(request, 'index.html', {})

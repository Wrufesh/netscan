"""eclassroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from netutil.views import index, interface_list_view, connected_hosts, scan_for_rouge, kill_airodumps

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='home'),
    url(r'^kill-airodumps$', kill_airodumps, name='kill-airodumps'),
    url(r'^interfaces$', interface_list_view, name='interface-list'),
    url(r'^network-hosts$', connected_hosts, name='connected-hosts'),
    url(r'^evil-twin/(?P<interface>[\w-]+)/$', scan_for_rouge, name='evil-twin'),
    url(r'^start-monitor/(?P<monitor_interface>[\w-]+)/$', scan_for_rouge, name='start-monitor')
    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the CustomerListView
    url(
        regex=r'^$',
        view=views.CustomerListView.as_view(),
        name='list'
    ),
    # URL pattern for the CustomerCreateView
    url(
        regex=r'^create/$',
        view=views.CustomerCreateView.as_view(),
        name='create'
    ),
    # URL pattern for the CustomerUpdateView
    url(
        regex=r'^(?P<pk>[\w.@+-]+)/update/$',
        view=views.CustomerUpdateView.as_view(),
        name='update'
    ),
    # URL pattern for the CustomerDeleteView
    url(
        regex=r'^(?P<pk>[\w.@+-]+)/delete/$',
        view=views.CustomerDeleteView.as_view(),
        name='delete'
    ),
    # URL pattern for the CustomerDetailView
    url(
        regex=r'^(?P<pk>[\w.@+-]+)/$',
        view=views.CustomerDetailView.as_view(),
        name='detail'
    )
]

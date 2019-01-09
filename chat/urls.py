from django.urls import path, re_path
#from django.conf.urls import url

from .views import bview

app_name ='bot_webhooks'

urlpatterns = [
    re_path(r'^<webhook_endpoint>/$', bview.as_view(), name = 'webhook'),

]







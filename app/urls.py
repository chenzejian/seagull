from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^send_email', views.send_email),
]
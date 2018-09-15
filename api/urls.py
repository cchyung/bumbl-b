from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^process', views.process),
    url(r'^get-snippets', views.get_more_snippets)
]
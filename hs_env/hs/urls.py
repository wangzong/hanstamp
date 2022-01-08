from django.urls import path

from . import views

app_name = 'hs'


urlpatterns = [
    path('', views.index, name='index'),
    path('hanzi/<str:char>', views.hanzis, name='hanzi'),
    path('search/', views.search, name='search'),
]
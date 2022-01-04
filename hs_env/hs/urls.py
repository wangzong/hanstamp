from django.urls import path

from . import views

app_name = 'hs'

urlpatterns = [
    path('', views.index, name='index'),
    path('hanzi/', views.hanzi, name='hanzi'),
]
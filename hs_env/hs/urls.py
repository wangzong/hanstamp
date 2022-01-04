from django.urls import path

from . import views

app_name = 'hs'

urlpatterns = [
    path('', views.index, name='index'),
    # path('new_hanzi/', views.new_hanzi, name='new_hanzi'),
]
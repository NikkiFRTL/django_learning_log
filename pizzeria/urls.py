"""
Определяет схемы URL для pizzeria
"""

from django.urls import path
from . import views


app_name = 'pizzeria'
urlpatterns = [
    # Домашняя страница
    path('', views.pizza_index, name='pizza_index'),
]

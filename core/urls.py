from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),
]
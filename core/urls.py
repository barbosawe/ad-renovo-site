from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),
    path('galeria-kids/', views.galeria_kids, name='galeria_kids'),
    path('galeria-jovens/', views.galeria_jovens, name='galeria_jovens'),
    path('galeria-circulo/', views.galeria_circulo, name='galeria_circulo'),
    path('galeria-music/', views.galeria_music, name='galeria_music'),
]
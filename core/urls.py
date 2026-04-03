from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),
    path('galeria-kids/', views.galeria_kids, name='galeria_kids'),
    path('galeria-jovens/', views.galeria_jovens, name='galeria_jovens'),
    path('galeria-circulo/', views.galeria_circulo, name='galeria_circulo'),
    path('galeria-music/', views.galeria_music, name='galeria_music'),
    path('college/cadastro/', views.college_cadastro, name='college_cadastro'),
    path('college/', views.college_login, name='college_login'),
    path('college/logout/', views.college_logout, name='college_logout'),
    path('college/dashboard/', views.college_dashboard, name='college_dashboard'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
]
from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    path('', views.home, name='home'),
    path('citas/', views.citas, name='citas'),
    path('citas/reservar/<int:medico_id>/', views.reservar, name='reservar'),
]
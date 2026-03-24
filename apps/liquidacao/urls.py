from django.urls import path
from . import views

app_name = 'liquidacao'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_data, name='api'),
    path('exportar/csv/', views.export_csv, name='export_csv'),
]

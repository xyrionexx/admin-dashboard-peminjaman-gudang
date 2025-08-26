from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_barang, name='get_barang'),
    path('delete/<int:id>/', views.delete_barang, name='delete_barang'),
]

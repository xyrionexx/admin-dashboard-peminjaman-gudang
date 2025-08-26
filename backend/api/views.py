from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Barang
from .serializers import BarangSerializer

class BarangViewSet(viewsets.ModelViewSet):
    queryset = Barang.objects.all()
    serializer_class = BarangSerializer

# barang/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Barang
from .models import Barang
from .serializers import BarangSerializer

@api_view(['GET'])
def get_barang(request):
    barang = Barang.objects.all()
    serializer = BarangSerializer(barang, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_barang(request, id):
    try:
        barang = Barang.objects.get(pk=id)
        barang.delete()
        return JsonResponse({'message': 'Barang berhasil dihapus'}, status=200)
    except Barang.DoesNotExist:
        return JsonResponse({'error': 'Barang tidak ditemukan'}, status=404)
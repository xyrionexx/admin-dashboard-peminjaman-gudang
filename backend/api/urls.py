from rest_framework import routers
from .views import BarangViewSet

router = routers.DefaultRouter()
router.register(r'barang', BarangViewSet)

urlpatterns = router.urls
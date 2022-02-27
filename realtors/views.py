from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Realtor
from .serializers import RealtorSerializer

class RealtorListView(ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer
    pagination_class = None

class RealtorView(RetrieveAPIView):
    # permission_classes = [AllowAny, ]
    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer

class TopSellerView(ListAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = Realtor.objects.filter(top_seller__in=[True])
    serializer_class = RealtorSerializer
    pagination_class = None
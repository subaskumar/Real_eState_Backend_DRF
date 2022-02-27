from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.parsers import FormParser,MultiPartParser
from .models import Listing
from .serializers import ListingSerializer, listingDetailSerializer,ListingAddSerializer
from datetime import datetime, timezone, timedelta
from django.db.models import Q
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings

class ListingsView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Listing.objects.order_by('-list_date')
    serializer_class = ListingSerializer

class ListingView(RetrieveAPIView):
    # defaut permission class is IsAuthenticated
    permission_classes = [AllowAny, ]
    queryset = Listing.objects.order_by('-list_date')
    serializer_class = listingDetailSerializer
    lookup_field = 'slug'
      
class AddListingView(CreateAPIView):
    # parser_classes = [MultiPartParser,FormParser]
    permission_classes = [AllowAny]
    serializer_class = ListingAddSerializer
    
    
    def create(self,request,*args, **kwargs):
        print(request.data)
        serializer = ListingAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

class SearchView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ListingSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def list(self, request, format=None):
        queryset = Listing.objects.order_by('-list_date')
        data = request.query_params
        sale_type = data.get('sale_type')
        home_type = data.get('home_type')
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        sqft = data.get('sqft')
        bedrooms = data.get('bedrooms')
        keywords = data.get('keywords')
        print(home_type,min_price,max_price,sqft,keywords,bedrooms,sale_type)
        
        multi_query = Q(Q(sale_type__iexact=sale_type) & Q(home_type__iexact=home_type)
                &  Q(bedrooms__gte = bedrooms) & Q(sqft__gte=sqft))
        
        queryset =  queryset.filter(multi_query)
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListingSerializer(page,context= {'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        # # sqft = data['sqft']  # if we not provide any value it will raise MultiValueDictKeyError(key) Error. it's pymongo problem
    
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
         """
         Return a single page of results, or `None` if pagination is disabled.
         """
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
         """
         Return a paginated style `Response` object for the given output data.
         """
         assert self.paginator is not None
         return self.paginator.get_paginated_response(data) 



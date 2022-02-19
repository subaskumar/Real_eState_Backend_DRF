from rest_framework import serializers
from .models import Listing
from datetime import datetime, timezone
from realtors.serializers import RealtorSerializer

class ListingSerializer(serializers.ModelSerializer):
    past_time = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        fields = ('id','title', 'zipcode','address', 'city', 'state', 'price','past_time', 'sale_type', 'home_type','description', 'bedrooms', 'bathrooms', 'sqft', 'photo_main', 'slug')
        lookup_field = 'slug'
        
    def get_past_time(self,obj):
        
        time = datetime.now()
        if obj.list_date.day == time.day:
            return str(time.hour - obj.list_date.hour) + " hours ago"
        else:
            if obj.list_date.month == time.month:
                return str(time.day - obj.list_date.day) + " days ago"
            else:
                if obj.list_date.year == time.year:
                    return str(time.month - obj.list_date.month) + " months ago"
        return obj.list_date
    
class listingDetailSerializer(serializers.ModelSerializer):
    # realtor = serializers.StringRelatedField()
    class Meta:
        model = Listing
        fields = '__all__'
        
    def to_representation(self, instance):          # here we override this method and instance is player class instance
        rep = super().to_representation(instance)   # it returns data of Player instance
        Realtor_details = RealtorSerializer(instance.realtor).data
        rep["realtor"] = Realtor_details
        return rep
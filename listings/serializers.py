from rest_framework import serializers
from .models import Listing
from datetime import datetime, timezone
from realtors.serializers import RealtorSerializer

# from rest_framework import serializers    

# class Base64ImageField(serializers.ImageField):

#     def to_internal_value(self, data):
#         from django.core.files.base import ContentFile
#         import base64
#         import six
#         import uuid

#         if isinstance(data, six.string_types):
#             if 'data:' in data and ';base64,' in data:
#                 header, data = data.split(';base64,')

#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('invalid_image')

#             file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#             file_extension = self.get_file_extension(file_name, decoded_file)

#             complete_file_name = "%s.%s" % (file_name, file_extension, )

#             data = ContentFile(decoded_file, name=complete_file_name)

#         return super(Base64ImageField, self).to_internal_value(data)

#     def get_file_extension(self, file_name, decoded_file):
#         import imghdr

#         extension = imghdr.what(file_name, decoded_file)
#         extension = "jpg" if extension == "jpeg" else extension

#         return extension

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
        
    def to_representation(self, instance):          # here we override this method and instance is Listing class instance
        rep = super().to_representation(instance)   # it returns data of Listing instance
        Realtor_details = RealtorSerializer(instance.realtor).data
        rep["realtor"] = Realtor_details
        return rep
    
class ListingAddSerializer(serializers.ModelSerializer):
    # photo_main = Base64ImageField(max_length=None, use_url=True,)
    class Meta:
        model = Listing
        fields = '__all__'
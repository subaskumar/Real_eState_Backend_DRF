from rest_framework import serializers
from .models import UserAccount
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from collections import OrderedDict

        
def validate_password(value):
    if len(value)< 6 :
        raise serializers.ValidationError("Password must be contain 6 characters.")
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAccount
        fields = ('email', 'password', 'password2', 'name',)

    def validate(self, data):
        email = data['email']
        query = UserAccount.objects.filter(email__iexact = email)
        if query.exists():
            raise serializers.ValidationError({"email": "That Email is already taken. Please choose another!"})
        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return data

    def create(self, validated_data):
        user = UserAccount.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        result = OrderedDict()
        result['data'] = data
        result['message'] = 'User Created sucessfully'
        result['status'] = 'sucssed'
        return result
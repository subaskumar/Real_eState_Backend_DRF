from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from rest_framework import status


class SignupView(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # or we can write direct serializer class
        # serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # self.perform_create(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)  # it return error code with status 200
        
            # headers = self.get_success_headers(serializer.data)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST, headers=headers)
            # if we return error with status code , the field vaidation error will not send to frontend,
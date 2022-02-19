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
            return Response(serializer.errors)
            # headers = self.get_success_headers(serializer.data)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST, headers=headers)
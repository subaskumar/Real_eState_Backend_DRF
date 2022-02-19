from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import Contact
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

class ContactCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        data = self.request.data
        print(data)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        tourDate = data.get('TourDate')
        agetEmail = data.get('AgentEmail')
        msg = data.get('message')
        try:
            subject = 'Request for Tour: {} '.format(name)
            message = 'Name: {} \nEmail: {} \nPhone: {} \nTour Date: {} \n\nMessage: {}\n'.format(name,
                        email,phone,tourDate,msg)            
            send_mail(subject, message, 'from_email', [agetEmail])
            
            contact = Contact(name = name, email = email, subject = subject, message = message)
            contact.save()

            return Response({'success': 'Message sent successfully'})

        except:
            return Response({'error': 'Message failed to send'})
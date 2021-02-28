from rest_framework import generics, permissions
from rest_framework import response, status
from knox.models import AuthToken
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .serializers import *
from django.conf import settings 
from django.core.mail import send_mail


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    required_permissions = {"POST":()}
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        subject = 'Welcome to credify'
        message = 'Hello '+user.name+' ,thank you for using credify. Manage your cloud certifications using credify'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [user.email] 
        send_mail( subject, message, email_from, recipient_list ) 
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
})

# class AdminLoginAPIView(generics.GenericAPIView):
#     serializer_class = AdminLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return response.Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
# })
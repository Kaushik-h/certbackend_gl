from rest_framework import generics, permissions,views
from rest_framework import response, status
from knox.models import AuthToken
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .serializers import *
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()


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
        # subject = 'Welcome to credify'
        # message = 'Hello '+user.name+' ,thank you for using credify. Manage your cloud certifications using credify'
        # email_from = settings.EMAIL_HOST_USER 
        # recipient_list = [user.email] 
        # send_mail( subject, message, email_from, recipient_list ) 
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

class ChangepasswordAPIView(views.APIView):
    http_method_names=['post']
    def post(self, request, *args, **kwargs):
        try:
            user=User.objects.get(email=request.data.get("email"))
            user.set_password(request.data.get("password"))
            user.save()
            return response.Response("Password updated",status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(str(e),status=status.HTTP_400_BAD_REQUEST)
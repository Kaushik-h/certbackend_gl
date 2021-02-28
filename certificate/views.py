from django.shortcuts import render,get_object_or_404
from .upload import Upload
from rest_framework import generics, views, permissions ,response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import *
from accounts.serializers import UserSerializer
from django.conf import settings 
from django.core.mail import send_mail

class CertificateView(views.APIView):
	permission_classes = [permissions.IsAuthenticated,]
	http_method_names=['get','post']
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	def get(self, request, *args, **kwargs): 
		try:
			user=self.request.user
			queryset=Certificates.objects.filter(user=user)
			serializer=CertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

	def post(self, request, *args, **kwargs): 
		# try:
			user=self.request.user	
			request.data["user"]=user.id
			pdf=request.FILES['pdf']
			pdf_name=user.name+request.data.get("certid")+'.pdf'
			a=Upload.upload_pdf(pdf, pdf_name)
			request.data["pdf_url"]='https://storage.googleapis.com/certificate_pdf/pdf/'+pdf_name
			serializer = CertificateSerializer(data=request.data)
			if serializer.is_valid():
				certificate = serializer.save()
				subject = 'New certificate uploaded' 
				message = 'Hello '+user.name+' , You have uploaded your '+certificate.csp+' '+certificate.certname+' certification in Credify'
				email_from = settings.EMAIL_HOST_USER 
				recipient_list = [user.email] 
				send_mail( subject, message, email_from, recipient_list ) 
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		# except Exception as e:
			# return response.Response(str(e))

class AllUsersView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['get']
	def get(self, request, *args, **kwargs): 
		try:
			queryset=User.objects.filter(user_type='nuser')
			serializer=UserSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AllUsersCertificateView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			user = User.objects.get(empid=request.data.get("empid"))
			queryset=Certificates.objects.filter(user=user)
			serializer=CertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AdminSendMailView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			user = User.objects.get(empid=request.data.get("empid"))
			subject = 'Crefidy admin' 
			message = request.data.get('msg')
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [user.email] 
			send_mail( subject, message, email_from, recipient_list ) 
			return response.Response("Mail sent",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))
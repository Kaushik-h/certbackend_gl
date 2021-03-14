from django.shortcuts import render,get_object_or_404
from .upload import Upload
from rest_framework import generics, views, permissions ,response, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import *
from accounts.serializers import UserSerializer
from django.conf import settings 
from django.core.mail import send_mail
from datetime import date,timedelta

class CertificateView(views.APIView):
	permission_classes = [permissions.IsAuthenticated,]
	http_method_names=['get','post']
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	def get(self, request, *args, **kwargs): 
		try:
			user=self.request.user
			queryset=Certificates.objects.filter(user=user)
			serializer=GetCertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

	def post(self, request, *args, **kwargs): 
		# try:
			user=self.request.user	
			request.data["user"]=user.id
			pdf=request.FILES['pdf']
			pdf_name=user.email+request.data.get("certid")+'.pdf'
			a=Upload.upload_pdf(pdf, pdf_name)
			request.data["pdf_url"]='https://storage.googleapis.com/certificate_pdf/pdf/'+pdf_name
			serializer = CertificateSerializer(data=request.data)
			if serializer.is_valid():
				certificate = serializer.save()
				# subject = 'New certificate uploaded' 
				# message = 'Hello '+user.name+' , You have uploaded your '+certificate.csp+' '+certificate.certname+' certification in Credify'
				# email_from = settings.EMAIL_HOST_USER 
				# recipient_list = [user.email] 
				# send_mail( subject, message, email_from, recipient_list ) 
				return response.Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		# except Exception as e:
			# return response.Response(str(e))

class AllUsersView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			queryset=User.objects.filter(user_type='nuser').filter(id__in=request.data.get('userids'))
			serializer=UserSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AllUsersCertificateView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			filters = {
 				key: value
    			for key, value in request.data.items()
			}
			queryset=Certificates.objects.filter(**filters)
			serializer=GetCertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class ExpiringCertificateView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			days=request.data.get("days")
			exp_date=date.today()+timedelta(days=days)
			queryset=Certificates.objects.filter(expiry_date__lte=exp_date).filter(expiry_date__gte=date.today())
			serializer=GetCertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class ExpiredCertificateView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['get']
	def get(self, request, *args, **kwargs): 
		try:
			queryset=Certificates.objects.filter(expiry_date__lte=date.today())
			serializer=GetCertificateSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AdminSendMailView(views.APIView):
	permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post','delete']
	def post(self, request, *args, **kwargs): 
		try:
			certs = Certificates.objects.filter(id__in=request.data.get("certids")).select_related('user')
			for cert in certs:
				exp = cert.expiry_date-date.today()
				subject = 'Crefidy admin' 
				message = 'Hello '+cert.user.name+' , Your '+cert.csp+' '+cert.certname+' certification is expiring '+str(exp.days+1)+' days'
				email_from = settings.EMAIL_HOST_USER 
				recipient_list = [cert.user.email] 
				print(cert,message,recipient_list)
				send_mail( subject, message, email_from, recipient_list ) 
			return response.Response("Mail sent",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

	def delete(self, request, *args, **kwargs):
		try:
			if request.data.get('certid') is not None:
				Certificates.objects.get(id=request.data.get('certid')).delete()
			if request.data.get('userid') is not None:
				User.objects.get(id=request.data.get('userid')).delete()
			return response.Response("Deleted",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))
		
class AdminHome(views.APIView):
	permission_classes = [permissions.IsAdminUser]
	http_method_names=['post']
	def post(self,request,*args,**kwargs):
		try:
			sbu=request.data.get("sbu")
			data={}

			if sbu==None:
				data["users_count"]=list(User.objects.filter(user_type='nuser').values_list('id',flat=True))
				certs=Certificates.objects.all()
				data["certificates_count"]=certs.count()
			else:
				data["users_count"]=set(Certificates.objects.filter(sbu=sbu).values_list('user',flat=True))
				certs=Certificates.objects.filter(sbu=sbu)
				data["certificates_count"]=certs.count()

			GCP={}
			GCP["GCP_count"]=certs.filter(csp="GCP").count()

			GCP_associate={}
			GCP_associate["GCP_associate_count"]=certs.filter(csp="GCP",level="Associate").count()
			GCP_associate_certs={}
			GCP_associate_certs["GCP_associatecloudengineer"]=certs.filter(csp="GCP",level="Associate",certname="Associate Cloud Engineer").count()
			GCP_associate["GCP_associate_certs"]=GCP_associate_certs

			GCP_professional={}
			GCP_professional["GCP_professional_count"]=certs.filter(csp="GCP",level="Professional").count()
			GCP_professional_certs={}
			GCP_professional_certs["GCP_professionalcloudarchitect"]=certs.filter(csp="GCP",level="Professional",certname="Professional Cloud Architect").count()
			GCP_professional_certs["GCP_professionalclouddeveloper"]=certs.filter(csp="GCP",level="Professional",certname="Professional Cloud Developer").count()
			GCP_professional_certs["GCP_professionaldataengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Data Engineer").count()
			GCP_professional_certs["GCP_professionalclouddevopsengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Cloud DevOps Engineer").count()
			GCP_professional_certs["GCP_professionalcloudsecurityengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Cloud Security Engineer").count()
			GCP_professional_certs["GCP_professionalcloudnetworkengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Cloud Network Engineer").count()
			GCP_professional_certs["GCP_professionalcollaborationengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Collaboration Engineer").count()
			GCP_professional_certs["GCP_professionalmachinelearningengineer"]=certs.filter(csp="GCP",level="Professional",certname="Professional Machine Learning Engineer").count()
			GCP_professional["GCP_professional_certs"]=GCP_professional_certs

			GCP["GCP_assocaite"]=GCP_associate
			GCP["GCP_professional"]=GCP_professional

			data["GCP"]=GCP

			AWS={}
			AWS["AWS_count"]=certs.filter(csp="AWS").count()

			AWS_foundational={}
			AWS_foundational["AWS_foundational_count"]=certs.filter(csp="AWS",level="Foundational").count()
			AWS_foundational_certs={}
			AWS_foundational_certs["AWS_AWScertifiedcloudpractitioner"]=certs.filter(csp="AWS",level="Foundational",certname="AWS Certified Cloud Practitioner").count()
			AWS_foundational["AWS_foundational_certs"]=AWS_foundational_certs

			AWS_associate={}
			AWS_associate["AWS_associate_count"]=certs.filter(csp="AWS",level="Associate").count()
			AWS_associate_certs={}
			AWS_associate_certs["AWS_AWScertifieddeveloper"]=certs.filter(csp="AWS",level="Associate",certname="AWS Certified Developer").count()
			AWS_associate_certs["AWS_AWScertifiedsysopsadministrator"]=certs.filter(csp="AWS",level="Associate",certname="AWS Certified SysOps Administrator").count()
			AWS_associate_certs["AWS_AWScertifiedsolutionsarchitect"]=certs.filter(csp="AWS",level="Associate",certname="AWS Certified Solutions Architect").count()
			AWS_associate["AWS_associate_certs"]=AWS_associate_certs

			AWS_professional={}
			AWS_professional["AWS_professional_count"]=certs.filter(csp="AWS",level="Professional").count()
			AWS_professional_certs={}
			AWS_professional_certs["AWS_AWScertifieddevopsengineer"]=certs.filter(csp="AWS",level="Professional",certname="AWS Certified DevOps Engineer").count()
			AWS_professional_certs["AWS_AWScertifiedsolutionsarchitect"]=certs.filter(csp="AWS",level="Professional",certname="AWS Certified Solutions Architect").count()
			AWS_professional["AWS_professional_certs"]=AWS_professional_certs

			AWS_specialty={}
			AWS_specialty["AWS_speciality_count"]=certs.filter(csp="AWS",level="Specialty").count()
			AWS_specialty_certs={}
			AWS_specialty_certs["AWS_AWScertifiedadvancednetworking"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Advanced Networking").count()
			AWS_specialty_certs["AWS_AWScertifiedsecurity"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Security").count()
			AWS_specialty_certs["AWS_AWScertifiedmachinelearning"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Machine Learning").count()
			AWS_specialty_certs["AWS_AWScertifieddatabase"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Database").count()
			AWS_specialty_certs["AWS_AWScertifieddataanalytics"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Data Analytics").count()
			AWS_specialty_certs["AWS_AWScertifiedalexaskillbuilder"]=certs.filter(csp="AWS",level="Specialty",certname="AWS Certified Alexa Skill Builder").count()
			AWS_specialty["AWS_speciality_certs"]=AWS_specialty_certs

			AWS["AWS_foundational"]=AWS_foundational
			AWS["AWS_associate"]=AWS_associate
			AWS["AWS_professional"]=AWS_professional
			AWS["AWS_specialty"]=AWS_specialty

			data["AWS"]=AWS

			Azure={}
			Azure["Azure_count"]=certs.filter(csp="Azure").count()

			Azure_fundamentals={}
			Azure_fundamentals["Azure_fundamentals_count"]=certs.filter(csp="Azure",level="Fundamentals").count()
			Azure_fundamentals_certs={}
			Azure_fundamentals_certs["Azure_certified:azure"]=certs.filter(csp="Azure",level="Fundamentals",certname="Certified: Azure").count()
			Azure_fundamentals_certs["Azure_microsoftcertified:azureai"]=certs.filter(csp="Azure",level="Fundamentals",certname="Microsoft Certified: Azure AI").count()
			Azure_fundamentals_certs["Azure_microsoftcertified:azuredata"]=certs.filter(csp="Azure",level="Fundamentals",certname="Microsoft Certified: Azure Data").count()
			Azure_fundamentals["Azure_foundational_certs"]=Azure_fundamentals_certs

			Azure_professional={}
			Azure_professional["Azure_professional_count"]=certs.filter(csp="Azure",level="Professional").count()
			Azure_professional_certs={}
			Azure_professional_certs["Azure_microsoftcertifiedazureadministrator"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified Azure Administrator").count()
			Azure_professional_certs["Azure_microsoftcertifiedazuredeveloper"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure Developer").count()
			Azure_professional_certs["Azure_microsoftcertifiedazuresecurityengineer"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure Security Engineer").count()
			Azure_professional_certs["Azure_microsoftcertifiedazureaiengineer"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure AI Engineer").count()
			Azure_professional_certs["Azure_microsoftcertifiedazuredatascientist"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure Data Scientist").count()
			Azure_professional_certs["Azure_microsoftcertifiedazuredataengineer"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure Data Engineer").count()
			Azure_professional_certs["Azure_microsoftcertifiedazuredatabaseadministrator"]=certs.filter(csp="Azure",level="Professional",certname="Microsoft Certified: Azure Database Administrator").count()
			Azure_professional["Azure_professional_certs"]=Azure_professional_certs

			Azure_expert={}
			Azure_expert["Azure_expert_count"]=certs.filter(csp="Azure",level="Expert").count()
			Azure_expert_certs={}
			Azure_expert_certs["Azure_microsoftcertifiedsolutionsarchitect"]=certs.filter(csp="Azure",level="Expert",certname="Microsoft Certified Solutions Architect").count()
			Azure_expert_certs["Azure_microsoftcertifiedcertifiedazuredevopsengineer"]=certs.filter(csp="Azure",level="Expert",certname="Microsoft Certified: Azure DevOps Engineer").count()
			Azure_expert["Azure_expert_certs"]=Azure_expert_certs

			Azure["Azure_fundamentals"]=Azure_fundamentals
			Azure["Azure_professional"]=Azure_professional
			Azure["Azure_expert"]=Azure_expert

			data["Azure"]=Azure

			return response.Response(data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))


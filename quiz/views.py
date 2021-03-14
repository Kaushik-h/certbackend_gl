from rest_framework import generics, views, permissions ,response, status
from .serializers import *
from .models import *
from django.db.models import Sum
from datetime import datetime
from .upload_report import Upload
from django.conf import settings 
from django.core.mail import send_mail, EmailMessage	

class AddQuizView(generics.CreateAPIView):
	# permission_classes = [permissions.IsAdminUser,]
	serializer_class=QuizSerializer
	queryset=Quiz.objects.all()

class DeleteQuizView(views.APIView):
	http_method_names=['delete']
	def delete(self, request, *args, **kwargs):
		try:
			Quiz.objects.get(id=request.data.get('quizid')).delete()
			return response.Response("Deleted",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AddQuestionView(views.APIView):
	# permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			quiz=Quiz.objects.get(id=request.data.get("quizid"))
			for i in range(1,(quiz.total_questions+1)):
				if request.data.get(str(i))==None:
					continue
				choices=request.data.get(str(i)).pop('choices')
				request.data.get(str(i))["quiz"]=quiz.id
				serializer=QuestionSerializer(data=request.data.get(str(i)))
				if serializer.is_valid():
					question=serializer.save()
					for c in choices:
						c["question"]=question.id
						cserializer=ChoiceSerializer(data=c)
						if cserializer.is_valid():
							choice=cserializer.save()
			return response.Response("Created successfully",status=status.HTTP_201_CREATED)
		except Exception as e:
			return response.Response(str(e))

class GetQuizView(views.APIView):
	# permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			filters = {
 				key: value
				for key, value in request.data.items()
			}
			queryset=Quiz.objects.filter(**filters)
			serializer=QuizSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class GetQuestionView(views.APIView):
	# permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			quiz=Quiz.objects.get(id=request.data.get("quizid"))
			queryset=Question.objects.filter(quiz=quiz)
			serializer=GetQuestionSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class QuizTakerView(views.APIView):
	permission_classes = [permissions.IsAuthenticated,]
	http_method_names=['get','post']

	def get(self, request, *args, **kwargs): 
		try:
			user=request.user
			# filters = {
 			# 	key: value
			# 	for key, value in request.data.items()
			# }
			queryset=QuizTaker.objects.filter(user=user)
			serializer=GetQuizTakerSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

	def post(self, request, *args, **kwargs): 
		try:
			user=request.user
			quiz=Quiz.objects.get(id=request.data.get("quiz"))
			request.data["user"]=user.id
			quiztaker=QuizTaker.objects.filter(user=user,quiz=quiz,max_score=True)
			if quiztaker:
				if request.data.get("score")>quiztaker[0].score:
					quiztaker[0].max_score=False
					quiztaker[0].save()
					request.data["max_score"]=True
				else:
					request.data["max_score"]=False
			else:
				request.data["max_score"]=True
			serializer=QuizTakerSerializer(data=request.data)
			if serializer.is_valid():
				result=serializer.save()
			else:
				return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class QuizTakerpdf(views.APIView):
	permission_classes = [permissions.IsAuthenticated,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			user=request.user
			quiztaker=QuizTaker.objects.get(id=request.data.get("quiztakerid"))
			pdf=request.FILES['report']
			quiz_date=str(datetime.now()).replace(" ","")
			pdf_name=user.email+quiz_date+'.pdf'
			a=Upload.upload_pdf(pdf, pdf_name)
			quiztaker.report_url='https://storage.googleapis.com/certificate_pdf/quiz/'+pdf_name
			quiztaker.save(force_update=True)
			subject = 'Quiz result' 
			message = 'Hello '+user.name+' , Your test results are in. You have scored '+quiztaker.score+' out of '+(quiztaker.quiz.question_count*quiztaker.quiz.marks)+' You can access your report through this link here' +quiztaker.report_url
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [user.email] 
			send_mail( subject, message, email_from, recipient_list ) 
			return response.Response("File uploaded",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class Rankings(views.APIView):
	http_method_names=['get']
	def get(self, request, *args, **kwargs): 
		try:
			queryset=User.objects.filter(user_type='nuser').filter(quiztaker__max_score=True).annotate(total=Sum('quiztaker__score')).order_by('-total')
			serializer=RankingsUserSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class FeedbackView(views.APIView):
	http_method_names=['get','delete']
	def get(self, request, *args, **kwargs): 
		try:
			queryset=Feedback.objects.all()
			serializer=GetFeedbackSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

	def delete(self, request, *args, **kwargs):
		try:
			Feedback.objects.get(id=request.data.get('feedbackid')).delete()
			return response.Response("Deleted",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))
		
class SendFeedback(views.APIView):
	http_method_names=['post']
	def post(self, request, *args, **kwargs):
		try:
			request.data["user"]=request.user.id
			serializer=FeedbackSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
			else:
				return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AdminQuizStats(views.APIView):
	# permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			filters = {
 				key: value
				for key, value in request.data.items()
			}
			queryset=QuizTaker.objects.filter(**filters)
			serializer=GetQuizTakerSerializer(queryset,many=True)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))

class AdminQuizStatspdf(views.APIView):
	# permission_classes = [permissions.IsAdminUser,]
	http_method_names=['post']
	def post(self, request, *args, **kwargs): 
		try:
			user=User.objects.get(id=request.data.get("userid"))
			pdf=request.FILES['stats']
			subject = 'Quiz stats' 
			message = 'Hello '+user.name+' .You can find the summary of your performance in this attachment'
			email_from = settings.EMAIL_HOST_USER 
			recipient_list = [user.email] 
			mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
			mail.attach("Credify-quiz-summary", pdf.read(), pdf.content_type)
			mail.send()
			return response.Response("File uploaded",status=status.HTTP_200_OK)
		except Exception as e:
			return response.Response(str(e))
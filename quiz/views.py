from rest_framework import generics, views, permissions ,response, status
from .serializers import *
from .models import *
from django.db.models import Sum
from datetime import datetime
from .upload_report import Upload

class AddQuizView(generics.CreateAPIView):
	# permission_classes = [permissions.IsAdminUser,]
	serializer_class=QuizSerializer
	queryset=Quiz.objects.all()

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
			pdf=request.FILES['report']
			quiz_date=str(datetime.now()).replace(" ","")
			pdf_name=user.email+quiz_date+'.pdf'
			a=Upload.upload_pdf(pdf, pdf_name)
			request.data["report_url"]='https://storage.googleapis.com/certificate_pdf/quiz/'+pdf_name
			serializer=QuizTakerSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
			else:
				return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			return response.Response(serializer.data,status=status.HTTP_200_OK)
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

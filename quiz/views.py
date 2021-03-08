from rest_framework import generics, views, permissions ,response, status
from .serializers import *
from .models import *

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

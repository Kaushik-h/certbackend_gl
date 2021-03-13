from rest_framework import serializers
from.models import *
from accounts.serializers import *
from accounts.models import *

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Choice
		fields='__all__'

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Question
		fields='__all__'

class GetQuestionSerializer(serializers.ModelSerializer):
	choices=ChoiceSerializer(many=True)
	class Meta:
		model=Question
		fields='__all__'

class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=Quiz
		fields='__all__'

class QuizTakerSerializer(serializers.ModelSerializer):
	class Meta:
		model=QuizTaker
		exclude=['report_url']
		
class GetQuizTakerSerializer(serializers.ModelSerializer):
	total_questions=serializers.SerializerMethodField()
	total_marks=serializers.SerializerMethodField()
	user=UserSerializer()
	quiz=QuizSerializer()
	class Meta:
		model=QuizTaker
		fields='__all__'
	def get_total_questions(self, obj):
		return obj.quiz.question_count
	def get_total_marks(self, obj):
		return (obj.quiz.question_count*obj.quiz.marks)

class GetFeedbackSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	quiz=QuizSerializer()
	class Meta:
		model=Feedback
		fields='__all__'

class FeedbackSerializer(serializers.ModelSerializer):
	class Meta:
		model=Feedback
		fields='__all__'

class RankingsUserSerializer(serializers.ModelSerializer):
	total=serializers.IntegerField()
	class Meta:
		model=User
		fields=('id','email','name','total')
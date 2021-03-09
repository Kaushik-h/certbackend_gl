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
		fields='__all__'

class GetQuizTakerSerializer(serializers.ModelSerializer):
	class Meta:
		model=QuizTaker
		fields='__all__'
		depth=1

class RankingsUserSerializer(serializers.ModelSerializer):
	total=serializers.IntegerField()
	class Meta:
		model=User
		fields=('id','email','name','total')
from rest_framework import serializers
from.models import *
from accounts.serializers import *

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

	
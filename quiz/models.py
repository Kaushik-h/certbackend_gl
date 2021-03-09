from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
User=get_user_model()

class Quiz(models.Model):
	name = models.CharField(max_length=100)
	category_choices = (("GCP", "GCP"),("AWS", "AWS"))
	category = models.CharField(max_length=30,choices=category_choices)
	subcategory = models.CharField(max_length=50)
	description = models.TextField()
	timelimit = models.IntegerField()
	marks = models.IntegerField()
	total_questions = models.IntegerField()

	@property
	def question_count(self):
		return self.questions.count()

	def __str__(self):
		return self.name

class Question(models.Model):
	quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
	text = models.TextField()
	explanation = models.TextField()
	question_types = (("single", "single"),("multiple", "multiple"))
	question_type = models.CharField(max_length=10,choices=question_types)

	def __str__(self):
		return self.text

class Choice(models.Model):
	question = models.ForeignKey(Question, related_name='choices' ,on_delete=models.CASCADE)
	text = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.text

class QuizTaker(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	rightans_no = models.IntegerField()
	wrongans_no = models.IntegerField()
	score = models.IntegerField(default=0)
	report_url = models.URLField()
	date = models.DateTimeField(auto_now_add=True)
	max_score = models.BooleanField()

	def __str__(self):
		return self.user.email
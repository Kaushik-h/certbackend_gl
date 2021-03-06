from django.db import models
from django.contrib.auth import get_user_model
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
	score = models.IntegerField(default=0)
	date_finished = models.DateTimeField(null=True)

	def __str__(self):
		return self.user.email
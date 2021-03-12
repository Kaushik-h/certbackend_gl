from django.urls import path
from .views import *

urlpatterns = [
    path('addquiz', AddQuizView.as_view()),
    path('deletequiz', DeleteQuizView.as_view()),
    path('addquestions', AddQuestionView.as_view()),
    path('getquiz', GetQuizView.as_view()),
    path('getquestions', GetQuestionView.as_view()),
    path('quizresults', QuizTakerView.as_view()),
    path('rankings', Rankings.as_view()),
    path('feedback', FeedbackView.as_view()),
    path('sendfeedback', SendFeedback.as_view()),
    path('adminquizstats', AdminQuizStats.as_view()),
]
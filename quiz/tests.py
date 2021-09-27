from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from .views import *

class ViewRequestFactoryTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True  # More verbose messages
    view_class = None
    def get_response(self, method):
        factory = RequestFactory()
        req = getattr(factory, method)('/')
        req.user = AnonymousUser()
        return self.view_class.as_view()(req, *[], **{})
    def is_callable(self):
        resp = self.get_response('post')
        self.assertEqual(resp.status_code, 200)

class GetquizTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = GetQuizView
    
    def test_get(self):
        self.is_callable()

class AccountTests(APITestCase):
    
    def test_create_quiz(self):
        response = Quiz.objects.create(name="Quiztest",category="GCP",subcategory="GCS",description="aa",timelimit=10,marks=2,total_questions=10)
        self.assertEqual(response.name, "Quiztest")

    def test_get_quiz(self):
        response = self.client.post('/getquiz',data={"id":1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_post_quiz(self):
        quiz={
            "name":"First 34quiz",
            "category":"GCP",
            "subcategory":"cloud storage",
            "description":"This quiz has 10 questions. Each carries 2 points. No negative marks",
	        "timelimit":10,
	        "marks":2,
	        "total_questions":10
        }
        response = self.client.post('/addquiz',data=quiz)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rankings(self):
        response = self.client.get('/rankings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




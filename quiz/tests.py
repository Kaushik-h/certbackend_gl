from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .views import *

class AccountTests(APITestCase):
    def test_create_account(self):
        response = self.client.get('/getquiz/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
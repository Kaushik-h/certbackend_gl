from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from .views import *

class ViewRequestFactoryTestMixin(object):
	"""Mixin with shortcuts for view tests."""
	longMessage = True  
	view_class = None
	def get_response(self, method):
		factory = RequestFactory()
		req = getattr(factory, method)('/')
		req.user = AnonymousUser()
		return self.view_class.as_view()(req, *[], **{})
	def is_callable(self):
		resp = self.get_response('get')
		self.assertEqual(resp.status_code, 401)

class GetcertTestCase(ViewRequestFactoryTestMixin, TestCase):
	view_class = CertificateView
	
	def test_get(self):
		self.is_callable()

class AccountTests(APITestCase):

	def test_token(self):
		response = self.client.get('/certificates')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_admin(self):
		response = self.client.get('/feedback')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_stats(self):
		response = self.client.post('/adminquizstats')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test(self):
		response = self.client.get('/expires')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)






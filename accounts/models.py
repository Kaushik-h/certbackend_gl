from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

class UserManager(BaseUserManager):

	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The Email must be set'))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

	def validate_email(value):
		if not value.endswith('virtusa.com'):
			raise ValidationError("Enter your org mail")
	email = models.EmailField(unique=True, null=False, blank=False, validators=[validate_email])
	name = models.CharField(max_length=40,null=False,blank=False)
	empid = models.CharField(max_length=20,null=False,blank=False,unique=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	USER_CHOICES = (('nuser', 'nuser',),('admin', 'admin',))
	user_type = models.CharField(null=False,blank=False,choices=USER_CHOICES,max_length=5)
	USERNAME_FIELD = 'email'
	objects = UserManager()

	
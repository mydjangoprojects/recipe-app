from django.contrib.auth.models import BaseUserManager, \
    PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext as _
from django.db import models


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        # Email validation
        if not email:
            raise ValueError('Users must have an email address.')

        # User Creation
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and saves a new staff user"""

        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new super user"""

        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports sign in and sign up using
       email instead of username"""
    username = None
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

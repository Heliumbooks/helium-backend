from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email_address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, default='', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, default='', blank=True, null=True)
    last_name = models.CharField(max_length=100, default='', blank=True, null=True)
    full_name = models.CharField(max_length=200, default='', blank=True, null=True)
    mobile_token = models.CharField(max_length=100, default='', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Accounts"


class UserPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    password_hash = models.CharField(max_length=255, null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Passwords"

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"



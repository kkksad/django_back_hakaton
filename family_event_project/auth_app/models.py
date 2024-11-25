from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_app_users',
        related_query_name='auth_app_user',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_app_users',
        related_query_name='auth_app_user',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name='custom_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return uuid.uuid4().hex




class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

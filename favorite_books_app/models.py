from typing import Text
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
import re

# Create your models here.
class userManager(models.Manager):
    def userValidation(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = "Passwords do not match"
        return errors


class User(models.Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255)
    password = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = userManager()


class Book(models.Model):
    title = CharField(max_length=255)
    description = TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="books_liked")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
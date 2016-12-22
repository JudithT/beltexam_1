from __future__ import unicode_literals
from django.db import models
import re, datetime
import bcrypt

# from bcrypt import hashpw

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm, birthday):
        errors = []
        newuser = ""
        EMAIL_REGEX = (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(first_name) <= 2:
            errors.append("A first name with at least two character is required")
        if len(last_name) <= 2:
            errors.append("A last name with at least two character is required")
        if len(password) == 0:
            errors.append("Password is required")
        elif password != confirm:
            errors.append("Password and confrimation must match")
        if len(email) == 0:
            errors.append("Email is required")
        elif not re.match(EMAIL_REGEX, email):
            errors.append("Valid email is required")
        if len(errors) is not 0:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            Users = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = hashed, birthday=birthday)
            newuser = "Successfully created new user"
            return (True, Users)

    def login(self, email, password):
        errors = []
        print "$$$$$$$$$$$$", email
        print "$$$$$$$$$$$$", password
        if User.objects.filter(email=email):
            user = User.objects.filter(email=email)[0]
            print "PRINT USER IN LOGIN METHOD", user
            hashed = user.password
            if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
                loggedin = "Successfully created new user"
                return (True, user)
            else:
                errors.append("Invalid password for this email")
                return (False, errors)
        else:
            errors.append("Invalid login credentials")
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=45, default='null')
    last_name = models.CharField(max_length=45, default='null')
    email = models.CharField(max_length=45, default='null')
    password = models.CharField(max_length=255, default='null')
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User)
    author = models.CharField(max_length=255)

class Favorite(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    message= models.ForeignKey(Message)
    user = models.ForeignKey(User)

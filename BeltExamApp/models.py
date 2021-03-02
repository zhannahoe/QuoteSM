from django.contrib.messages.api import error
from django.db import models
import re
from datetime import date
import datetime
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from django.http import request

class UserManager(models.Manager):
    def basic_validator(self, forminfo):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        matchingEmail = User.objects.filter(email = forminfo['email'])
        today = date.today()
        thirteen = datetime.datetime(2008, 2, 25)
        print('*****************')
        print(today)

        errors = {}
        if len(forminfo['first_name']) == 0:
            errors['firstNameRequired'] = 'Must enter First name name'
        elif len(forminfo['first_name']) <= 2:
            errors['firstNameNotLongEnough'] = 'First name must be longer than 2 characters'

        if len(forminfo['last_name']) == 0:
            errors['lastNameRequired'] = 'Must enter Last name'
        elif len(forminfo['last_name']) <= 2:
            errors['lastNameNotLongEnough'] = 'Last name must be longer than 2 characters'

        if len(forminfo['email']) == 0:
            errors['emailRequired'] = 'Must enter email'
        elif not email_regex.match(forminfo['email']):
            errors['invalidEmail'] = 'Email must be a valid address'
        elif len(matchingEmail) > 0:
            errors['repeatEmail'] = 'Email is already in use'

        if len(forminfo['password']) == 0:
            errors['passwordRequired'] = 'Must enter password'
        elif len(forminfo['password']) <= 7:
            errors['passwordLongEnough'] = 'Password must be at least 8 characters'
        elif forminfo['password'] != forminfo['confirm_password']:
            errors['passwordNotMatching'] = 'Passwords must match'

        return errors

    def login_validator(self, forminfo):
        errors = {}
        emailLogin = User.objects.filter(email = forminfo['email'])
        print (emailLogin)

        if len(emailLogin) == 0:
            errors['emailError'] = 'Must enter email'
        elif emailLogin[0].email != forminfo['email']:
            errors['wrongEmail'] = 'Email is not on file'

        if len(forminfo['password']) == 0:
            errors['passwordRequired'] = 'Must enter password'
        elif emailLogin[0].password != forminfo['password']:
            errors['wrongPassword'] = 'Password does not match email'

        return errors
    
    def update_validator(self, forminfo, currentUser):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        matchingEmail = User.objects.filter(email = forminfo['email'])
        

        if len(forminfo['first_name']) == 0:
            errors['firstNameRequired'] = 'Must enter First name name'
        elif len(forminfo['first_name']) <= 2:
            errors['firstNameNotLongEnough'] = 'First name must be longer than 2 characters'

        if len(forminfo['last_name']) == 0:
            errors['lastNameRequired'] = 'Must enter Last name'
        elif len(forminfo['last_name']) <= 2:
            errors['lastNameNotLongEnough'] = 'Last name must be longer than 2 characters'

        if len(forminfo['email']) == 0:
            errors['emailRequired'] = 'Must enter email'
        elif not email_regex.match(forminfo['email']):
            errors['invalidEmail'] = 'Must be a valid email address'
        elif len(matchingEmail) > 0 and matchingEmail[0].email != currentUser.email:
            errors['repeatEmail'] = 'Email already in use'
            print(currentUser.email)

        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, forminfo):
        errors = {}
        if len(forminfo['author']) == 0:
            errors['authorRequired'] = 'Author is required'
        elif len(forminfo['author']) <= 3:
            errors['authorTooShort'] = "Author's name should be longer than 3 characters"

        if len(forminfo['quote']) == 0:
            errors['quoteRequired'] = 'Quote is required'
        elif len(forminfo['quote']) < 10:
            errors['quoteTooShort'] = 'Quote must be longer than 10 characters'
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    actual_quote = models.TextField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='uploaded_quote', on_delete=models.CASCADE, null=True)
    users_who_like = models.ManyToManyField(User, related_name='liked_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    numLikes = models.IntegerField(null=True)

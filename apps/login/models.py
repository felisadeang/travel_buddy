from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def isValidRegistration(self, userInfo):
        passFlag = True
        errors = []
        if len(userInfo['name']) < 3:
            errors.append('Name must be at least 3 characters.')
            passFlag = False
        if len(userInfo['username']) < 3:
            errors.append('Username must be at least 3 characters.')
            passFlag = False
        if len(userInfo['password']) < 8:
            errors.append('Password must contain at least 8 characters.')
            passFlag = False
        if userInfo['password'] != userInfo['confirm_password']:
            errors.append('Passwords do not match.')
            passFlag = False
        if len(self.filter(username=userInfo['username'])) > 0:
			errors.append("Registration is invalid.")
			passFlag = False

        if passFlag == True:
            hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
            self.create(name = userInfo['name'], username = userInfo['username'], password = hashed)
        return [passFlag, errors]

    def ValidLogin(self, userInfo):
        passFlag = True
        errors = []
        if len(User.objects.filter(username=userInfo['username'])) > 0:
            hashed = User.objects.get(username = userInfo['username']).password
            hashed = hashed.encode('utf-8')
            password = userInfo['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                passFlag = True
            else:
                errors.append("Unsuccessful login.")
                passFlag = False
        else:
            errors.append("Unsuccessful login.")
            passFlag = False
        return [passFlag, errors]

class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    userManager = UserManager()

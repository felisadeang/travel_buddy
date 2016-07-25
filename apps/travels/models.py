from __future__ import unicode_literals
from ..login.models import User
from django.contrib import messages
from django.db import models
from datetime import date, datetime
from dateutil.parser import parse as parse_date

class TravelManager(models.Manager):
    def ValidTravelPlanned(self, userInfo, request):
        passFlag = True
        if len(userInfo['destination']) < 1:
            messages.warning(request, 'Destination field left blank.')
            passFlag = False
        if len(userInfo['description']) < 1:
            messages.warning(request, 'Description field left blank.')
            passFlag = False

        unicode_text_from = userInfo['travel_date_from']
        from_date = parse_date(unicode_text_from)
        if from_date.date() < date.today():
            messages.warning(request, 'Travel from date cannot be in the past.')
            passFlag = False
        unicode_text_to = userInfo['travel_date_to']
        to_date = parse_date(unicode_text_to)
        if to_date.date() < date.today():
            messages.warning(request, 'Travel to date cannot be in the past.')
            passFlag = False
        if to_date < from_date:
            messages.warning(request, 'Travel to date cannot be before travel from date.')
            passFlag = False

        if passFlag:
            logged_in = request.session['logged_in']
            travelplanner = User.objects.get(id=logged_in)
            travelmaker = User.objects.get(id=logged_in)
            travel = self.create(destination = userInfo['destination'], description = userInfo['description'], travel_date_from = userInfo['travel_date_from'], travel_date_to = userInfo['travel_date_to'], travelplanner_id = travelplanner)
        return passFlag

class Travel(models.Model):
    destination = models.TextField(max_length=100)
    description = models.TextField(max_length=150)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    travelplanner_id = models.ForeignKey(User, related_name="travelplanner")
    travelmaker_id = models.ManyToManyField(User, related_name="travelmaker")
    travelManager = TravelManager()
    objects = models.Manager()

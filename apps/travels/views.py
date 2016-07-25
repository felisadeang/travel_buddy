from django.shortcuts import render, redirect
from ..login.models import User
from .models import Travel
from django.db import models
from django.contrib import messages
from django.core.urlresolvers import reverse

def travels(request, id):
    logged_in = request.session['logged_in']
    context = {
        "person": User.objects.get(id=id),
        "travels" : Travel.objects.all(),
    }
    return render(request, 'travels/index.html', context)

def create(request):
    return render(request, 'travels/create.html')

def createtravel(request):
    if Travel.travelManager.ValidTravelPlanned(request.POST, request):
        passFlag = True
        return redirect(reverse('login_travels', kwargs={'id':request.session['logged_in']}))
    else:
        passFlag = False
        return redirect (reverse('travels_create'))

def show(request, id):
	context = {
		"travel": Travel.objects.get(id=id),
	}
	return render(request, 'travels/show.html', context)

def join(request):
    if request.method == 'POST':
        id = request.POST['traveler']
        traveler = User.objects.get(id=request.POST['traveler'])
        travelplans = Travel.objects.get(id=request.POST['destination'])
        travelplans.travelmaker_id.add(traveler)
        travelplans.save()
        return redirect(reverse('login_travels', kwargs={'id':id}))

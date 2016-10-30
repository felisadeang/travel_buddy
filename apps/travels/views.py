from django.shortcuts import render, redirect
from ..login.models import User
from .models import Travel
from django.db import models
from django.contrib import messages
from django.core.urlresolvers import reverse

def travels(request, id):
    # if request.session['logged_in'] != id:
    #     return redirect(reverse('login_travels', kwargs={'id':request.session['logged_in']}))
    # else:
        user = User.objects.get(id=request.session["logged_in"])
        context = {
            "loggedin": User.objects.get(id=id),
            "travels" : Travel.objects.all(),
            "trips_off": Travel.objects.exclude(travelplanner_id=user).exclude(travelmaker_id=user.id)
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
        traveler_id = request.POST['traveler']
        dest_id = request.POST['destination']
        traveler = User.objects.get(id=traveler_id)
        travelplans = Travel.objects.get(id=dest_id)
        travelplans.travelmaker_id.add(traveler)
        travelplans.save()
        return redirect(reverse('login_travels', kwargs={'id':request.session['logged_in']}))

def remove(request, id):
    Travel.objects.get(id=id).delete()
    return redirect(reverse('login_travels', kwargs={'id':request.session['logged_in']}))

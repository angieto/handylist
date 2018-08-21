from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
import bcrypt
from datetime import date
from .models import *

def index(request):
    return render(request, 'main/index.html')

def create(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index')
    else:
        user_password = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt(10))
        user_password = user_password.decode('utf8')
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=user_password)
        request.session['user'] = user.id
        return redirect('dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index') 
    else:   
        user = User.objects.get(email=request.POST['email'])
        request.session['user'] = user.id
        print("This is the user's id:", request.session['user'])
        return redirect('dashboard')

def dashboard(request):
    user = User.objects.get(id=request.session['user'])
    context = {
        'user': user,
        'available_jobs': Job.objects.exclude(participants=user),
        'my_jobs': user.participated_jobs.all()
    }
    return render(request, 'main/dashboard.html', context)

def view(request, id):
    # display the page with job description and the adding information
    job = Job.objects.get(id=id)
    return render(request, 'main/view.html', {'job':job})

def make_job(request):
    return render(request, 'main/make_job.html')

def submit_the_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('make_job')    
    else:
        user = User.objects.get(id=request.session['user'])
        new_job = Job.objects.create(title=request.POST['title'], description=request.POST['desc'], location=request.POST['location'], creator=user)
        return redirect('dashboard')

def add_job(request, id):
    user = User.objects.get(id=request.session['user'])
    job = Job.objects.get(id=id)
    job.participants.add(user)
    job.save()
    return redirect('dashboard')

def edit_job(request, id):
    job = Job.objects.get(id=id)
    # direct to the page with prepopulated job info
    return render(request, 'main/edit_job.html', {'job':job})

def edit(request, id):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('edit_job', id)    
    else:
        user = User.objects.get(id=request.session['user'])
        job = Job.objects.get(id=id)
        job.title=request.POST['title']
        job.description=request.POST['desc']
        job.location=request.POST['location']
        job.creator=user
        job.save()
        return redirect('dashboard')

def cancel(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('dashboard')

def done(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    # Done link on the user's My Jobs list deletes the job from the database
    return redirect('dashboard')

def logout(request):
    request.session.clear()
    return redirect('index')

def back(request):
    return redirect('dashboard')

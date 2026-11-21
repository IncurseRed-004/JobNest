from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from jobnest_app.forms import RegistrationForm, JobForm
from jobnest_app.models import Job, Application
from django.db.models import Q


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')

    else:
        form = RegistrationForm()
    return render(request,'register.html',{"form":form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data =request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('job_list')
    else:
        form = AuthenticationForm()

    return render(request,'login.html',{"form":form})

def user_logout(request):
    logout(request)
    return redirect("login")

def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query)
        )
    return render(request,'job_list.html',{"jobs":jobs,'query':query})

def job_details(request,id):
    job = get_object_or_404(Job,id=id)
    return render(request,'job_details.html',{"job":job})

@login_required(login_url='login')
def job_application(request,id):
    job =get_object_or_404(Job,id=id)

    if request.method =="POST":
        Application.objects.create(
        user = request.user,
        job = job
        )

        return redirect('my_applications')
    return redirect('job_details',id=id)

@login_required(login_url='login')
def my_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request,'my_applications.html',{"applications":applications})


@staff_member_required
def admin_job_listing(request):
    jobs =Job.objects.all()
    return render(request,'admin_job_listing.html',{"jobs":jobs})

@staff_member_required
def add_job(request):

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()

            return redirect('admin_job_listing')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {"form": form})

@staff_member_required
def edit_job(request,id):
    job = get_object_or_404(Job,id=id)

    if request.method =="POST":
        form = JobForm(request.POST,instance=job)

        if form.is_valid():
            form.save()
            return redirect('admin_job_listing')

    else:
        form =JobForm(instance=job)

    return render(request,'job_form.html',{"form":form})

@staff_member_required
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('admin_job_listing')

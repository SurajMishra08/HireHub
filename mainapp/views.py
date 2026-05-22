from django.shortcuts import render,redirect
from .forms import EnquiryForm
from django.contrib import messages
from .models import *
from django.db import transaction
from django.utils import timezone

# Create your views here.
def index(request):
    newly_job = Job.objects.all().order_by('-created_at')[:5]
    for job in newly_job:
        if job.deadline < timezone.now().date():
            job.id_active = False
            job.save()
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'newly_job':newly_job,
        'user':user
    }
    return render(request, "mainapp/index.html",context)

def jobdetails(request,id):
    job = Job.objects.get(id=id)
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'job':job,
        'user':user
    }
    return render(request, "mainapp/jobdetails.html",context)

def userlogin(request):
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'user':user
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(username=username, password=password)
            if user and user.usertype == "admin":
                messages.success(request,"Welcome Admin")
                request.session['adminid'] = user.username
                request.session.set_expiry(0)
                return redirect('admindash')
            elif user and user.usertype == "jobseeker":
                messages.success(request, "Welcome Jobseeker")
                request.session['jsid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
            elif user and user.usertype == "employer":
                messages.success(request, "Welcome Employer")
                request.session['empid'] = user.username
                request.session.set_expiry(0)
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid username and password")
            return redirect('login')
    return render(request, "mainapp/login.html",context)

def register(request):
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'user':user
    }
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password != confirmpassword :
            messages.warning(request,"Password must be Same")
            return redirect('register')
        exists = LoginInfo.objects.filter(username=email)
        if exists:
            messages.error(request,"This mail is already registered")
            return redirect('register')
        try:
            with transaction.atomic():
                log = LoginInfo(usertype=usertype, username=email,password=password)
                if usertype == "jobseeker":
                    js = Jobseeker(user=log,first_name=firstname,last_name=lastname,email=email,contact_no=contact_no)
                    log.save()
                    js.save()
                elif usertype == "employer":
                    emp = Employer(user=log,first_name=firstname,last_name=lastname,email=email,contact_no=contact_no)
                    log.save()
                    emp.save()
                messages.warning(request,"Registered successfully . Now Login to update profile")
                return redirect('register')
        except Exception as e:
            messages.warning(request,"Something went Wrong")
            return redirect('register')
    return render(request, "mainapp/register.html",context)

def contact(request):
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    form = EnquiryForm()
    context = {
        'user':user,
        "form":form
    }
    if request.method == "POST":
        data = EnquiryForm(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request,"Enquiry submitted successfully")
        else:
            messages.error(request, "Failed to send enquiry, Invalid form detail")
        return redirect('contact')
    else:
        form = EnquiryForm()

    return render(request, "mainapp/contact.html",context)

def about(request):
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'user':user,
    }
    return render(request, "mainapp/about.html",context)

def jobs(request):
    all_jobs = Job.objects.all().order_by('-created_at')
    for job in all_jobs:
        if job.deadline < timezone.now().date():
            job.id_active = False
            job.save()
    userid = request.session.get('jsid') or request.session.get('empid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(username=userid)
        if obj.usertype == "jobseeker":
            user = Jobseeker.objects.get(email=userid)
        elif obj.usertype == "employer":
            user = Employer.objects.get(email=userid)
    context = {
        'all_jobs': all_jobs,
        'user': user,

    }
    return render(request, "mainapp/jobs.html",context)

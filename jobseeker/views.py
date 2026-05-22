from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.utils import timezone

# Create your views here.


def jobseekerdash(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    applications = JobApplication.objects.filter(jobseeker=js)
    context = {
        'jsid' : jsid,
        'js' : js,
        'applications': applications
    }
    return render(request, "jobseeker/jobseekerdash.html",context)

def jsupdate(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experiences = Experience.objects.filter(jobseeker=js)
    context = {
        'js': js,
        'educations' : educations,
        'experiences' : experiences
    }
    if request.method == "POST":
        js.first_name = request.POST.get('firstname')
        js.last_name = request.POST.get('lastname')
        js.dob = request.POST.get('dob')
        js.gender = request.POST.get('gender')
        js.contact_no = request.POST.get('contact_no')
        js.locality = request.POST.get('locality')
        js.city = request.POST.get('city')
        js.district = request.POST.get('district')
        js.zip_code = request.POST.get('zip_code')
        js.state = request.POST.get('state')
        js.country = request.POST.get('country')
        picture = request.FILES.get('picture')
        if picture:
            js.picture = picture
        js.save()
        messages.success(request, "Updated Successfully")
    return render(request, "jobseeker/jsupdate.html",context)

def jsprofile(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    educations = Education.objects.filter(jobseeker=js)
    experiences = Experience.objects.filter(jobseeker=js)
    context = {
        'js': js,
        'educations' : educations,
        'experiences' : experiences
    }
    return render(request, "jobseeker/jsprofile.html",context)

def appliedjobs(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    applications = JobApplication.objects.filter(jobseeker = js)
    context = {
        'jsid' : jsid,
        'js' : js,
        'applications' : applications
    }
    return render(request, "jobseeker/appliedjobs.html",context)

def save_education (request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        degree_name = request.POST.get('degree_name')
        specialization = request.POST.get('specialization')
        institute = request.POST.get('institute')
        university = request.POST.get('university')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        Education.objects.create(jobseeker=js, degree_name=degree_name, specialization=specialization, institute=institute, university=university, start_year=start_year, end_year=end_year)
        messages.success(request,"Educational Information added successfully")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went Wrong")
        return redirect('login')
    
def save_experience(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        designation = request.POST.get('designation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        Experience.objects.create(jobseeker=js, company_name=company_name, designation=designation, start_date=start_date, end_date=end_date, description=description)
        messages.success(request,"Experience added successfully")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went Wrong")
        return redirect('login')
    
def save_additional(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        resume = request.FILES.get('resume')
        if resume:
            js.resume=resume
        cv = request.FILES.get('cover_letter')
        if cv:
            js.cover_letter=cv
        js.expected_salary = request.POST.get('expected_salary')
        js.current_salary = request.POST.get('current_salary')
        js.notice_period = request.POST.get('notice_period')
        js.linkedin_url = request.POST.get('linkedin_url')
        js.github_url = request.POST.get('github_url')
        js.portfolio_url = request.POST.get('portfolio_url')
        work = request.POST.get('is_open_to_work')
        if work == "on":
            js.is_open_to_work = True
        else:
            js.is_open_to_work = False
        js.save()
        messages.success(request,"Additional added successfully")
        return redirect('jsupdate')
    else:
        messages.error(request, "Something went Wrong")
        return redirect('login')

def logoutjobseeker(request):
    if 'jsid' not in request.session:
        messages.error(request, "Login First")
        return redirect('index')
    del request.session['jsid']
    messages.success(request, "Logout Successfully")
    return redirect('index')

def save_skill(request):
    if 'jsid' not in request.session:
        messages.error(request, "Login First")
        return redirect('index')
    
    jsid = request.session.get('jsid')
    jsdata = Jobseeker.objects.get(email=jsid)
    if request.method == "POST":
        skills_input = request.POST.get('skills')

        if skills_input:
            skills_objects = []
            skill_names = [s.strip() for s in skills_input.split(',') if s.strip()]

            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact = name,
                    defaults = {'skill_name':name}
                )
                skills_objects.append(skill)
            jsdata.skills.set(skills_objects)
            messages.success(request,"Skills updated successfully")
        else:
            jsdata.skills.clear()
            messages.warning(request,"All skills removed")
        return redirect('jsupdate')
    return redirect('jsupdate')
    
def apply(request,id):
    if 'jsid' not in request.session:
        messages.error(request, "You must be logged In before applying any job.")
        return redirect('index')
    jobseekerid = request.session.get('jsid')
    jsdata = Jobseeker.objects.get(email=jobseekerid)
    job = Job.objects.get(id=id)

    if job.is_active == False:
        messages.error(request,"Link is inactive")
        return redirect('jobdetails',id=job.id)
    
    if job.deadline < timezone.now().date():
        messages.error(request,"Deadline has passed")
        return redirect('jobdetails',id=job.id)
    
    if JobApplication.objects.filter(jobseeker=jsdata,job=job):
        messages.warning(request,"You have already applied for this job.")
        return redirect('jobdetails',id=job.id)
    
    JobApplication.objects.create(
        jobseeker=jsdata,
        job = job
    )
    messages.success(request, "Applied successfully")
    return redirect('jobdetails',id=job.id)

def jschangepassword(request):
    if "jsid" not in request.session:
        messages.error(request,"Login Required")
        return redirect('login')
    jsid = request.session.get('jsid')
    js = LoginInfo.objects.get(username=jsid)
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd2')
        newpwd = request.POST.get('newpwd2')
        confirmpwd = request.POST.get('confirmpwd2')
        if oldpwd != js.password:
            messages.warning(request, "Old Password not matched!!")
            return redirect('jschangepassword')
        elif newpwd != confirmpwd:
            messages.error(request, "New and confirm password must be same")
            return redirect('jschangepassword')
        elif newpwd == js.password:
            messages.warning(request, "New password should be different from old.")
            return redirect('jschangepassword')
        else:
            js.password = newpwd
            js.save()
            messages.success(request, "Password Changed Successfully.")
            return redirect('jobseekerdash')
    return render(request, "jobseeker/jschangepassword.html")
        
from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from django.core.mail import send_mail

# Create your views here.

def employerdash(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'empdata':empdata
    }
    return render(request, "employer/employerdash.html",context)

def empprofile(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    companydata = empdata.company
    context = {
        'empid':empid,
        'empdata':empdata,
        'companydata': companydata,
   }
    return render(request, "employer/empprofile.html",context)

def viewjobs(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    emp_job = Job.objects.filter(employer = empdata)
    context = {
        'empid':empid,
        'empdata':empdata,
        'emp_job':emp_job
    }
    return render(request, "employer/viewjobs.html",context)

def deljob(request,id):
    if 'empid' not in request.session:
        messages.error(request,"Please login first")
        return redirect('index')
    # empid = request.session.get('empid')
    # empdata = Employer.objects.get(email = empid)
    # job = Job.objects.filter(employer = empdata)
    del_job = Job.objects.get(id=id)
    del_job.delete()
    messages.success(request,"Job deleted Successfully.")
    return redirect('viewjobs')

def editjob(request,id):
    if 'empid' not in request.session:
        messages.error(request,"Please login first")
        return redirect('index')
    # empid = request.session.get('empid')
    # empdata = Employer.objects.get(email = empid)
    # job = Job.objects.filter(employer = empdata)
    edit_job = Job.objects.get(id=id)
    if request.method == "POST":
        edit_job.title = request.POST.get('title')
        edit_job.job_type = request.POST.get('job_type')
        edit_job.salary = request.POST.get('salary')
        edit_job.location = request.POST.get('location')
        skills_required = request.POST.get('skills_required')
        edit_job.vacancy = request.POST.get('vacancy')
        edit_job.deadline = request.POST.get('deadline')
        edit_job.description = request.POST.get('description')
        if skills_required:
            job_skill = []
            skill_names = [s.strip() for s in skills_required.split(',') if s.strip()]
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact = name,defaults={'skill_name':name}
                )
                job_skill.append(skill)
            edit_job.skills_required.set(job_skill)
        edit_job.save()
        messages.success(request,"Job updated successfully.")
    messages.success(request,"Job deleted Successfully.")
    return redirect('viewjobs')

def postjob(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    all_skill = Skill.objects.all()
    cats = JobCategory.objects.all()
    context = {
        'empid':empid,
        'empdata':empdata,
        'all_skill':all_skill,
        'cats':cats
    }
    if request.method == "POST":
        cat = None
        catid = request.POST.get('catid')
        if catid:
          cat = JobCategory.objects.get(id=catid)  
        title = request.POST.get('title')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        vacancy = request.POST.get('vacancy')
        deadline = request.POST.get('deadline')
        skills_required = request.POST.get('skills_required')
        description = request.POST.get('description')
        if not empdata.company:
            messages.warning(request, "You haven't added company information yet. please add this first.")
            return redirect('postjob')
        job = Job.objects.create(
            category=cat,
            employer = empdata,
            company = empdata.company,
            title=title,
            job_type=job_type,
            salary=salary,
            location=location,
            vacancy=vacancy,
            deadline=deadline,
            description=description
        )
        if skills_required:
            job_skill = []
            skill_names = [s.strip() for s in skills_required.split(',') if s.strip()]
            for name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    skill_name__iexact = name,defaults={'skill_name':name}
                )
                job_skill.append(skill)
            job.skills_required.set(job_skill)
        job.save()
        messages.success(request,"Job posted Successfully")
        return redirect('postjob')
    return render(request, "employer/postjob.html",context)

def empupdate(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    context = {
        'empid':empid,
        'empdata':empdata,
    }
    if request.method == "POST":
        picture = request.FILES.get('picture')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        contact_no = request.POST.get('contact_no')
        designation = request.POST.get('designation')
        #email = request.POST.get('email')
        if picture:
            empdata.picture=picture
        empdata.first_name=firstname
        empdata.last_name=lastname
        empdata.dob=dob
        empdata.gender=gender
        empdata.contact_no=contact_no
        empdata.designation = designation
        empdata.save()
        messages.success(request, "Updated Successfully")
        return redirect('empupdate')
    return render(request, "employer/empupdate.html",context)

def empchangepassword(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login First")
        return redirect('index')
    empid = request.session.get('empid')
    emp = LoginInfo.objects.get(username=empid)
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        if oldpwd != emp.password:
            messages.warning(request, "Old Password not matched!!")
            return redirect('empchangepassword')
        elif newpwd != confirmpwd:
            messages.error(request, "New and confirm password must be same")
            return redirect('empchangepassword')
        elif newpwd == emp.password:
            messages.warning(request, "New password should be different from old.")
            return redirect('empchangepassword')
        else:
            emp.password = newpwd
            emp.save()
            messages.success(request, "Password Changed Successfully.")
            return redirect('employerdash')
    return render(request, "employer/empchangepassword.html")

def emplogout(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login First")
        return redirect('index')
    del request.session['empid']
    messages.success(request, "Logout Successfully")
    return redirect('index')

def companydetails(request):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        contact_no = request.POST.get('contact_no')
        logo = request.FILES.get('logo')
        industry = request.POST.get('industry')
        established_at = request.POST.get('established_at')
        website = request.POST.get('website')
        email = request.POST.get('email')
        location = request.POST.get('location')
        details = request.POST.get('details')
        comp = Company.objects.create(
            company_name = company_name,
            contact_no = contact_no,
            logo = logo,
            industry = industry,
            established_at = established_at,
            website = website,
            email = email,
            location = location,
            details = details
        )
        empdata.company = comp
        empdata.save()
        messages.success(request, "Company Details added successfully.")
        return redirect('empupdate')
    else:
        messages.error(request, "Something went wrong")
        return redirect('index')


def viewapplicant(request,id):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    empid = request.session.get('empid')
    empdata = Employer.objects.get(email=empid)
    job = Job.objects.get(id=id)
    applications = JobApplication.objects.filter(job=job)
    context = {
        'empid':empid,
        'empdata':empdata,
        'applications':applications,
        'job':job
    }
    return render(request, 'employer/viewapplicant.html',context)

def updatestatus(request, appid):
    if 'empid' not in request.session:
        messages.error(request, "Please Login first")
        return redirect('index')
    app = JobApplication.objects.get(id=appid)
    if request.method == "POST":
        status = request.POST.get('status')
        app.status = status
        app.save()
        if status == 'selected':    
            try:
                send_mail(
                f"Selection Confirmation for the Position Applied - HireHub",
                f"""
Dear {app.jobseeker.first_name} {app.jobseeker.last_name},
We are pleased to inform you that you have been selected for the position of {app.job.title},

Please confirm your accepectance and share your availability for joining.

Best Regards,
{app.job.employer.first_name} {app.job.employer.last_name}
{app.job.employer.company.company_name}
                """,
                f"",
                [app.jobseeker.email],
                fail_silently=False,
            )
            except:
                messages.error(request,"Something went wrong")
        if status == 'rejected':    
            try:
                send_mail(
                f"Selection Confirmation for the Position Applied - HireHub",
                f"""
Dear {app.jobseeker.first_name} {app.jobseeker.last_name},
Thank you for taking the time to apply for the {app.job.title} position at {app.job.employer.company.company_name}. We appreciate the effort you put into your application and the interest you have shown in joining our team.

After careful consideration, we regret to inform you that we will not be moving forward with your application at this time. While your skills and experience are commendable, we have decided to pursue other candidates whose qualifications more closely align with our current needs.

We encourage you to apply for future opportunities with us, as we believe your background could be a strong fit for other roles.

Wishing you success in your job search and future endeavors

Best Regards,
{app.job.employer.first_name} {app.job.employer.last_name}
{app.job.employer.company.company_name}
                """,
                f"",
                [app.jobseeker.email],
                fail_silently=False,
            )
            except:
                messages.error(request,"Something went wrong")
        
        messages.success(request, "Application status updated successfully.")
        return redirect('viewapplicant',id=app.job.id)
    else:
        return redirect('viewapplicant',id=app.job.id)
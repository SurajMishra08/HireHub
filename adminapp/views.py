from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

# Create your views here.
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    return render(request,"admin/admindash.html")

def viewenq(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    en = Enquiry.objects.all()
    context = {
        'enquiry' : en
    }
    return render(request,"admin/viewenq.html",context)

def delenq(request,eid):
    if 'adminid' in request.session:
        try:
            enq = Enquiry.objects.get(id=eid)
            enq.delete()
            return redirect('viewenq')
        except Enquiry.DoesNotExist:
            messages.error(request,"Enquiry not found")
            return redirect('viewenq')


def changepass(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        admin = LoginInfo.objects.get(username = adminid)
        if newpwd != confirmpwd:
            messages.warning(request,"New passwords and old passwords are not matched")
            return redirect('changepass')
        elif admin.password != oldpwd:
            messages.error(request,"Old passward that you enter is wrong")
            return redirect('changepass')
        elif oldpwd == newpwd:
            messages.warning(request,"Old password and new password should not be same")
            return redirect('changepass')
        else:
            admin.password = newpwd
            admin.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('admindash')
    return render(request, "admin/changepass.html",context)

def adminlogout(request):
    if "adminid" not in request.session:
        messages.error(request, "LOGIN First")
        return redirect('index')
    del request.session['adminid']
    messages.success(request, "Logged out successfully")
    return redirect('index')

def addcat(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    context = {
        'adminid' : adminid
    }
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if JobCategory.objects.filter(category_name__iexact = category_name):
            messages.warning(request, "Category already exists")
            return redirect('addcat')
        JobCategory.objects.create(category_name=category_name)
        messages.success(request,"New Category added")
        return redirect('addcat')
    return render(request,"admin/addcat.html",context)

def viewcat(request):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    adminid = request.session.get('adminid')
    cats = JobCategory.objects.all()
    context = {
        'adminid' : adminid,
        'categories': cats
    }
    return render(request,"admin/viewcat.html",context)

def deletecat(request, cid):
    if 'adminid' not in request.session:
        messages.error(request,"Login first")
        return redirect('login')
    try:
        cat = JobCategory.objects.get(id=cid)
        cat.delete()
        messages.success(request,"Category deleted successfully")
    except JobCategory.DoesNotExist:
        messages.error(request,"Category not found")
    return redirect('viewcat')

def viewjobseekers(request):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    jobseekers = Jobseeker.objects.all().select_related('user').prefetch_related('skills', 'educations', 'experiences')
    context = {
        'jobseekers': jobseekers
    }
    return render(request, "admin/viewjobseekers.html", context)

def editjobseeker(request, jid):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    js = Jobseeker.objects.get(id=jid)
    if request.method == "POST":
        js.first_name = request.POST.get('first_name')
        js.last_name = request.POST.get('last_name')
        js.email = request.POST.get('email')
        js.contact_no = request.POST.get('contact_no')
        js.save()
        messages.success(request, "Jobseeker updated successfully")
        return redirect('viewjobseekers')
    return render(request, "admin/editjobseeker.html", {"js": js})


def deletejobseeker(request, jid):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    try:
        js = Jobseeker.objects.get(id=jid)
        js.delete()
        messages.success(request, "Jobseeker deleted successfully")
    except Jobseeker.DoesNotExist:
        messages.error(request, "Jobseeker not found")
    return redirect('viewjobseekers')


def viewemployers(request):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    employers = Employer.objects.all().select_related('user', 'company')
    context = {
        'employers': employers
    }
    return render(request, "admin/viewemployers.html", context)



def deleteemployer(request, eid):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')
    try:
        emp = Employer.objects.get(id=eid)
        emp.delete()
        messages.success(request, "Employer deleted successfully")
    except Employer.DoesNotExist:
        messages.error(request, "Employer not found")
    return redirect('viewemployers')


def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "Login first")
        return redirect('login')

    # Collect stats
    total_jobseekers = Jobseeker.objects.count()
    total_employers = Employer.objects.count()
    total_categories = JobCategory.objects.count()
    total_jobs = Job.objects.count()
    total_enquiries = Enquiry.objects.count()

    context = {
        'total_jobseekers': total_jobseekers,
        'total_employers': total_employers,
        'total_categories': total_categories,
        'total_jobs': total_jobs,
        'total_enquiries': total_enquiries,
    }
    return render(request, "admin/admindash.html", context)

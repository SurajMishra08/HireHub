from django.urls import path
from . import views

urlpatterns = [
    path('jobseekerdash/',views.jobseekerdash, name='jobseekerdash'),
    path('jsupdate/',views.jsupdate, name='jsupdate'),
    path('apply/<id>',views.apply, name='apply'),
    path('jsprofile/',views.jsprofile, name='jsprofile'),
    path('logoutjobseeker/',views.logoutjobseeker, name='logoutjobseeker'),
    path('appliedjobs/',views.appliedjobs, name='appliedjobs'),
    path('save_education/',views.save_education, name='save_education'),
    path('save_experience/',views.save_experience, name='save_experience'),
    path('save_skill/',views.save_skill, name='save_skill'),
    path('save_additional/',views.save_additional, name='save_additional'),
    path('jschangepassword/',views.jschangepassword, name='jschangepassword'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('employerdash',views.employerdash,name='employerdash'),
    path('postjob',views.postjob,name='postjob'),
    path('viewjobs',views.viewjobs,name='viewjobs'),
    path('empprofile',views.empprofile,name='empprofile'),
    path('empupdate',views.empupdate,name='empupdate'),
    path('companydetails',views.companydetails,name='companydetails'),
    path('empchangepassword',views.empchangepassword,name='empchangepassword'),
    path('viewapplicant/<id>',views.viewapplicant,name='viewapplicant'),
    path('updatestatus/<appid>',views.updatestatus,name='updatestatus'),
    path('deljob/<id>',views.deljob,name='deljob'),
    path('editjob/<id>',views.editjob,name='editjob'),
    path('emplogout',views.emplogout,name='emplogout'),
]

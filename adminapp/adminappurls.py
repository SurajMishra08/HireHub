from django.urls import path
from . import views
urlpatterns =[
    path('admindash/',views.admindash,name='admindash'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('changepass/',views.changepass,name='changepass'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('delenq/<int:eid>/',views.delenq,name='delenq'),
    path('addcat/',views.addcat,name='addcat'),
    path('viewcat/',views.viewcat,name='viewcat'),
    path('deletecat/<int:cid>/', views.deletecat, name='deletecat'),
    path('viewjobseekers/', views.viewjobseekers, name='viewjobseekers'),
    path('editjobseeker/<int:jid>/', views.editjobseeker, name='editjobseeker'),
    path('deletejobseeker/<int:jid>/', views.deletejobseeker, name='deletejobseeker'),
    path('viewemployers/', views.viewemployers, name='viewemployers'),
    path('deleteemployer/<int:eid>/', views.deleteemployer, name='deleteemployer'),

]
from django.urls import path 
from.import views
from .views import user_login,req_blood,sign

urlpatterns=[
    path('',views.index, name='index'),
    path('donate/', views.register, name='donate'),
    path('appointment',views.appointment, name='appointment'),
    path('login',views.user_login,name='login'),
    path('overview',views.overview, name='overview'),
    path('find/',views.req_blood, name='find'),
    path('contact',views.contact,name='contact'),
    path('signup',views.sign,name='signup'),
    path('vision',views.vision, name='vision'),
    path('profile',views.donor_profile,name='profile'),
    path('submit_donation',views.submit_donation,name='submit_donation'),
    path('succ', views.success_reg,name='succ'),
    path('succ2',views.succ_sign,name='succ2'),
    path('logout',views.logout,name='logout'),
    path('succ3',views.succ_reg,name='succ3'),
    path('succ4',views.succ4,name='succ4'),

]
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
    path('profile',views.profile,name='profile'),
    path('submit_donation',views.submit_donation,name='submit_donation'),

]
from django.contrib import admin
from .models import *


@admin.register(Donors)
class admin_don (admin.ModelAdmin):
    list_display=('id','national_id','username','email','password')

@admin.register(Appointments)
class admin_reg(admin.ModelAdmin):
    list_display=('national','appointment_date','center_name','status')

@admin.register(USER)
class USERadmin(admin.ModelAdmin):
    list_display=('name','age','gender','location','phone','center')


@admin.register(REQUESTS)
class reqadmin(admin.ModelAdmin):
    list_display=('name','idNumber','email','phone','gender','bloodType','location','address')

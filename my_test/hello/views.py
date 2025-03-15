from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from.forms import DonoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

client_id:str
authentication =False
from django.core.mail import send_mail
from django.conf import settings


def user_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email','')
        password = request.POST.get('password','')
      
        if Auth(email,password):
            request.session['client_id'] = email
            request.session['authentication'] = True
            return redirect('index')
        
        else:
            print("please enter an existing email address")
            return render(request,'test.html',{'Error':'Invalid credentials'})

       
    else:

        return render(request, 'test.html')
    
def index (request):
    authentication=request.session.get('authentication',False)
    client_id=request.session.get('client_id',None)

    if authentication and client_id:
        data = Donors.objects.filter(email=client_id).first()

        
        content = {'user': data, "auth": authentication}
        print(data, authentication)
        return render(request, 'index.html', content)
    else:
       return render(request, 'index.html', {'auth':False}) 
    

def donate (request):
    template=loader.get_template('donate.html')
    return HttpResponse(template.render())

@login_required

def profile(request):
    user=request.user
    try:
        donor=Donors.objects.get(email=user.email)
        national_id=donor.national_id
    except Donors.DoesNotExist:
        national_id="N/A"

    context={
        'username':user.username,
        'email':user.email,
        'national_id':national_id,
    }
    return render(request,'profile.html',context)
def appointment(request):
    template=loader.get_template('appointment.html')
    return HttpResponse(template.render())

def overview(request):
    template=loader.get_template('overview.html')
    return HttpResponse(template.render())

def find(request):
    template=loader.get_template('find.html')
    return HttpResponse(template.render())

def contact(request):
    template=loader.get_template('contact.html')
    return HttpResponse(template.render())

def signup(request):
    template=loader.get_template('signup.html')
    return HttpResponse(template.render())

def vision(request):
    template=loader.get_template('vision.html')
    return HttpResponse(template.render())




def register(request):
    if request.method =='POST':
        name=request.POST.get('name','')
        age=request.POST.get('age','')
        id_number=request.POST.get('id_number','')
        gender=request.POST.get('gender','')
        location=request.POST.get('location','')
        phone=request.POST.get('phone','')
        center=request.POST.get('center','')
    
        new=USER(name=name,age=age, id_number=id_number, location=location,phone=phone,center=center)
        new.save()
        return redirect(request,'appointment')
       
        
    return render(request, 'donate.html',{})

def req_blood(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        idNumber=request.POST.get('idNumber','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        gender=request.POST.get('gender','')
        bloodType=request.POST.get('bloodType','')
        location=request.POST.get('location','')
        address=request.POST.get('address','')

        if REQUESTS.objects.filter(email=email).exists():
            messages.error(request,'This email is alreaady registered. Please use a different email!')
            return redirect('find')

        req=REQUESTS(name=name, idNumber=idNumber,email=email,phone=phone,gender=gender,bloodType=bloodType,location=location,address=address)
        req.save()

        messages.success(request,'Your request has been submitted succsefully!')
        return redirect ('index')

    return render(request, 'find.html')

def sign(request):
    if request.method=='POST':
        national_id=request.POST.get('national_id','')
        username=request.POST.get('username','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')

        if Donors.objects.filter(email=email).exists():
            return render(request,'signup.html',{'error':'Email already exists!'})

        hashed_password=make_password(password)

        sig=Donors(
            national_id=national_id,
            username=username,
            email=email,
            password=password
        )
        sig.save()

        subject='Welcome to Donor Hub!'

        message=f'''
        Hello {username},
        You have successsfully created an acoount in donorhub.
        Together, let's save humanity by donating blood .
        thankyiu for joining us
        best regards,
        Donor Hub team
        '''
        from_email=settings.DEFAULT_FROM_EMAIL
        recipient_list=[email]

        try:
            send_mail(subject, message,from_email,recipient_list)
            print("Email sent successfully!")
        except Exception as e:
            print(f"failed to send the email:{e}")

        return redirect('login')
    return render(request,'signup.html')

def user_logout(request):
    request.session.flush()
    return redirect('test')

def submit_donation(request):
    if request.method =='POST':
        user=request.user
        id_number=request.POST.get('id_number','')
        subject='Donation Registration Successful'
        message=f'''
        Hello{user.username},
        Thank you for registering as a donor!Your National ID is {id_number}.
        You are scheduled to attend on :
        We appreciate your contribution to saving lives .

        Best regards ,
        Donor Hub Team
        '''
        from_email=settings.DEFAULT_FROM_EMAIL
        recipient_list=[user.email]

        send_mail(subject, message,from_email,recipient_list)

        return render(request,'donor.html')














from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from.forms import DonoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.conf import settings 
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

client_id:str
authentication =False




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


def donor_profile(request):
    if 'client_id' not in request.session:
        return redirect('login')
    
    email=request.session['client_id']

    try:
        donor=Donors.objects.get(email=email)
        national_id=donor.national_id

        user_info=USER.objects.get(id_number=national_id)
    except Donors.DoesNotExist:
        return render(request,'error.html',{'error':'User information not found'})
    
    context={
        'national_id':donor.national_id,
        'username1':donor.username,
        'email':donor.email,

        'name':user_info.name,
        'gender':user_info.gender,
        'location':user_info.location,
        'phone':user_info.phone,
    }
    return render(request,'profile.html',context)

    
def appointment(request):
    if request.method=='POST':
        if 'client_id' not in request.session:
            return redirect('login')
        
        user_email=request.session['client_id']
        appointment_date=request.POST.get('appointmentDate','')

        try:
            donor=Donors.objects.get(email=user_email)
        except Donors.DoesNotExist:
            return render(request,'appointment.html',{'error':'Donor not found. Please sign up first.'})
        
        subject='Appointment confirmation'
        message=f'''
        Hello{donor.username},
        Your appointment to donate blood has been scheduled successsfully.
        Appointment Date: {appointment_date}
        Reporting Time:8:00 AM

        Please arrrive at the registration center on time .

        best regards ,
        Donor Hub Team 
        '''

        from_email=settings.DEFAULT_FROM_EMAIL
        recipient_list=[user_email]

        try:
            send_mail(subject,message,from_email,recipient_list)
            print("appointment confirmation email sent successfully")
            return redirect ('succ4')
        except Exception as e:
            print(f"Failed to send email:{e}")
            return render(request,'appointment.html',{'error':'Failed to send confirmation email.please try again'})
        
        
    else:
        return render(request, 'appointment.html')
        
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
    if request.method == 'POST':
        name = request.POST.get('name', '')
        age = request.POST.get('age', '')
        
        gender = request.POST.get('gender', '')
        location = request.POST.get('location', '')
        phone = request.POST.get('phone', '')
        center = request.POST.get('center', '')

        if 'client_id' in request.session:
            email=request.session['client_id']
        else:
            return render(request,'donate.html',{'error':'You must be logged in to register as a donor.'})
        
        try:
            donor=Donors.objects.get(email=email)
            national_id=donor.national_id
        except Donors.DoesNotExist:
            return render(request,'donate.html',{'error':"Donor not found. Please sign up first."})
        
        if USER.objects.filter(id_number=national_id).exists():
            return render(request,'donate.html',{'error':'You are already registered as a Donor.'})
        
        new_donor=USER(
    
            name=name,
            age=age,
            id_number=national_id,
            gender=gender,
            location=location,
            phone=phone,
            center=center
        )
        new_donor.save()
        

        return render(request,'succ3.html',{'name':name,'center':center,})
    
    return render(request,'donate.html',{})


def succ_reg (request):
    template=loader.get_template('succ3.html')
    return HttpResponse(template.render())    


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

        
        return redirect ('succ')

    return render(request, 'find.html')

def success_reg(request):
    template=loader.get_template('succ.html')
    return HttpResponse(template.render())



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

        return redirect('succ2')
    return render(request,'signup.html')

def succ_sign(request):
    template=loader.get_template('succ2.html')
    return HttpResponse(template.render())

def logout(request):
    request.session.flush()
    return redirect('signup')

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
    
  
    
    
def succ4(request):
    template=loader.get_template('succ4.html')
    return HttpResponse(template.render())

"""openai.api_key=''

@csrf_exempt
def chatbot(request):
    if request.method=='POST':
        user_message=request.POST.get('message','')

        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You are a helpful assistant that provides information about blood donation"},
                {"role":"user","content":user_message},

            ]

        )

        bot_response=response['choices'][0]['message']['content']
        return JsonResponse({'response':bot_response})
    return JsonResponse({'error':'Invalid request method'}, status=400)
    
"""














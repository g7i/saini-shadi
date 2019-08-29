from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Register
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

def home(request):
    global USER
    USER = request.user
    profiles = User.objects.all()
    profiles = profiles.filter(registered = True)
    profiles = profiles[:6]
    return render(request,'index.html',{'profiles':profiles})


def signup(request):
    response_data = {}
    if request.method == 'POST':
            try:
                request.session['otp_verify']
            except:
                response_data = {'Message':'Please Enter your no. and verify with OTP'}
                return JsonResponse(response_data)
            if request.session['otp_verify'] == 'yes':
                if request.POST['password1']==request.POST['password2']:
                    try:
                        user = User.objects.get(username=request.POST['username'])
                        response_data = {'Message':'User already exists..'}
                        return JsonResponse(response_data)

                    except User.DoesNotExist:
                        User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],mobile=int(request.POST['phone_number']))
                        user = auth.authenticate(username=request.POST['username'],password=request.POST['password1'])
                        auth.login(request, user)
                        response_data = {'Message':'User created Successfully..'}
                        return JsonResponse(response_data)

                else:
                    response_data = {'Message':'Password didn\'t match..'}
                    return JsonResponse(response_data)
            
            else:
                response_data = {'Message':'Please verify your number..'}
                return JsonResponse(response_data)

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        try:
            user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
            if user is None:
                raise Exception
        except:
            try:
                user = User.objects.get(username=request.POST['username'],password=request.POST['password'])
            except:
                user = None
        if user is not None:
            auth.login(request,user)
            if user.published:  
                return redirect('home')
            else:
                return redirect('edit')
        else:
            return render(request,'login.html',{'error':'Username or Password is incorrect..'})
    else:
        return render(request, 'login.html')

def forget(request):
    if request.method == 'POST':
            try:
                request.session['otp_verify']
            except:
                response_data = {'Message':'Please Enter your no. and verify with OTP'}
                return JsonResponse(response_data)
            if request.session['otp_verify'] == 'yes':
                if request.POST['password1']==request.POST['password2']:
                    try:
                        user = User.objects.get(username=request.POST['username'],mobile=int(request.POST['phone_number']))
                        user.password=request.POST['password1']
                        user.save()
                        auth.login(request, user)
                        response_data = {'Message':'Password Changed Successfully..'}
                        return JsonResponse(response_data)

                    except User.DoesNotExist:
                        response_data = {'Message':'User Doesnot Exists..'}
                        return JsonResponse(response_data)

                else:
                    response_data = {'Message':'Password didn\'t match..'}
                    return JsonResponse(response_data)
            
            else:
                response_data = {'Message':'Please verify your number..'}
                return JsonResponse(response_data)
    else:
        return render(request, 'forget.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def profile(request):
    global USER
    USER = request.user
    return render(request,'profile.html')

@login_required(login_url='login')
def detail(request,id):
    if not request.user.registered:
            return render(request,'result.html',{'error':'Please get registered with sainishadi.com to view profiles. Click on Register in Main Menu.'})
    return render(request,'detail.html',{'profile':get_object_or_404(User,pk=id)})

def contact(request):
    return render(request,'contact.html')

def delete(request):
    user = request.user
    user.delete()
    return redirect('home')

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        if not request.user.registered:
            return render(request,'result.html',{'error':'Please get registered with sainishadi.com to continue your search. Click on Register in Main Menu.'})
        city = request.POST['city']
        state = request.POST['state']
        gender = request.POST['gender']
        age_group = request.POST['age']
        objs = User.objects.all()
        results= []
        if state:
            objs = objs.filter(state=state)
        if city:
            objs = objs.filter(city=city)
        if gender:
            objs = objs.filter(gender=gender)
        if age_group:
            if age_group == "1":
                for obj in objs:
                    if obj.age==18 or obj.age==19 or obj.age==20 or obj.age==21:
                        results.append(obj)
            if age_group == "2":
                for obj in objs:
                    if obj.age==22 or obj.age==23 or obj.age==24 or obj.age==25:
                        results.append(obj)
            if age_group == "3":
                for obj in objs:
                    if obj.age==26 or obj.age==27 or obj.age==28 or obj.age==29:
                        results.append(obj)
            if age_group == "4":
                for obj in objs:
                    if obj.age==30 or obj.age==31 or obj.age==32 or obj.age==33:
                        results.append(obj)
            if age_group == "5":
                for obj in objs:
                    if obj.age==34 or obj.age==35 or obj.age==36 or obj.age==37:
                        results.append(obj)
        else:
            results = objs
        if not results:
            return render(request,'result.html',{'profiles':results,'error':'No Profile Matched Your Query..'})
        return render(request,'result.html',{'profiles':results})


def edit(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.father_name = request.POST['father_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.status = request.POST['status']
        user.gender = request.POST['gender']
        user.job_type = request.POST['job_type']
        user.job_desc = request.POST['job_desc']
        user.manglik = request.POST['manglik']
        user.self_gotra = request.POST['self_gotra']
        user.mother_gotra = request.POST['mother_gotra']
        user.dadi_gotra = request.POST['dadi_gotra']
        user.nani_gotra = request.POST['nani_gotra']
        user.edu = request.POST['edu']
        user.address = request.POST['address']
        user.city = request.POST['city']
        user.state = request.POST['state']
        if request.POST['dob']:
            user.dob = request.POST['dob']
        user.image = request.FILES.get('image',user.image)
        user.drink = request.POST['drink']
        user.smoking = request.POST['smoking']
        user.colour = request.POST['colour']
        user.physique = request.POST['physique']
        if not request.POST['feet']=="None":
            user.height_foot = request.POST['feet']
        if not request.POST['inch']=="None":
            user.height_inch = request.POST['inch']
        user.published = True
        user.save()
        return redirect('profile')
    else:
        return render(request,'edit.html')

import requests
import urllib.parse
from django.http import JsonResponse

def send_otp(request):
    response_data = {}
    if request.method == "POST" and request.is_ajax:
        user_phone = request.POST['phone_number']
        url = "http://2factor.in/API/V1/6fef1ba2-be3b-11e9-ade6-0200cd936042/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
        response = requests.request("GET", url)
        data = response.json()
        request.session['otp_session_data'] = data['Details']
        # otp_session_data is stored in session.
        response_data = {'Message':'Success'}
    else:
        response_data = {'Message':'Failed'}
    
    return JsonResponse(response_data)

def otp_verification(request):
    response_data = {}
    if request.method == "POST" and request.is_ajax:
        user_otp = request.POST['otp']
        url = "http://2factor.in/API/V1/6fef1ba2-be3b-11e9-ade6-0200cd936042/SMS/VERIFY/" + request.session['otp_session_data'] + "/" + user_otp + ""
        response = requests.request("GET", url)		
        data = response.json()
        if data['Status'] == "Success":
            # logged_user.is_active = True

            response_data = {'Message':'Success'}
            request.session['otp_verify'] = 'yes'
        else:
            response_data = {'Message':'Failed'}
            request.session['otp_verify'] = 'no'
    return JsonResponse(response_data)

from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = 'wUXm4Uzybte7klQ7'

def register(request):
    if request.user.registered:
        return redirect('home')
    if not request.user.published:  
        return redirect('edit')
    reg = Register.objects.create(user=request.user)
    global USER
    USER = request.user
    param_dict = {
            'MID':'tfbWmY61557297752157',
            'ORDER_ID': f'{reg.id}',
            'TXN_AMOUNT':'101',
            'CUST_ID':request.user.username.replace(' ','__'),
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://ec2-13-234-30-158.ap-south-1.compute.amazonaws.com/handlerequest/',
        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html' , {'param_dict' : param_dict})

@csrf_exempt
def handlerequest(request):

        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                reg = get_object_or_404(Register,pk=int(response_dict['ORDERID']))
                reg.status = 'Yes'
                reg.save()
                global USER
                USER.registered = True
                USER.save()
        return render(request, 'paystatus.html',{'response':response_dict})

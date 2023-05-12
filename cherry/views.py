from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from cherry.models import *
from cherry.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')






def registration(request):
    ufd=UserForm()
    pfd=ProfileForm()
    d={'ufd':ufd,'pfd':pfd}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            send_mail('Registration',
                      'Successfully Registation is Done',
                      'deviprasadisaka@gmail.com',
                      [NSUO.email],
                      fail_silently=True)
            return HttpResponse('Registration is Done Successfully')
        else:
            return HttpResponse('Invalid Data is Entered')
            
    return render(request,'registration.html',d)



def devi_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')
        
    return render(request,'devi_login.html')
@login_required
def devi_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO,'PO':PO}
        return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is Changed Successfully')
    return render(request,'change_password.html')



def forget_password(request):
    if request.method=='POST':
        username=request.POST['username']
        pw=request.POST['pw']
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is Changed Successfully')
    return render(request,'forget_password.html')

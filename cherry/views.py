from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from cherry.models import *
from cherry.forms import *
# Create your views here.

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

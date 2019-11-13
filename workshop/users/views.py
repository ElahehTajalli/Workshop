# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.mail import EmailMessage
import uuid
from users.models import Profile
from django.template.loader import render_to_string
from tasks import send_mail
from django.contrib.sites.shortcuts import get_current_site




# Create your views here.
def signup(request):
    if request.method == 'POST':
        try:
            u = User.objects.create_user (
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email']
            )

            p = Profile(
                user=u,
                verify_id = uuid.uuid4()
            )
            

        except:
            return render(
                request,
                'users/signup.html',
                context= {
                    'error':'Duplicate'
                },
                status=400
            )
        u.save()
        p.save()
        current_site = get_current_site(request)  
        message = render_to_string('users/verify.html', {
                'token': p.verify_id,
                'domain': current_site.domain,
            })
        send_mail.delay('Verify Email', message, u.email)
        # login(request, u)    
        return render(
            request,
            'users/signup.html',
            context = {
                'add' : "Please check your Email!"
            }
        )

    elif request.method == 'GET':
        return render(
            request,
            'users/signup.html',
        )



def login_view(request):
    if request.method == 'GET':
        return render(
            request,
            'users/login.html',
            context={
                'error': '',
            }
        )

    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if  user is not None:
            p = Profile.objects.get(
                user = user
            )

            if p.verify :
                login(request, user)
                return redirect(
                    'list/'
                )

            return render(
                request,
                'users/login.html',
                context = {
                    'error' : "Your email not verified!!"
                }
            )

        else :
            return render(
                request,
                'users/login.html',
                context={
                    'error': 'Not Found'
                },
                status= 404
            )
    elif request.method == 'GET':
        return render(
            request,
            'users/login.html',
        )        



def verify(request, verify_id=None):
    p = Profile.objects.get(
        verify_id = verify_id
    )

    if p:
        p.verify = True
        p.save()
        return redirect(
            'list/'
        )

    return HttpResponse(
            'Not Found',
            status=404
        )    



def user_list(request, verify_id=None):
    if request.user.is_authenticated:
        return render(
            request,
            'users/userList.html',
            context={
                'users': User.objects.all()
            }
            )            

    return redirect(
            'login/'
            )  
    



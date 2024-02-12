from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from myProject.forms import *
from django.contrib import messages

from django.contrib.auth import get_user_model
from myApp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('mySigninPage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')


def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('mySigninPage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signupPage.html', {'form': form})


def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboardPage')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPage.html', {'form': form})


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('mySigninPage')

def dashboardPage(request):

    return render(request, 'dashboardPage.html')
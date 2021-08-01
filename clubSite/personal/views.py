from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse

def userProfile(request):
    context = {}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
        object = request.user
        context['username'] = object.username
        context['email'] = object.email
        context['last_login'] = str(object.last_login).split(".")[0]
    return render(request, 'personal/userProfile.html', context=context)

def editUserInfo(request):
    object = request.user
    if request.POST['username']:
        object.username = request.POST['username']
    if request.POST['pass']:
        object.set_password(request.POST['pass'])
    if request.POST['email']:
        object.email = request.POST['email']
    object.save()
    return HttpResponseRedirect(reverse('personal:userProfile'))

def login(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'personal/login.html', context=context)

def authenticateAccount(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        raise Http404("The account does not exist")

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('personal:login'))

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
# from organize.models import User

# Create your views here.

def my_login(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='login.html', context=context)

def my_logout(request):
    logout(request)
    return redirect('login')

def sign_up(request):
    return render(request, template_name='sign_up.html')

def add_user(request):
    context = {}
    if request.method == 'POST':

        new = request.POST.get('username')
        guser = User.objects.filter(username=new)
        print(guser)
        if guser:
            context['error'] = 'Username have already!'
            print('111111111111')
            return render(request, template_name='sign_up.html', context=context)
        else:
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('Email'),
                request.POST.get('password')
            )
            user.first_name = request.POST.get('Firstname')
            user.last_name = request.POST.get('Lastname')
            user.save()
            return redirect('login')
    else:
        return redirect('login')



from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from poll.models import Poll, Pollchoice,Pollvote
from django.contrib.auth.models import User
# from organize.models import User
import datetime


# Create your views here.

def home(request):

    polll = Poll.objects.all()
    currentDT = datetime.datetime.now()
    pollnow1 = Poll.objects.filter(end_date__gt=currentDT)
    pollnow2 = Poll.objects.filter(end_date=currentDT,end_time__gte=currentDT,start_time__lte=currentDT)
    polllate1 = Poll.objects.filter(end_date__lt=currentDT)
    polllate2 = Poll.objects.filter(end_date=currentDT,end_time__lt=currentDT)
    context={
        'polllate1':polllate1,
        'polllate2':polllate2,
        'pollnow1':pollnow1,
        'pollnow2':pollnow2,

    }

    return render(request, template_name='poll/home.html',context=context)

@login_required
def add_poll(request):
    return render(request, template_name='poll/add_poll.html')

@login_required
def my_poll(request):
    return render(request, template_name='poll/my_poll.html')

@login_required
def save_poll(request):

    # polll = Poll.objects.filter(create_by=4)
    # print(polll)
    userr = request.user
    # userrr = User.objects.filter(username=userr)
    # print(userrr)
    if request.method == 'POST':
        title=request.POST.get('name')
        poll = Poll.objects.create(
            subject=request.POST.get('name'),
            detail=request.POST.get('detail'),
            start_date=request.POST.get('datestart'),
            end_date=request.POST.get('dateend'),
            password=request.POST.get('password'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            create_by_id=userr.id
        )
        

        choice1 = Pollchoice.objects.create(
            subject=request.POST.get('choice1'),
        )

        choice2 = Pollchoice.objects.create(
            subject=request.POST.get('choice2'),
        )

        choice3 = Pollchoice.objects.create(
            subject=request.POST.get('choice3'),
        )

        polll = Poll.objects.get(subject=title)

        c1 = Pollchoice.objects.get(subject=choice1.subject)
        c1.polls.add(polll)
        c2 = Pollchoice.objects.get(subject=choice2.subject)
        c2.polls.add(polll)
        c3 = Pollchoice.objects.get(subject=choice3.subject)
        c3.polls.add(polll)

    return redirect('home')

def view_detail(request,poll_id):
    user = request.user
    polls = Poll.objects.filter(id=poll_id)
    pollss = Poll.objects.get(id=poll_id)
    choice = pollss.pollchoice_set.all()
    context={
        'polls':polls,
        'choice':choice
    }
    return render(request, template_name='poll/view_detail.html', context=context)

def my_poll(request):
    user = request.user
    allpoll = Poll.objects.filter(create_by_id=user.id)
    context={
        'allpoll':allpoll
    }

    return render(request, template_name='poll/my_poll.html', context=context)


def poll_vote(request,poll_id):

    userr = request.user
    if request.method == 'POST':
        poll_choice_id = request.POST.get('choice_no',None)
        poll_vote=Pollvote.objects.create(
            poll_id=poll_id,
            poll_choice_id=poll_choice_id,
            user_id=userr.id
        )
    return redirect('home')

def edit_poll(request,poll_id):
    
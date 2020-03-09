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
@login_required
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
    userr = request.user
    have = Pollvote.objects.filter(poll_id=poll_id,user_id=userr.id)
    polls = Poll.objects.filter(id=poll_id)
    pollss = Poll.objects.get(id=poll_id)
    choice = pollss.pollchoice_set.all()

    poll = Pollchoice.objects.filter(polls=poll_id)
    choice1 = poll[0].poll_choice_id
    choice2 = poll[1].poll_choice_id
    choice3 = poll[2].poll_choice_id

    choicename1 = poll[0].subject
    choicename2 = poll[1].subject
    choicename3 = poll[2].subject

    count1 = (Pollvote.objects.filter(poll_id=poll_id,poll_choice_id=choice1)).count()
    count2 = (Pollvote.objects.filter(poll_id=poll_id,poll_choice_id=choice2)).count()
    count3 = (Pollvote.objects.filter(poll_id=poll_id,poll_choice_id=choice3)).count()

    context={
        'polls':polls,
        'choice':choice,
        'count1':count1,
        'count2':count2,
        'count3':count3,
        'choicename1':choicename1,
        'choicename2':choicename2,
        'choicename3':choicename3

    }

    if have:
        context['error'] = 'You had voted already!'
        return render(request, template_name='poll/view_detail.html', context=context)
    else:
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
    poll = Poll.objects.filter(id=poll_id)
    epoll = Poll.objects.get(id=poll_id)

    choice ={}
    if request.method == 'POST':
            epoll.subject=request.POST.get('name')
            epoll.detail=request.POST.get('detail')
            epoll.start_date=request.POST.get('datestart')
            epoll.end_date=request.POST.get('dateend')
            epoll.password=request.POST.get('password')
            epoll.start_time=request.POST.get('start_time')
            epoll.end_time=request.POST.get('end_time')

            epoll.save()
            

            choice = Pollchoice.objects.filter(polls=poll_id)

    context={
        'poll':poll,
        'choice':choice
    }
    return render(request, template_name='poll/edit_poll.html',context=context)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from poll.models import Poll, Pollchoice,Pollvote
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

import datetime


# Create your views here.
@login_required
def home(request):

    polll = Poll.objects.all()
    currentDT = datetime.datetime.now()
    pollnow1 = (Poll.objects.filter(end_date__gt=currentDT))
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

    userr = request.user
    if request.method == 'POST':
        title=request.POST.get('name')
        try:
            poll = Poll.objects.create(
            subject=request.POST.get('name'),
            detail=request.POST.get('detail'),
            start_date=request.POST.get('datestart'),
            end_date=request.POST.get('dateend'),
            password=request.POST.get('password'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            create_by_id=userr.id,
            picture=request.FILES['document'].name  
        )
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)

        except:
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

    check = Poll.objects.filter(id=poll_id)
    if check[0].password:

        context={
            'check':check,
        }
        return render(request, template_name='poll/check_password.html', context=context)

    else:

        # check vote already
        userr = request.user
        have = Pollvote.objects.filter(poll_id=poll_id,user_id=userr.id)
        polls = Poll.objects.filter(id=poll_id)
        pollss = Poll.objects.get(id=poll_id)
        choice = pollss.pollchoice_set.all()

        # total vote 
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

        # vote closed
        currentDT = datetime.datetime.now()
        polllate1 = Poll.objects.filter(end_date__lt=currentDT)
        polllate2 = Poll.objects.filter(end_date=currentDT,end_time__lt=currentDT)
        close = 0
        for i in range (0,len(polllate1)):
            if polllate1[i].id==poll_id:
                close=close+1
            else:
                close=close+0

        for i in range (0,len(polllate2)):
            if polllate2[i].id==poll_id:
                close=close+1
            else:
                close=close+0

        context={
            'polls':polls,
            'choice':choice,
            'count1':count1,
            'count2':count2,
            'count3':count3,
            'choicename1':choicename1,
            'choicename2':choicename2,
            'choicename3':choicename3,
        }

        if have:
            context['error'] = 'You had voted already!'
            return render(request, template_name='poll/view_detail.html', context=context)
        elif close>0:
            context['closed'] = 'This poll is closed.'
            return render(request, template_name='poll/view_detail.html', context=context)
        else:
            return render(request, template_name='poll/view_detail.html', context=context)
        



def view_password(request,poll_id):
    context={}
    checkk = Poll.objects.filter(id=poll_id)
    if request.method == 'POST':
        
        check = Poll.objects.get(id=poll_id)
        password = request.POST.get('check')
        if check.password==password:
            # check vote already
            userr = request.user
            have = Pollvote.objects.filter(poll_id=poll_id,user_id=userr.id)
            polls = Poll.objects.filter(id=poll_id)
            pollss = Poll.objects.get(id=poll_id)
            choice = pollss.pollchoice_set.all()

            # total vote 
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

            # vote closed
            currentDT = datetime.datetime.now()
            polllate1 = Poll.objects.filter(end_date__lt=currentDT)
            polllate2 = Poll.objects.filter(end_date=currentDT,end_time__lt=currentDT)
            close = 0
            for i in range (0,len(polllate1)):
                if polllate1[i].id==poll_id:
                    close=close+1
                else:
                    close=close+0

            for i in range (0,len(polllate2)):
                if polllate2[i].id==poll_id:
                    close=close+1
                else:
                    close=close+0

            context={
                    'polls':polls,
                    'choice':choice,
                    'count1':count1,
                    'count2':count2,
                    'count3':count3,
                    'choicename1':choicename1,
                    'choicename2':choicename2,
                    'choicename3':choicename3,
            }

            if have:
                context['error'] = 'You had voted already!'
                return render(request, template_name='poll/view_detail.html', context=context)
            elif close>0:
                context['closed'] = 'This poll is closed.'
                return render(request, template_name='poll/view_detail.html', context=context)
            else:
                return render(request, template_name='poll/view_detail.html', context=context)
        
        else:
            context['error'] = 'Password is wrong!'

            context['checkk'] = checkk
            return render(request, template_name='poll/check_password.html', context=context)

    


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
    context={
        'poll':poll,
    }

    if request.method == 'POST':
        try:
            epoll.subject=request.POST.get('name')
            epoll.detail=request.POST.get('detail')
            epoll.start_date=request.POST.get('datestart')
            epoll.end_date=request.POST.get('dateend')
            epoll.password=request.POST.get('password')
            epoll.start_time=request.POST.get('start_time')
            epoll.end_time=request.POST.get('end_time')
            epoll.picture=request.FILES['document'].name
            epoll.save()
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
            

        except:
            epoll.subject=request.POST.get('name')
            epoll.detail=request.POST.get('detail')
            epoll.start_date=request.POST.get('datestart')
            epoll.end_date=request.POST.get('dateend')
            epoll.password=request.POST.get('password')
            epoll.start_time=request.POST.get('start_time')
            epoll.end_time=request.POST.get('end_time')
            epoll.save()

        context['success'] = 'Edit success!'

    
    return render(request, template_name='poll/edit_poll.html',context=context)


def delete_poll(request,poll_id):
    context={}
    poll = Poll.objects.get(id=poll_id)
    poll.delete()
    context['success'] = 'Delete poll success!'
    return render(request, template_name='poll/my_poll.html',context=context)

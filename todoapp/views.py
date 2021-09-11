from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from todoapp.forms import LoginForm,AddForm,AddForm,UpdateForm,SignupForm
from todoapp.models import TodoListModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

from django.conf import settings as conf_settings
page_size = conf_settings.PAGE_SIZE

@login_required (login_url='/login')
def home(request):


    sdata=TodoListModel.objects.filter(user=request.user,status='START')
    paginator=Paginator(sdata,page_size)
    page_number = request.GET.get('page')

    try:
        sdata=paginator.page(page_number)
    except PageNotAnInteger:
        sdata=paginator.page(1)
    except EmptyPage:
        sdata=paginator.page(paginator.num_pages)
    return render(request,'todoapp/home.html',{'sdata':sdata})
from django.contrib.auth import authenticate,logout,login

def loginview(request):
    lform=LoginForm()
    if request.method=='POST':
        lform=LoginForm(request.POST)
        if lform.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/home')
            else:
                return redirect('/login')

    lform=LoginForm()
    return render(request,'todoapp/login.html',{'lform':lform})
@login_required(login_url='/login')
def add_view(request):
    form=AddForm()
    if request.method=='POST':
        form=AddForm(request.POST)
        if form.is_valid():
            form.save()
            form=AddForm()
            return render(request,'todoapp/add_list.html',{'form':form})

    return render(request,'todoapp/add_list.html',{'form':form})



# update view for details
@login_required(login_url='/login')
def delete_view(request, id):
    ddata=TodoListModel.objects.get(id=id)
    ddata.delete()
    return redirect('/tlist')

@login_required(login_url='/login')
def update_view(request,id):
    uform=UpdateForm()
    if request.method=='POST':
        uform=UpdateForm(request.POST)
        if uform.is_valid():
            nstatus=request.POST['status']
            udata=TodoListModel.objects.get(id=id)
            udata.status=nstatus
            udata.save()
            return redirect('/tlist')
    return render(request,'todoapp/update.html',{'uform':uform})

def logoutview(request):
    logout(request)
    return render(request,'todoapp/logout.html')

def signup_view(request):
    sform=SignupForm()
    if request.method=='POST':
        sform=SignupForm(request.POST)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        if sform.is_valid():
            pdata=User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            )
            pdata.save()
            pdata.set_password(pdata.password)
            pdata.save()
            sform=SignupForm()
            return render(request,'todoapp/signup.html',{'sform':sform})
    return render(request,'todoapp/signup.html',{'sform':sform})
def done_view(request):
    done_list=TodoListModel.objects.filter(user=request.user,status='DONE')
    paginator=Paginator(done_list,3)
    page_number = request.GET.get('page')

    try:
        done_list=paginator.page(page_number)
    except PageNotAnInteger:
        done_list=paginator.page(1)
    except EmptyPage:
        done_list=paginator.page(paginator.num_pages)
    return render(request,'todoapp/done_list.html',{'done_list':done_list})

def list_view(request):
    total_list=TodoListModel.objects.filter(user=request.user)
    paginator=Paginator(total_list,3)
    page_number = request.GET.get('page')

    try:
        total_list=paginator.page(page_number)
    except PageNotAnInteger:
        total_list=paginator.page(1)
    except EmptyPage:
        sdata=paginator.page(paginator.num_pages)
    return render(request,'todoapp/total_list.html',{'total_list':total_list})

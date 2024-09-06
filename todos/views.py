from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def get_showing_todos(request,all_todo):

    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return all_todo.filter(status=True)
        if request.GET.get('filter') == 'incompleted':
            return all_todo.filter(status=False)
        
    return all_todo


@login_required(login_url='login')
def create_todo(request):
    all_todo = Todo.objects.filter(user=request.user)
    completed_count = all_todo.filter(status=True).count()
    incompleted_count = all_todo.filter(status=False).count()
    all_count = all_todo.count()
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo=Todo(user=request.user,todo_name=task)
        new_todo.save()
        return redirect('create_todo')
    all_todo = Todo.objects.filter(user=request.user)
    context = {
        'all_todo':get_showing_todos(request,all_todo),
        'completed_count':completed_count,
        'incompleted_count':incompleted_count,
        'all_count':all_count
    }
    return render(request,'todo.html',context)


def todo_delete(request,name):
    get_todo=get_object_or_404(Todo,user=request.user,todo_name=name)
    context = {
        'get_todo':get_todo
    }
    if request.method == 'POST':
        get_todo.delete()
        return redirect('create_todo')
    return render(request,'delete_alerts.html',context)



def update(request,name):
    get_todo = Todo.objects.get(user=request.user,todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('create_todo')



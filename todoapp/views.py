from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm


def home(request):
    return render(request, 'todoapp/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todoapp/signup_user.html',
                              {'form': UserCreationForm(),
                               'error': 'That username has already taken. Please choose a new username'})

        else:
            return render(request, 'todoapp/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def current_todos(request):
    return render(request, 'todoapp/current_todos.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todoapp/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/login_user.html',
                          {'form': AuthenticationForm(), 'error': 'user or password did not match'})
        else:
            login(request, user)
            return redirect('current_todos')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todoapp/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todoapp/create_todo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})

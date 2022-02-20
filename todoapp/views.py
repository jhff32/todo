from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def signup_user(request):

    return render(request, 'todoapp/signup_user.html', {'form': UserCreationForm()})
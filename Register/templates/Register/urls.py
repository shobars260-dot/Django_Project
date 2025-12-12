from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    form = RegisterForm()
    return render(request, 'Register/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomRegistrationForm

# 1. មុខងារឡុកអ៊ីន
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 2. មុខងារចុះឈ្មោះ
def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# 3. មុខងារចាកចេញ
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('/')
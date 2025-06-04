from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm

# Create your views here.
def index(request):
    """
    Render the home page of the PenniniBet application.
    """
    return render(request, 'bolao/pages/index.html')

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'bolao/auth/register.html', {'form': form})

def login_view(request):
    """
    Handle user login with username or email.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('index')
    else:
        form = UserLoginForm()
    
    return render(request, 'bolao/auth/login.html', {'form': form})

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, 'Logout realizado com sucesso!')
    return redirect('index')

def events(request):
    """
    Render the events page.
    """
    return render(request, 'bolao/pages/events.html')

def orders(request):
    """
    Render the orders page.
    """
    return render(request, 'bolao/pages/orders.html')

def settings(request):
    """
    Render the settings page.
    """
    return render(request, 'bolao/pages/settings.html')
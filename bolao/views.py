from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    """
    Render the home page of the PenniniBet application.
    """
    return render(request, 'bolao/index.html')

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'bolao/auth/register.html', {'form': form})

def login_view(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'bolao/auth/login.html', {'form': UserCreationForm()})

def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('index')
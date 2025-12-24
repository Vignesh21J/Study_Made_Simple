from django.shortcuts import render, redirect

from .forms import RegisterUserForm
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import authenticate, login, logout


# Create your views here.

def RegisterUser(request):

    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            messages.success(request, "Registered Successfully..!")
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form':form
    }

    return render(request, 'base/register.html', context)

def LoginUser(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "User with this Email does not exist..!")
            return render(request, 'base/login.html')
        
        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In..!")
            return redirect('home')
        else:
            messages.error(request, "Email or Password does not exist..!")
        

    return render(request, 'base/login.html')


def LogoutUser(request):
    logout(request)
    return redirect('home')
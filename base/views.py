from django.shortcuts import render

from .forms import RegisterUserForm
from django.contrib import messages


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
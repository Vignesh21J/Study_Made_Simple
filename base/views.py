from django.shortcuts import render, redirect

from .forms import RegisterUserForm
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import authenticate, login, logout

from .models import PasswordReset
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from .decorators import unauthenticated_user


# Create your views here.

@unauthenticated_user
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

@unauthenticated_user
def LoginUser(request):

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
            messages.error(request, "Email or Password is Invalid. Try Again with correct credentials..!")
        

    return render(request, 'base/login.html')


def LogoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def Forgot_Password_View(request):

    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            reset_password_url = reverse('reset-password', kwargs={'reset_id':new_password_reset.reset_id})
            full_reset_password_url = request.build_absolute_uri(reset_password_url)

            email_body = f'Reset your password using the link below:\n\n\n{full_reset_password_url}'

            email_message = EmailMessage(
                'Reset Your Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]    # List of recipients (receiver email)
            )

            email_message.fail_silently=True
            email_message.send()

            return redirect('reset-password-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"Email sending failed due to incorrect credentials. So Try again with correct credentials!")
            return redirect('forgot-password')

    return render(request, 'base/forgot_password.html')


def Reset_Password_Sent_View(request, reset_id):
    
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'base/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    


@unauthenticated_user
def Reset_Password_View(request, reset_id):

    try:
        reset_entry = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_have_error = False

            if password != confirm_password:
                password_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 6:
                password_have_error = True
                messages.error(request, 'Password must be at least 6 characters long')

            expiration_time = reset_entry.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                reset_entry.delete()
                messages.error(request, 'Reset link has expired')
                return redirect('forgot-password')
            
            if not password_have_error:
                user = reset_entry.user
                user.set_password(password)
                user.save()
                reset_entry.delete()
                messages.success(request, 'Password reset. Proceed to login.')
                return redirect('login-user')
            
            return render(request, 'reset_password.html', {'reset_id': reset_entry.reset_id})

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'base/reset_password.html', {'reset_id':reset_id})
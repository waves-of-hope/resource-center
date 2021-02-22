from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, UserProfileForm


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # adding a flash message
            messages.success(request,
                'Your account has been created. You are now able to log in.'
            )
            return redirect('login')

    else:
        form = CustomUserCreationForm()

    context = {'form': form }
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        # pass the current user's info to the form
        form = UserProfileForm(request.POST, request.FILES,
            instance=request.user
        )
        
        if form.is_valid():
            form.save()
            messages.success(request, 
                'Your profile has been updated'
            )
            # avoid the redirect alert from browser
            #  when one reloads the page
            return redirect('profile')

    else:
        form = UserProfileForm(instance=request.user)

    context = {'form': form }
    return render(request, 'accounts/profile.html', context)

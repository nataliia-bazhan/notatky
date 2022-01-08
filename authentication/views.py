from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("auth:log_in")
    return render(request, "sign_up.html", {'form': form})


def log_in(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("notes:notes")
        else:
            messages.info(request,
                          "Try again! username or password is incorrect")
            context['error'] = "username or password is incorrect"
    return render(request, "log_in.html", context)


def log_out(request):
    logout(request)
    return redirect("notes:notes")


@login_required
def profile(request, pk):
    user = User.objects.get(id=pk)
    context = {"user": user}
    return render(request, "profile.html", context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #update_session_auth_hash(request, user)
            logout(request)
            messages.success(request, 'Your password was successfully updated!')
            return redirect("auth:log_in")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })



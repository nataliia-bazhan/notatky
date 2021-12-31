from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("auth:log_in")
    return render(request, "sign_up.html", {'form': form})


def log_in(request):
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
    return render(request, "log_in.html", {})


def log_out(request):
    logout(request)
    return redirect("notes:notes")


def profile(request, pk):
    user = User.objects.get(id=pk)
    context = {"user": user}
    return render(request, "profile.html", context)

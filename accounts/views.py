from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, UserProfileEditModelForm
from .models import User

from rooms.models import Topic


def login_view(request):

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user is not None:
            login(request, user=user)
            return redirect("rooms:homepage")
        else:
            messages.error(request, "Username or password does not exists!")

    return render(request, "accounts/login_register.html")


def logout_view(request):
    logout(request)
    return redirect("rooms:homepage")


def register_view(request):

    authentication_page = "register"

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
        "authentication_page": authentication_page,
    }

    return render(request, "accounts/login_register.html", context)


def profile_view(request, pk):

    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }

    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit_view(request):

    if request.method == "POST":
        form = UserProfileEditModelForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", request.user.id)
    else:
        form = UserProfileEditModelForm(instance=request.user)

    context = {
        "form": form,
    }

    return render(request, "accounts/profile_edit.html", context)

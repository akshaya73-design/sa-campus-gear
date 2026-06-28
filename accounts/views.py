from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login Successful."
            )

            if user.is_staff:
                return redirect("inventory_dashboard")

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged Out Successfully."
    )

    return redirect("home")
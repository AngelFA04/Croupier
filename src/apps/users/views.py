from django.shortcuts import render


def logout(request):
    return render(request, "users/logout.html")


def login(request):
    return render(request, "users/login.html")

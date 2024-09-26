from django.shortcuts import render, HttpResponse


def show_user_name(request):
    return HttpResponse("Luís")

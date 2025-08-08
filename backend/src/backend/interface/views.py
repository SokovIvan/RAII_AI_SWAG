from django.shortcuts import render


def home(request):

    return render (request, "index.html")


def upload(request):

    return render (request, "upload_sound.html")
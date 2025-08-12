from django.shortcuts import render
from .ModelsAI.ModelsUsage import ModelsUsage

def home(request):

    return render (request, "index.html")


def upload(request):

    return render (request, "upload_sound.html")

#def tickets(request):

 #   return render (request, "tickets.html")

#def ticket(request):

    #return render (request, "ticket.html")

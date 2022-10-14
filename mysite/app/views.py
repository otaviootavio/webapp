from django.shortcuts import render

# Create your views here.


def olamundo(request):
    return render(request,"ola_mundo.html")

def home(request):
    return render(request,"home.html")


from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.


def show(request):
    time=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")    
    return HttpResponse("Login at "+time)


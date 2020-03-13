from django.shortcuts import render

# Create your views here.

def showTemplates(request):
    return render(request, 'test1.html')
   
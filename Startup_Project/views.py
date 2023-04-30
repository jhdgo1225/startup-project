from django.shortcuts import render


def index(request):
    return render(request, 'startup-project/main.html')

# Create your views here.

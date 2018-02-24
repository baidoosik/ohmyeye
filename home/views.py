from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def eye_check(request):
    return render(request, 'home/eye_check.html')
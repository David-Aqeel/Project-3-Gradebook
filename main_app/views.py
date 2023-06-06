from django.shortcuts import render
from .models import Cohorts


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cohorts_index(request):
    cohorts = Cohorts.objects.all()
    return render(request, 'cohorts/index.html', {'cohorts': cohorts})
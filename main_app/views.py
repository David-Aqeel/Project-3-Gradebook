from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Cohorts, Student


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cohorts_index(request):
    cohorts = Cohorts.objects.all()
    return render(request, 'cohorts/index.html', {'cohorts': cohorts})




class StudentList(ListView):
  model = Student

class StudentDetail(DetailView):
  model = Student

class StudentCreate(CreateView):
  model = Student
  fields = '__all__'

class StudentUpdate(UpdateView):
  model = Student
  fields = ['name', 'color']

class StudentDelete(DeleteView):
  model = Student
  success_url = '/toys' 
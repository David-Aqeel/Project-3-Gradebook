from django.shortcuts import render
from .models import Cohorts
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cohorts_index(request):
    cohorts = Cohorts.objects.all()
    return render(request, 'cohorts/index.html', {'cohorts': cohorts})

def cohorts_detail(request, cohort_id):
    cohort = Cohorts.objects.get(id=cohort_id)
    return render(request, 'cohorts/detail.html', {
        'cohort': cohort,
    })
    
class CohortCreate(CreateView):
    model = Cohorts
    fields = ['subject_name', 'note']
    

class CohortUpdate(UpdateView):
  model = Cohorts
  fields = ['subject_name', 'note',]

class CohortDelete(DeleteView):
  model = Cohorts
  success_url = '/cohorts'
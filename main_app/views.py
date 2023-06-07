from django.shortcuts import render, redirect 
from .models import Cohorts, Student, Student_Grades
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import Assignment_Form




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
    id_list = cohort.students.all().values_list('id')
    students_cohort_doesnt_have = Student.objects.exclude(id__in=id_list)
    assigment_form = Assignment_Form()
    return render(request, 'cohorts/detail.html', {
       'cohort': cohort, 'assigment_form': assigment_form, 
       'students': students_cohort_doesnt_have,
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


def add_assignment(request, cohort_id):
  form = Assignment_Form(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_assignment = form.save(commit=False)
    new_assignment.cohort_id = cohort_id
    new_assignment.save()
  return redirect('detail', cohort_id=cohort_id)


def students_index(request):
    students = Student.objects.all()
    return render(request, 'main_app/student_list.html', {'students': students})

# class StudentList(ListView):
#   model = Student

  

class StudentDetail(DetailView):
  model = Student

class StudentCreate(CreateView):
  model = Student
  fields = '__all__'

class StudentUpdate(UpdateView):
  model = Student
  fields = ['name', 'grade_level']

class StudentDelete(DeleteView):
  model = Student
  success_url = '/students' 

def assoc_student(request, cohort_id, student_id):
  Cohorts.objects.get(id=cohort_id).students.add(student_id)
  return redirect('detail', cohort_id=cohort_id)

def unassoc_student(request, cohort_id, student_id):
  Cohorts.objects.get(id=cohort_id).students.remove(student_id)
  return redirect('detail', cohort_id=cohort_id)

def add_student_grades(request, cohort_id):
    form = Student_Grades_Form(request.POST)
    new_student_grades = form.save(commit=False)
    new_student_grades.cohort_id = cohort_id
    new_student_grades.save()
    return redirect('detail', cohort_id=cohort_id)

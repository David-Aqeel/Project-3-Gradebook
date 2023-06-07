import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cohorts, Student, Student_Grades, Photo


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


@login_required
def cohorts_index(request):
    cohorts = Cohorts.objects.all()
    return render(request, "cohorts/index.html", {"cohorts": cohorts})


@login_required
def cohorts_detail(request, cohort_id):
    cohort = Cohorts.objects.get(id=cohort_id)
    id_list = cohort.students.all().values_list("id")
    students_cohort_doesnt_have = Student.objects.exclude(id__in=id_list)
    return render(
        request,
        "cohorts/detail.html",
        {
            "cohort": cohort,
        },
    )


class CohortCreate(LoginRequiredMixin, CreateView):
    model = Cohorts
    fields = ["subject_name", "note"]

    def form_valid(self, form):
        # self.request.user is the logged in user
        form.instance.user = self.request.user
        # Let the CreateView's form_valid method
        # do its regular work (saving the object & redirecting)
        return super().form_valid(form)


class CohortUpdate(LoginRequiredMixin, UpdateView):
    model = Cohorts
    fields = [
        "subject_name",
        "note",
    ]


class CohortDelete(LoginRequiredMixin, DeleteView):
    model = Cohorts
    success_url = "/cohorts"


def students_index(request):
    students = Student.objects.all()
    return render(request, "main_app/student_list.html", {"students": students})


# class StudentList(ListView):
#   model = Student


class StudentDetail(LoginRequiredMixin, DetailView):
    model = Student


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    fields = "__all__"


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ["name", "grade_level"]


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = "/students"


@login_required
def add_student_grades(request, cohort_id):
    form = Student_Grades_Form(request.POST)
    new_student_grades = form.save(commit=False)
    new_student_grades.cohort_id = cohort_id
    new_student_grades.save()
    return redirect("detail", cohort_id=cohort_id)
  
@login_required
def add_photo(request, student_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, student_id=student_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('students_detail', pk=student_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the db
            user = form.save()
            # Automatically log in the new user
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup template
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)

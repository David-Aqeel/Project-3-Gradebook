import os
import uuid
import boto3
from django.shortcuts import render, redirect
from .models import Cohorts, Student, Student_Grades, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import Student_Grades_Form  #Assignment_Form
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



def calculate_total_grade(student_grades):
    total_grade = 0
    for grade in student_grades:
        if grade.grade:
            total_grade += int(grade.grade)
    return total_grade

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
    # assigment_form = Assignment_Form()
    return render(
        request,
        "cohorts/detail.html",
        {
            "cohort": cohort,
            # "assigment_form": assigment_form,
            "students": students_cohort_doesnt_have,
        },
    )


# class CohortCreate(CreateView):
#     id_list = cohort.students.all().values_list("id")
#     students_cohort_doesnt_have = Student.objects.exclude(id__in=id_list)
#     return render(
#         request,
#         "cohorts/detail.html",
#         {
#             "cohort": cohort,
#         },
#     )


class CohortCreate(LoginRequiredMixin, CreateView):
    model = Cohorts
    fields = ["subject_name", "note"]

    def form_valid(self, form):
        # self.request.user is the logged in user
        form.instance.teacher_id = self.request.user.id
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


# def add_assignment(request, cohort_id):
#     form = Assignment_Form(request.POST)
#     # validate the form
#     if form.is_valid():
#         # don't save the form to the db until it
#         # has the cat_id assigned
#         new_assignment = form.save(commit=False)
#         new_assignment.cohort_id = cohort_id
#         new_assignment.save()
#     return redirect("detail", cohort_id=cohort_id)


def students_index(request):
    students = Student.objects.all()
    return render(request, "main_app/student_list.html", {"students": students})


# class StudentList(ListView):
#   model = Student


class StudentDetail(LoginRequiredMixin, DetailView):
    model = Student
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         student = self.get_object()
         student_grades = Student_Grades.objects.filter(students=student)
         total_grade = calculate_total_grade(student_grades)
         context["student_grades"] = student_grades
         context["total_grade"] = total_grade
         context["student_grades_form"] = Student_Grades_Form()
         return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     student = self.get_object()
    #     context["student_grades_form"] = Student_Grades_Form()
    #     return context


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    fields = "__all__"


def assoc_student(request, cohort_id, student_id):
    Cohorts.objects.get(id=cohort_id).students.add(student_id)
    # Student_Grades.objects.get(cohort_id=cohort_id).remove()
    return redirect("detail", cohort_id=cohort_id)


def unassoc_student(request, cohort_id, student_id):
    Cohorts.objects.get(id=cohort_id).students.remove(student_id)
    # Student_Grades.objects.get(cohort_id=cohort_id).remove()
    # Student_Grades.objects.get(grade)
    return redirect("detail", cohort_id=cohort_id)


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ["name", "grade_level"]


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = "/students"


@login_required
def add_student_grades(request, student_id):
    form = Student_Grades_Form(request.POST)
    new_student_grades = form.save(commit=False)
    new_student_grades.student_id = student_id
    new_student_grades.cohort_id = cohort_id
    new_student_grades.save()
    return redirect("students_detail", student_id=student_id)

def detail(request, cohort_id):
    cohort = Cohorts.objects.get(id=cohort_id)
    students = cohort.students.all()
    student_grades = StudentGrades.objects.filter(student__in=students)

    context = {
        'cohort': cohort,
        'students': students,
        'student_grades': student_grades,
    }

    return render(request, 'cohorts/detail.html', context)

def add_grade(request, cohort_id, student_id):
    if request.method == 'POST':
        grade = request.POST['grade']
        student = Student.objects.get(id=student_id)
        cohort = Cohorts.objects.get(id=cohort_id)
        student_grade = Student_Grades(grade=grade, cohorts=cohort, students=student)
        student_grade.save()
    return redirect('detail', cohort_id=cohort_id)

def delete_grade(request, cohort_id, grade_id):
    if request.method == 'POST':
        grade = Student_Grades.objects.get(id=grade_id)
        grade.delete()
    return redirect('detail', cohort_id=cohort_id)

@login_required
def add_photo(request, student_id):
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")

        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind(".") :]
        try:
            bucket = os.environ["S3_BUCKET"]
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, student_id=student_id)
        except Exception as e:
            print("An error occurred uploading file to S3")
            print(e)
    return redirect("students_detail", pk=student_id)


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



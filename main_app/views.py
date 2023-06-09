import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cohorts, Student, Student_Grades, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import Student_Grades_Form  # Assignment_Form
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def calculate_gpa(student_grades):
    print("This is calculate_gpa")
    print(student_grades)
    grade_points = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "F": 0.0,
    }

    total_grades = len(student_grades)
    if total_grades == 0:
        return 0.0  # Return 0.0 if no grades are available

    grade_sum = 0.0
    total_subjects = len(set([grade.cohorts for grade in student_grades]))
    print("This is  total_subjects")
    print(total_subjects)

    for student_grade in student_grades:
        grade = student_grade.grade
        grade_sum += grade_points.get(grade, 0.0)

    gpa = grade_sum / total_subjects
    return round(gpa, 2)


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
    cohort = get_object_or_404(Cohorts, id=cohort_id)
    cohort = Cohorts.objects.get(id=cohort_id)
    print("These are cohort.students.all()")
    print(cohort.students.all())
    id_list = cohort.students.all().values_list("id")
    students_cohort_doesnt_have = Student.objects.exclude(id__in=id_list)
    student_grades = Student_Grades.objects.filter(cohorts=cohort_id)
    #  {% for student_grade in student.student_grades.all %}
    print("These are the student grades in the detail view")
    print(student_grades)
    #   {% if student_grade.cohorts_id == cohort.id %}
    # print("These are student_grade.cohorts_id")
    # print(student_grades[0])
    # # <p>Grade: {{ student_grade.grade }}</p>
    # print("These are student_grade.grade")
    # print(student_grades[0].grade)

    return render(
        request,
        "cohorts/detail.html",
        {
            "cohort": cohort,
            "students_cohort_doesnt_have": students_cohort_doesnt_have,
            "student_grades": student_grades,
        },
    )


# THIS IS NOT BEING USED AT ALL
# def detail(request, cohort_id):
#     cohort = Cohorts.objects.get(id=cohort_id)
#     students = cohort.students.all()
#     student_grades = Student_Grades.objects.filter(student__in=students)
#     gpa = calculate_gpa(student_grades)


#     context = {
#         'cohort': cohort,
#         'students': students,
#         'student_grades': student_grades,
#         'gpa': gpa
#     }

#     return render(request, 'cohorts/detail.html', context)

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
        form.instance.teacher = self.request.user
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
        gpa = calculate_gpa(student_grades)
        context["student_grades"] = student_grades
        context["gpa"] = gpa
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
# def add_student_grades(request, student_id, cohort_id):
#     form = Student_Grades_Form(request.POST)
#     new_student_grades = form.save(commit=False)
#     new_student_grades.student_id = student_id
#     new_student_grades.cohort_id = cohort_id
#     new_student_grades.save()
#     return redirect("students_detail", pk=student_id)


@login_required
def add_grade(request, cohort_id, student_id):
    if request.method == "POST":
        print("This is request.POST:", request.POST)
        grade = request.POST.get("grade")
        print("This is add_grade")
        print(grade)
        if grade is not None:
            created = Student_Grades.objects.update_or_create(
                students_id=student_id, cohorts_id=cohort_id, defaults={"grade": grade}
            )
    return redirect("detail", cohort_id=cohort_id)


# THIS CODE ORIGINALLY WENT INSIDE ADD_GRADE
# student = Student.objects.get(id=student_id)
# cohort = Cohorts.objects.get(id=cohort_id)
# student_grade = Student_Grades(grade=grade, cohorts=cohort, students=student)
# student_grade.save()

# def delete_grade(request, cohort_id, grade_id):
#     if request.method == "POST":
#         grade = Student_Grades.objects.get(id=grade_id)
#         grade.delete()
#     return redirect("detail", cohort_id=cohort_id)


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

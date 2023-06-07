from django.forms import ModelForm
from .models import Student_Grades, Assignment

class Student_Grades_Form(ModelForm):
  class Meta:
    model = Student_Grades
    fields = ['grade']




class Assignment_Form(ModelForm):
  class Meta:
    model = Assignment
    fields = ['date', 'assignment']
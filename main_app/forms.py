from django.forms import ModelForm
from .models import Student_Grades

class Student_Grades_Form(ModelForm):
  class Meta:
    model = Student_Grades
    fields = ['grade']

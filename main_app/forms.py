from django import forms
from django.forms import ModelForm
from .models import Student_Grades # Assignment

class Student_Grades_Form(ModelForm):
   grade = forms.ChoiceField(choices=Student_Grades.GRADE_CHOICES)
   class Meta:
    model = Student_Grades
    fields = '__all__'




# class Assignment_Form(ModelForm):
#   class Meta:
#     model = Assignment
#     fields = ['date', 'assignment']
from django import forms
from django.forms import ModelForm
from .models import Student_Grades 

class Student_Grades_Form(ModelForm):
   grade = forms.ChoiceField(choices=Student_Grades.GRADE_CHOICES)
   class Meta:
    model = Student_Grades
    fields = '__all__'





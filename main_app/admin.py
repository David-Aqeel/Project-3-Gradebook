from django.contrib import admin
from .models import Cohorts, Student, Student_Grades, Photo   #Assignment,


# Register your models here.
admin.site.register(Cohorts)
# admin.site.register(Assignment)
admin.site.register(Student) 
admin.site.register(Student_Grades) 
admin.site.register(Photo) 

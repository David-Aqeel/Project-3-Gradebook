from django.contrib import admin
from .models import Cohorts, Student, Assignment, Student_Grades, Photo


# Register your models here.
admin.site.register(Cohorts)
admin.site.register(Assignment)
admin.site.register(Student) 
admin.site.register(Student_Grades) 
admin.site.register(Photo) 

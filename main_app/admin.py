from django.contrib import admin
from .models import Cohorts

from .models import Cohorts, Student


# Register your models here.


admin.site.register(Student) 
admin.site.register(Cohorts)

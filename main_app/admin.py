from django.contrib import admin
from .models import Cohorts

from .models import Cohorts, Student, Assignment


# Register your models here.


admin.site.register(Student) 
admin.site.register(Cohorts)
admin.site.register(Assignment)


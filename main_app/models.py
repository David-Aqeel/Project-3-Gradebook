from django.db import models

# Create your models here.
#Additional Comment part 2
from django.db import models
from django.urls import reverse

# Create your models here.
# Reminder to put the Teacher foreign key
class Cohort(models.Model):
    name = models.CharField(max_length=50)
    note = models.TextField(max_length=150)
    
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cohort_id': self.id})

class Student(models.Model):
    name = models.CharField(max_length = 100)
    grade_level = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'student_id': self.id})
    
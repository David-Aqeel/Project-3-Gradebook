from django.db import models
from django.urls import reverse

# Create your models here.
class Cohorts(models.Model):
    subject_name = models.CharField(max_length=50)
    note = models.TextField(max_length=150)
    
    def __str__(self):
        return f'{self.subject_name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cohort_id': self.id})
    
class Student_Grades(models.Model):
    grade = models.IntegerField()
    cohorts = models.ForeignKey(
    Cohorts,
    on_delete=models.CASCADE
  )
    
    def __str__(self):
        return f"{self.get_grade_display()}"
    
    class Meta:
        ordering = ['-grade']
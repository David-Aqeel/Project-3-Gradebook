from django.db import models
from django.urls import reverse

# Create your models here.

class Student(models.Model):
  name = models.CharField(max_length=75)
  grade_level = models.IntegerField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('students_detail', kwargs={'pk': self.id})


class Cohorts(models.Model):
    subject_name = models.CharField(max_length=50)
    note = models.TextField(max_length=150)

    students = models.ManyToManyField(Student)
    
    def __str__(self):
        return f'{self.subject_name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cohort_id': self.id})
    
class Assignment(models.Model):
  date = models.DateField('Due Date')
  assignment = models.CharField(max_length=100)
  grade = models.IntegerField()
  cohort = models.ForeignKey(Cohorts, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.assignment()} on {self.date}"
  
  class Meta:
    ordering = ['-date']
    
class Student_Grades(models.Model):
    grade = models.IntegerField()
    cohorts = models.ForeignKey(
    Cohorts,
    on_delete=models.CASCADE
  )
    students = models.ForeignKey(
    Student,
    on_delete=models.CASCADE
  )

    def __str__(self):
        return f"{self.get_grade_display()}"
    
    class Meta:
        ordering = ['-grade']

from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.subject_name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cohort_id': self.id})


# class Assignment(models.Model):
#   date = models.DateField('Due Date')
#   assignment = models.CharField(max_length=100)
#   grade = models.IntegerField()
#   cohort = models.ForeignKey(Cohorts, on_delete=models.CASCADE)

#   def __str__(self):
#     return f"{self.assignment} on {self.date}"
  
#   class Meta:
#     ordering = ['-date']
    
class Student_Grades(models.Model):
    # grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(101)])
    grade = models.CharField()
    cohorts = models.ForeignKey(Cohorts, on_delete=models.CASCADE)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
      return f"Grade: {self.grade} - Cohort: {self.cohorts} - Student: {self.students}"
   
        
class Photo(models.Model):
  url = models.CharField(max_length=200)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for student_id: {self.student_id} @{self.url}"

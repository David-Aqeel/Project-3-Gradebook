from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cohorts/', views.cohorts_index, name='index'),

    path('students/', views.StudentList.as_view(), name='students_index'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='students_detail'),
    path('students/create/', views.StudentCreate.as_view(), name='students_create'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='students_update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='students_delete'),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cohorts/', views.cohorts_index, name='index'),
    path('cohorts/<int:cohort_id>/', views.cohorts_detail, name='detail'),
    path('cohorts/create/', views.CohortCreate.as_view(), name='cohorts_create'),
    path('cohorts/<int:pk>/update/', views.CohortUpdate.as_view(), name='cohorts_update'),
    path('cohorts/<int:pk>/delete/', views.CohortDelete.as_view(), name='cohorts_delete'),

    path('cohorts/<int:cohort_id>/add_assignment/', views.add_assignment, name='add_assignment'),
    path('cohorts/<int:cohort_id>/assoc_student/<int:student_id>/', views.assoc_student, name='assoc_student'),
    path('cohorts/<int:cohort_id>/unassoc_student/<int:student_id>/', views.unassoc_student, name='unassoc_student'),


    path('cohorts/<int:cohort_id>/add_student_grades/', views.add_student_grades, name='add_student_grades'),
    path('students/', views.students_index, name='students_index'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='students_detail'),
    path('students/create/', views.StudentCreate.as_view(), name='students_create'),
    path('students/<int:pk>/update/', views.StudentUpdate.as_view(), name='students_update'),
    path('students/<int:pk>/delete/', views.StudentDelete.as_view(), name='students_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('students/<int:student_id>/add_photo/', views.add_photo, name='add_photo'),
]

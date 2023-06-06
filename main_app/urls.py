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
]
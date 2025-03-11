from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_questionnaire, name='start'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('success/', views.success, name='success'),
    path('no-questions/', views.no_questions, name='no_questions'),
    path('view-responses/<str:admin_password>/', views.view_all_responses, name='view_responses'),
]
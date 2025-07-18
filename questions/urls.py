from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('start/', views.start_questionnaire, name='start'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('previous/', views.previous_question, name='previous_question'),
    path('success/', views.success, name='success'),
    path('results/', views.results, name='results'),
    path('no-questions/', views.no_questions, name='no_questions'),
    
    path('reset/', views.reset_session, name='reset_session'),
    path('go-to-question/<int:question_id>/', views.go_to_question, name='go_to_question'),
]
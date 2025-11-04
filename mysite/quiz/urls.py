from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_view, name='root'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/submit/', views.quiz_submit, name='quiz_submit'),
    path('quiz/add/', views.quiz_add, name='quiz_add'),
    path('quiz/<int:pk>/edit/', views.quiz_edit, name='quiz_edit'),
    path('quiz/<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('quiz/<int:quiz_pk>/question/add/', views.question_add, name='question_add'),
    path('quiz/<int:quiz_pk>/question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('quiz/<int:quiz_pk>/question/<int:pk>/delete/', views.question_delete, name='question_delete'),
]

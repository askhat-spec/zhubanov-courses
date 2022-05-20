from django.urls import path
from . import views


urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('login/', views.Login.as_view(), name='login'),
    # path('register/', views.UserRegisterView.as_view(), name='register'),
    path('create-course/', views.create_course, name='create-course'),
    path('<slug:course_slug>/', views.edit_course, name='edit-course'),
    path('create-lecture/<slug:course_slug>/', views.create_lecture, name='create-lecture'),
    path('edit-lecture/<slug:course_slug>/<slug:lecture_slug>/', views.edit_lecture, name='edit-lecture'),
]
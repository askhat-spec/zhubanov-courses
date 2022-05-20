from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('courses/<slug:department_slug>/', views.courses_list, name='courses_list_by_department'),
    path('courses/', views.courses_list, name='courses_list'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lecture_slug>/', views.lecture_detail, name='lecture_detail')
]
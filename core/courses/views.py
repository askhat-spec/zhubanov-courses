from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Course, Department, Lecture


class MainPage(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(is_active=True).order_by('-modified')[:4]


def courses_list(request, department_slug=None):
    department = None
    departments = Department.objects.all()
    courses = Course.objects.filter(is_active=True)
    if department_slug:
        department = get_object_or_404(Department, slug = department_slug)
        courses = courses.filter(department=department)
    return render(request, 'courses.html', {'department': department, 
                                            'departments': departments,
                                            'courses': courses})


def course_detail(request, course_slug=None):
    course = get_object_or_404(Course, slug = course_slug)
    lectures = Lecture.objects.filter(course = course)
    return render(request, 'course_detail.html', {'course': course, 'lectures': lectures})


def lecture_detail(request, course_slug, lecture_slug):
    lecture = get_object_or_404(Lecture, slug = lecture_slug)
    lectures = Lecture.objects.filter(course__slug=course_slug)
    return render(request, 'lecture_detail.html', {'lecture' :lecture, 'lectures': lectures})
from django.contrib.auth.views import LoginView
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

import boto3
import environ

from .utils import get_encoded_data
from .forms import AuthUserForm, RegisterUserForm, CourseCreateForm, LectureCreateForm
from courses.models import Course, Lecture


env = environ.Env()
environ.Env().read_env()

S3_BUCKET_NAME = env('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')


@login_required
def cabinet(request):
    courses = Course.objects.filter(author=request.user)
    return render(request, 'cabinet.html', context={'courses': courses})    


@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect("cabinet")
    else:
        form = CourseCreateForm()
    return render(request, "create_course.html", {"form": form})


@login_required
def edit_course(request, course_slug):
    course = get_object_or_404(Course, slug = course_slug)
    lectures = Lecture.objects.filter(course = course)
    if request.method == "POST":
        form = CourseCreateForm(request.POST,  request.FILES, instance = course)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect("cabinet")
    else:
        form = CourseCreateForm(instance = course)
    return render(request, "edit_course.html", {"form": form, "lectures": lectures, "course": course})


@login_required
def create_lecture(request, course_slug):
    course = get_object_or_404(Course, slug = course_slug)
    if request.method == "POST":
        form = LectureCreateForm(request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course

            # botocore.handlers.BUILTIN_HANDLERS = [elem for elem in botocore.handlers.BUILTIN_HANDLERS if not (elem[0].startswith('before-parameter-build.s3.') and elem[1] == botocore.handlers.validate_ascii_metadata)]
            # Видеоны AWS S3-ге салу және URL адресін сақтау
            if form.cleaned_data['video']:
                s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
                video = form.cleaned_data['video']
                bucket = s3.Bucket(S3_BUCKET_NAME)

                encoded_metadata = get_encoded_data(str(course.department), course.title, lecture.title,)

                bucket.upload_fileobj(video.file, video.name, ExtraArgs={"ACL": "public-read", "Metadata": encoded_metadata})

                # Видеоның сілтемесін сақтау
                lecture.video_url = f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{video.name}'
            lecture.save()
            return redirect('edit-course', course_slug=course_slug)
    else:
        form = LectureCreateForm()
    return render(request, 'create_lecture.html', {"form": form, "course": course})


@login_required
def edit_lecture(request, course_slug, lecture_slug):
    course = get_object_or_404(Course, slug = course_slug)
    current_lecture = get_object_or_404(Lecture, slug = lecture_slug)
    if request.method == "POST":
        form = LectureCreateForm(request.POST, request.FILES, instance = current_lecture)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course
            # botocore.handlers.BUILTIN_HANDLERS = [elem for elem in botocore.handlers.BUILTIN_HANDLERS if not (elem[0].startswith('before-parameter-build.s3.') and elem[1] == botocore.handlers.validate_ascii_metadata)]
            if form.cleaned_data['video']:
                s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
                video = form.cleaned_data['video']
                bucket = s3.Bucket(S3_BUCKET_NAME)

                encoded_metadata = get_encoded_data(str(course.department), course.title, lecture.title,)

                bucket.upload_fileobj(video.file, video.name, ExtraArgs={"ACL": "public-read", "Metadata": encoded_metadata})

                # Видеоның сілтемесін сақтау
                lecture.video_url = f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{video.name}'
            else:
                lecture.video_url = current_lecture.video_url
            lecture.save()
            return redirect('edit-course', course_slug=course_slug)
    else:
        form = LectureCreateForm(instance = current_lecture)
    return render(request, 'create_lecture.html', {"form": form})


class Login(LoginView):
    form_class = AuthUserForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('cabinet')


class UserRegisterView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main_page')


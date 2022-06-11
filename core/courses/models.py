from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import slugify


class Degree(models.Model):
    name = models.CharField(max_length=30, verbose_name='Академиялық дәреже')

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='Өзі туралы')

    def get_full_name(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)


class Department(models.Model):
    name = models.CharField(max_length=150, verbose_name='Кафедра')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('courses_list_by_department', args=[self.slug])


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Курс')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    code = models.IntegerField(unique=True, blank=True, null=True, verbose_name='Курс коды')
    image = models.ImageField(upload_to='course_images', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    degree = models.ForeignKey(Degree,blank=True, null=True, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    description = models.TextField(verbose_name='Сипаттамасы')
    syllabus = models.TextField(blank=True, null=True, verbose_name='Силлабус')
    readings = models.TextField(blank=True, null=True, verbose_name='Оқу құралдары')
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, editable=True)
    modified = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('course_detail', args=[self.slug])


class Lecture(models.Model):
    title = models.CharField(max_length=255, verbose_name='Лекция')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Лекция сипаттамасы')
    transcript = models.TextField(blank=True, null=True, verbose_name='Лекция жазбасы')
    video_url = models.URLField(max_length=255, unique=True, verbose_name='URL видеолекции')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lecture, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('lecture_detail', args=[self.course.slug ,self.slug])
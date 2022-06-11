from django.test import TestCase, Client
from django.urls import reverse
from courses.models import *


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_department = Department.objects.create(name='test department')
        self.test_degree = Degree.objects.create(name='Bachelor')
        self.test_user = User.objects.create_user(
            username='john',
            password='secret'
        )
        self.test_course = Course.objects.create(
            title='Test Course',
            code='123',
            author=self.test_user,
            degree=self.test_degree,
            department=self.test_department,
            description='Some Test Description'
        )
        self.test_lecture = Lecture.objects.create(
            title = 'Test Lecture',
            video_url = 'https://zhubanov-courses.s3.eu-north-1.amazonaws.com/test.mp4',
            course = self.test_course
        )

    def test_slugs(self):
        self.assertEquals(self.test_department.slug, 'test-department')
        self.assertEquals(self.test_course.slug, 'test-course')
        self.assertEquals(self.test_lecture.slug, 'test-lecture')

    def test_edit_course(self):
        course = Course.objects.first()
        course.title = 'Edited Course Title'
        course.save()
        self.assertEquals(course.title, 'Edited Course Title')
        self.assertEquals(course.slug, 'edited-course-title')
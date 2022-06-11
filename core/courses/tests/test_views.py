from django.test import TestCase, Client
from django.urls import reverse
from courses.models import *


class TestViews(TestCase):
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

    def test_user(self):
        self.assertFalse(self.test_user.password == 'secret')
        self.assertTrue(self.test_user.check_password("secret"))
        self.assertEquals(self.test_user.course_set.count(), 1)

    def test_main_page(self):
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_course_list(self):
        url = reverse('courses_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')

    def test_course_list_by_department(self):
        url = reverse('courses_list_by_department', args=['test-department'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')

    def test_course_detail(self):
        url = reverse('course_detail', args=['test-course'])
        response = response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_detail.html')

    def test_lectures_list(self):
        url = reverse('lecture_detail', args=['test-course', 'test-lecture'])
        response = response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lecture_detail.html')
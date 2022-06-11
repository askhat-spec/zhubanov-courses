from django.test import SimpleTestCase
from django.urls import resolve, reverse
from courses.views import *


class TestUrls(SimpleTestCase):
    
    def test_main_page_resolves(self):
        url = reverse('main_page')
        self.assertEquals(resolve(url).func.view_class, MainPage)

    def test_courses_list_by_department_resolves(self):
        url = reverse('courses_list_by_department', args=['department_slug'])
        self.assertEquals(resolve(url).func, courses_list)

    def test_courses_list_url_resolves(self):
        url = reverse('courses_list')
        self.assertEquals(resolve(url).func, courses_list)

    def test_courses_detail_url_resolves(self):
        url = reverse('course_detail', args=['course_slug'])
        self.assertEquals(resolve(url).func, course_detail)

    def test_lecture_detail_url_resolves(self):
        url = reverse('lecture_detail', args=['course_slug', 'lecture_slug'])
        self.assertEquals(resolve(url).func, lecture_detail)
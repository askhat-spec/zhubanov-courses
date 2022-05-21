from django.contrib import admin
from courses.models import Department, Course, Lecture, Degree, Profile


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Degree)
admin.site.register(Profile)
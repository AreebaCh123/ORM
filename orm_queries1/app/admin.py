from django.contrib import admin
from .models import Student, Course

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_students']

    def get_students(self, obj):
        # Join all student names into a single string
        return ", ".join([student.name for student in obj.students.all()])

    get_students.short_description = 'Students'

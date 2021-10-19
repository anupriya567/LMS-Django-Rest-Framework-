from django.contrib import admin
from .models import Category,Course,Tag

class CourseAdminModel(admin.ModelAdmin):
    model = Course
    list_editable = ['active']
    list_display = ['id', 'title', 'discount', 'active']


admin.site.register(Category)
admin.site.register(Course, CourseAdminModel)
admin.site.register(Tag)
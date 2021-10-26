from django.contrib import admin
from . models import Doubt,DoubtAnswers
# Register your models here.

class DoubtAdminModel(admin.ModelAdmin):
    model = Doubt
    list_display = ['id', 'course', 'chapter', 'user']

admin.site.register(Doubt,DoubtAdminModel)
admin.site.register(DoubtAnswers)

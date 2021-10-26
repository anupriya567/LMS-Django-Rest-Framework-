from django.contrib import admin
from .models import Review

class ReviewAdminModel(admin.ModelAdmin):
    model = Review
    list_editable = ['active']
    list_display = ['course','user','rating','active']


admin.site.register(Review,ReviewAdminModel)


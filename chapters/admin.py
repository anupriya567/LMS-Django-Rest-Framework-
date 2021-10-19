from django.contrib import admin
from chapters.models import Chapter,HeadingChapter,TextChapter,VideoChapter,LinkChapter
from chapters.forms import TextChapterForm, VideoChapterForm



class TextChapterAdminModel(admin.ModelAdmin):
    form = TextChapterForm


class VideoChapterAdminModel(admin.ModelAdmin):
    form = VideoChapterForm


admin.site.register(Chapter)
admin.site.register(HeadingChapter)
admin.site.register(LinkChapter)
admin.site.register(TextChapter, TextChapterAdminModel)
admin.site.register(VideoChapter, VideoChapterAdminModel)

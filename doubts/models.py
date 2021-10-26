from django.db import models
from courses.models import Course
from chapters.models import Chapter
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Doubt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='doubts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts') 
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='doubts')  
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


class DoubtAnswers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    question = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers') 
    created = models.DateTimeField(auto_now_add=True)
    answer =  models.CharField(max_length=500)
    

    


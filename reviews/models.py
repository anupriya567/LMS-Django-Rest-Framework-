from django.db import models
from courses.models import Course
from django.contrib.auth.models import User
import uuid
from django.core.validators  import MinValueValidator,MaxValueValidator
# Create your models here.

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')   
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=500)
    active = models.BooleanField(default= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} | {self.rating}'

         
   
     


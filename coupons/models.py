from django.db import models
import uuid
from courses.models import Course
import shortuuid
# Create your models here.


def random_code():
    return shortuuid.ShortUUID().random(length=6).upper()


class Coupon(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=6,null=False, default=random_code)   
    name = models.CharField(max_length=50,default = "coupon")  

    def __str__(self):
        return self.code       


















class CouponM(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='coupon')
    code = models.CharField(max_length=6,
                            null=False, default=random_code)                            

    def __str__(self):
        return self.code                            



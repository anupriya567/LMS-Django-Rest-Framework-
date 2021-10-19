from django.shortcuts import render
from coupons.serializers import CouponSerializer
from rest_framework.views import APIView
from . models import Coupon
from courses.models import Course
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from uuid import UUID

#  /api/coupon/

#  /api/coupon/course/course_id
class CouponRetrieveByCourse(APIView):
    queryset = Coupon.objects.all()

    def get(self, request, *args, **kwargs):
        
        course_id = self.kwargs.get('pk')
        try:
            UUID(course_id)
        except:
            return Response({"course": ["course id is not valid id"]}, status=status.HTTP_400_BAD_REQUEST)    
       
        self.queryset = self.queryset.filter(course__id = course_id, active=True)
        if len(self.queryset) == 0:
            content = {'Not Found':'No coupons found for this course'}
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CouponSerializer(self.queryset,many = True)
        return Response(serializer.data)


class CouponModelViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
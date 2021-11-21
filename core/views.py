from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
@api_view()
def api_root(request):
    response = {
        'API ROOT' : reverse('api_root',request = request),   
        'Courses':
        {
        'Course List': reverse('courses:course-list', request=request),
        'Course Detail': reverse('courses:course-detail',args=['<id>'] , request = request),
        'Course Detail Slug': reverse('courses:CourseDetailSlug',args=['<course-slug>'] , request=request),
        },  

        'Categories':
        {
        'Category List': reverse('courses:category-list', request=request),
        'Category Detail': reverse('courses:category-detail',args=['<id>'] , request=request),
        'Category Detail Slug': reverse('courses:CategoryDetailSlug',args=['<category-slug>'] , request=request),
        },  

        'Chapters': 
        {
          'Chapter Types': reverse('chapters:chapter-type', request=request),
          'Video Plateforms Available': reverse('chapters:video-plateform-listview', request=request),
          'Chapter List by Course': reverse('chapters:chapter-list', args=['<course_id>'],request=request),
          'Chapter Detail': reverse('chapters:chapter-detail',args=['<chapter_id>'], request=request),
          'Create Chapter': reverse('chapters:chapter-createview', request=request)

        },
        'Tags':
        {
        'Tag List': reverse('courses:tag-list', request=request),
        'Tag Detail': reverse('courses:tag-detail',args=['<id>'] , request=request),
        }, 
        'Coupons':
        {
          'Coupon List': reverse('coupons:coupon-list',request=request),
          'Coupon Detail': reverse('coupons:coupon-detail',args = ['<coupon_id>'],request=request),
          'CouponByCode': reverse('coupons:coupon-retrieve-by-course',args=['<course_id>'],request=request)
        },
        'Orders':
        {
          'OrderCreate':reverse("orders:create-order", request=request),
          'Make Payment on Razorpay': 'http://127.0.0.1:5500/djangoo/flyhigh/payment_test/index.html',
          'Validate Payment': reverse('orders:validate-payment',request=request)
        },
        'Subscriptions':
        {
          'Subscription List':reverse("subscriptions:subscription-list", request=request),
          # 'CourseSubscribedByUser':reverse("subscriptions:subscription-list-of-user",args=['<user_id>'], request=request),
          
        },
          'Doubts':
        {
          'Doubts List':reverse("doubts:doubts-list", request=request),
          'Doubts Detail':reverse("doubts:doubts-detail",args = ['<doubt_id>'], request=request),
          # 'Doubts Create':reverse("doubts:doubts-create", request=request),
          
          
        },

     'DoubtAnswers':
        {
          'DoubtAnswers List':reverse("doubts:answers-list", request=request),
          'Doubts Detail':reverse("doubts:answers-detail",args = ['<doubt_id>'], request=request),
          # 'Doubts Create':reverse("doubts:doubts-create", request=request),
          # 'CourseSubscribedByUser':reverse("subscriptions:subscription-list-of-user",args=['<user_id>'], request=request),
          
        },
      'Authentication': 
      {
       'Generate Token Pair':reverse("token_obtain_pair", request=request),
       'Generate Access Token from Refresh Token ':reverse("token_refresh", request=request),

      },
    }
    return Response(response)



# 'DoubtAnswers List':reverse("doubts:answers-list", request=request),
# ye answers basename se aaya h
# doubts ye app ka name h
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
        'Subscription':
        {
          'Subscription List':reverse("subscriptions:subscription-list", request=request),
          'CourseSubscribedByUser':reverse("subscriptions:subscription-list-of-user", request=request),
          
        }
    }
    return Response(response)


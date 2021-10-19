from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter




coupon_router = DefaultRouter()
coupon_router.register("", views.CouponModelViewSet, basename='coupon')
urlpatterns = [
  
# /api/coupons/
# CouponRetrieveByCourse
  
  path("course/<str:pk>/",views.CouponRetrieveByCourse.as_view(),name = 'coupon-retrieve-by-course'),

  path('', include(coupon_router.urls))

]

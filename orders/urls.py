from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# /api/orders/

OrderUrls = [
   
path('create-order/',views.CreateOrder.as_view(),name = 'create-order'),
path('validate-payment/',views.ValidatePayment.as_view(),name = "validate-payment")

]
SubscriptionUrls= [
   
path('',views.SubscriptionList.as_view(),name = 'subscription-list'),
path('user/<int:pk>', views.CourseSubscribedByUser.as_view(),name='subscription-list-of-user')

]
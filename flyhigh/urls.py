"""flyhigh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core.views import api_root
from orders.urls import OrderUrls,SubscriptionUrls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api_root'),

    path('api/', include(('courses.urls', 'courses'), namespace='courses')),

    path('api/chapters/', include(('chapters.urls', 'chapters'), namespace='chapters')),
    path('api/coupons/', include(('coupons.urls', 'coupons'), namespace='coupons')),
    path('api/doubts/', include(('doubts.urls', 'doubts'), namespace='doubts')),
    path('api/orders/', include((OrderUrls, 'orders'), namespace='orders')),
    path('api/subscriptions/',include((SubscriptionUrls, 'order'), namespace='subscriptions')),
   
]

from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.

course_router = DefaultRouter()
course_router.register('',views.CourseVS,basename="course")

category_router = DefaultRouter()
category_router.register('',views.CategoryVS,basename="category")

tag_router = DefaultRouter()
tag_router.register('',views.TagVS,basename="tag")
# tag-list
# tag-detail

# /api/

urlpatterns = [

     path('categories/', include(category_router.urls)),
     path('categories/slug/<str:slug>/', views.CategoryDetailSlug.as_view(),
         name='CategoryDetailSlug'),
     path('categories/<str:category_id>/courses', views.CoursesByCategory.as_view(),
         name='CoursesByCategory'),

    path('tags/', include(tag_router.urls)),

    path('courses/', include(course_router.urls)),
    path('courses/slug/<str:slug>/', views.CourseDetailSlug.as_view(),
         name='CourseDetailSlug'),
    
    
    # path('categories/', CategoryListView.as_view(), name='category-listview'),
    # path('categories/<str:pk>', CategoryDetailView.as_view(),
    #      name='category-detailview'),
]
# api/



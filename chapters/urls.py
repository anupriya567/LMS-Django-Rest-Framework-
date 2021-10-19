from . import views
from django.contrib import admin
from django.urls import path


# base url : api/chapters/
urlpatterns = [
    path('chapter-types/', views.ChapterTypes, name='chapter-type'),
    path('video-plateforms/', views.VideoPlateform,name='video-plateform-listview'),

    path('course/<str:course>', views.ChapterList.as_view(),name='chapter-list'),
    path('<str:pk>/', views.ChapterDetail.as_view(),name='chapter-detail'),
    path('', views.ChapterCreate.as_view(),name='chapter-createview'),

   
]
 
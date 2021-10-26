from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('answers',views.DoubtAnswersModelVS,basename = 'answers')
router.register('',views.DoubtModelVS,basename = 'doubts')


# /api/doubts/
urlpatterns = [

path('', include(router.urls)),

 
 
# path('course/<str:course_id>',views.DoubtsByCourse.as_view(),name = "doubts-by-course"),
# path('chapter/<str:chapter_id>',views.DoubtsByChapter.as_view(),name = "doubts-by-chapter"),
# path('',include(router2.urls)),
]


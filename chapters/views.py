from rest_framework.exceptions import ValidationError
from courses.models import Course
from chapters.models import VideoChapter
from orders.models import Subscription
from chapters.serializers import ChapterSerializer,ChapterDetailSerializer,VideoChapterSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from chapters.models import Chapter, chapter_choices, chapter_choices_description, video_plateform_choices
from rest_framework import status
from rest_framework.permissions import IsAdminUser
# from core.permissions import isAdminUserOrReadOnly
import uuid


@api_view(['GET'])
def ChapterTypes(request):

    def searchDescription(id):
        for _id, description in chapter_choices_description:
            if id == _id:
                return description

    types = map(lambda e: dict(
        id=e[0], type=e[1],description=searchDescription(e[0]) ), chapter_choices)
    return Response(types)


@api_view(['GET'])
def VideoPlateform(request):

    plateforms = map(lambda e: dict(
        id=e[0], plateform=e[1]), video_plateform_choices)
    return Response(plateforms)


class ChapterList(ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    ordering = ['index']
    
    def get(self, request, *args, **kwargs):
            try:
              course = self.kwargs.get('course')
              uuid.UUID(course)
            except:
              return Response({"course": ["Course id is not valid"]}, status=status.HTTP_400_BAD_REQUEST)

            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course = self.kwargs.get('course')
        return Chapter.objects.filter(parent_chapter=None, course=Course(pk=course))
      

class ChapterCreate(CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    # permission = IsAdminUser

   
    def get_serializer(self,*args, **kwargs):

        request = self.request
        # print(request.data)
        serializer = self.serializer_class(
            data=request.data, context={"request":  request, "full": True})
        serializer.is_valid()
        return serializer
            
        
class ChapterDetail(APIView):

    def get(self, request, **kargs):
        chapter_id = kargs.get('pk')
        user = request.user
        print(user)
        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist or ValidationError:
            return Response("not ok",status = status.HTTP_404_NOT_FOUND)
        #  user subscribed this course
        # then alwaays return full ojject data
        # add full flag in create Chapter View
        context = {
            "full": chapter.is_preview,
            "request": request
        }
        
        if user.is_authenticated:
            if(user.is_superuser):
                 context['full'] = True
            else:
                subscribed = chapter.course.is_user_enrolled(user)
                context['full'] = subscribed
    
            serailizer = ChapterSerializer(chapter, context=context)
       
            return Response(serailizer.data)
        return Response("You are not logged in")  














    
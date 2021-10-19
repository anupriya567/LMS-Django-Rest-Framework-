from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from courses.serializers import CourseSerializer,CategorySerializer,TagSerializer
from courses.models import Course,Category,Tag
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from courses.permissions import IsAdminOrReadOnly
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from courses.pagination import CoursePagination
# from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from watchlist_app.api.pagination import  WatchListPagination,WatchListCPagination


class CourseVS(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer 
    filterset_fields = ['category','slug', 'price','discount']  
    search_fields = ['title']        
    ordering_fields = ['price']
    pagination_class = CoursePagination
        
    
    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        if tag is not None:
            courses = Tag.objects.filter(tag=tag).values_list('course')
            return self.queryset.filter(pk__in=courses)
        return self.queryset

    def create(self, request, *args, **kwargs):
        course = request.data
        category_id = Course.get('category_id')
        # course.pop('category_id')

        category = None
        if category_id is None:
            return Response({'category_id': ['category_id is required.']}, status= status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist or ValidationError:
            return Response({'category_id': ['category_id is not valid.']}, status= status.HTTP_400_BAD_REQUEST)

        context = {
            "request": request
        }
        serializer = CourseSerializer(data=course, context=context)
        if(serializer.is_valid()):
            courseInstance = Course(
                **serializer.validated_data, category=category)
 
            courseInstance.save()
            return Response(CourseSerializer(courseInstance, context=context).data)

        return Response(serializer.errors,  status= status.HTTP_400_BAD_REQUEST)

class CategoryVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 

class TagVS(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer 

    def create(self, request, *args, **kwargs):
        tag = request.data
        course_id = tag.get('course')
        
        course = None
        try:
           course = Course.objects.get(pk = course_id)
        except Course.DoesNotExist or ValidationError:
            return Response({'course': ['course id is invalid']})
        
        serializer = TagSerializer(data = tag)
        if serializer.is_valid():
            tag = Tag(self,**serializer.validated_data,course = course)
            tag.save()
            return Response(TagSerializer(tag).data)
        else:
            return Response(serializer.errors)

class CourseDetailSlug(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 

class CategoryDetailSlug(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    
class CoursesByCategory(APIView):

    def get(self, request,category_id):
        try:
           courses = Course.objects.filter(category__id = category_id)  

        except ValidationError:
          return Response({"course id": ["No courses for this category"]}, status= status.HTTP_400_BAD_REQUEST)

        serializer = CourseSerializer(courses,many = True)
        return Response(serializer.data)





































# class CategoryList(generics.ListCreateAPIView):
    

# class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class CourseList(APIView): 

#     def get(self,request):
#         courses = Course.objects.all()    
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = CourseSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Chapter,LinkChapter,HeadingChapter,TextChapter,VideoChapter
from rest_framework.serializers import ModelSerializer,Serializer

def changeChapterData(instance):
    chapter_type = instance.chapter_type

    if(chapter_type == 'T'):
        chapter = instance.text_chapter
        instance.text_chapter = TextChapter(title=chapter.title, id=chapter.id)

    if(chapter_type == 'L'):
        chapter = instance.link_chapter
        instance.link_chapter = LinkChapter(id=chapter.id, title=chapter.title)

    if(chapter_type == 'V'):
        chapter = instance.video_chapter
        instance.video_chapter = VideoChapter(id=chapter.id, title=chapter.title)

    return instance

class LinkChapterSerializer(ModelSerializer):
    chapter = serializers.UUIDField(required=False)
    class Meta:
        model = LinkChapter
        fields = '__all__'   

    def to_representation(self, instance):
        original_object = super().to_representation(instance)
        original_object.pop('chapter') 
        return original_object
        

class HeadingChapterSerializer(ModelSerializer):
    chapter = serializers.UUIDField(required=False)
    class Meta:
        model = HeadingChapter
        fields = '__all__'  

    def to_representation(self, instance):
        original_object = super().to_representation(instance)
        original_object.pop('chapter')    
        return original_object     


class TextChapterSerializer(ModelSerializer):
    chapter = serializers.UUIDField(required=False)
    class Meta:
        model = TextChapter
        fields = '__all__' 

    def to_representation(self, instance):
        original_object = super().to_representation(instance)
        original_object.pop('chapter')        
        return original_object
   

class VideoChapterSerializer(ModelSerializer):
    chapter = serializers.UUIDField(required=False)

    class Meta:
        model = VideoChapter
        fields = '__all__'

    def to_representation(self, instance):
        original_object = super().to_representation(instance)
        original_object.pop('chapter')        
        return original_object    

class ChildChapterSerializer(ModelSerializer):
    index = serializers.IntegerField(required=False)
    heading_chapter = HeadingChapterSerializer(read_only=True)
    link_chapter = LinkChapterSerializer(read_only=True)
    video_chapter = VideoChapterSerializer(read_only=True)
    text_chapter = TextChapterSerializer(read_only=True)
    
    class Meta:
        model = Chapter
        fields = '__all__'

    def to_representation(self, instance):
        full = self.context.get("full")
        if not full:
            instance = changeChapterData(instance)

        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user
        course = instance.course
        data['is_enrolled'] = course.is_user_enrolled(user)
        return data 
            

class ChapterSerializer(ModelSerializer):
    index = serializers.IntegerField(required=False)
    heading_chapter = HeadingChapterSerializer(read_only=True)
    link_chapter = LinkChapterSerializer(read_only=True)
    video_chapter = VideoChapterSerializer(read_only=True)
    text_chapter = TextChapterSerializer(read_only=True)
    child_chapters = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        full = self.context.get("full")
        if not full:
            instance = changeChapterData(instance)
         
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user
        course = instance.course
        data['is_enrolled'] = course.is_user_enrolled(user)
        return data  
    
       
    def get_child_chapters(self,instance):
        childs = instance.child_chapters.all().order_by('index')
        serializer = ChildChapterSerializer(childs, many=True,context = self.context)
        return serializer.data
    
    class Meta:
        model = Chapter
        fields = '__all__'


    def create(self, validated_data):
        # print(validated_data)
        data = self.context.get('request').data
        chapter_type = data.get('chapter_type')
        chapter_type_object = None
        # print(chapter_type)

        if(chapter_type == 'H'):
            chapter_type_object = self.handleHeadingChapter(data)
            print(chapter_type_object)

        if(chapter_type == 'T'):
            chapter_type_object = self.handleTextChapter(data)

        if(chapter_type == 'V'):
            chapter_type_object = self.handleVideoChapter(data)  
        
        if(chapter_type == 'L'):
            chapter_type_object = self.handleLinkChapter(data)    
        
        print("validated data", validated_data)
        chapter = Chapter(**validated_data)
        course = chapter.course
        parent_chapter = validated_data.get('parent_chapter')
        

        if chapter.parent_chapter is None:
            last_index_parent_ch = Chapter.objects.filter(course = course,parent_chapter = None).count()
            chapter.index = last_index_parent_ch + 1   
        
        else:
          # find index of child chapter
            totalChilds = Chapter.objects.filter(
                parent_chapter=parent_chapter).count()
            chapter.index = totalChilds+1
            
        chapter.save()    
        chapter_type_object.chapter = chapter 
        chapter_type_object.save() 
        return chapter

    def handleHeadingChapter(self, raw_json):
        heading_chapter_raw = raw_json.get('heading_chapter')
        if not heading_chapter_raw:
            raise ValidationError(
                {"heading_chapter": ["heading_chapter is required"]})

        header_chapter_serializer = HeadingChapterSerializer(
            data=heading_chapter_raw)

        if header_chapter_serializer.is_valid():
            print("heading data:",header_chapter_serializer.validated_data)
            return HeadingChapter(**header_chapter_serializer.validated_data )
        else:
            raise ValidationError(
                {"heading_chapter": header_chapter_serializer.errors})
        

    def handleTextChapter(self, raw_json):
        text_chapter_raw = raw_json.get('text_chapter')
        if not text_chapter_raw:
            raise ValidationError(
                {"text_chapter": ["text_chapter is required"]})

        text_chapter_serializer = TextChapterSerializer(
            data=text_chapter_raw)

        if text_chapter_serializer.is_valid():
            return TextChapter(**text_chapter_serializer.validated_data )
        else:
            raise ValidationError(
                {"text_chapter": text_chapter_serializer.errors})
        

    def handleLinkChapter(self, raw_json):
        link_chapter_raw = raw_json.get('link_chapter')
        if not link_chapter_raw:
            raise ValidationError(
                {"link_chapter": ["link_chapter is required"]})

        link_chapter_serializer = LinkChapterSerializer(
            data=link_chapter_raw)

        if link_chapter_serializer.is_valid():
            return LinkChapter(**link_chapter_serializer.validated_data )
        else:
            raise ValidationError(
                {"link_chapter": link_chapter_serializer.errors})


    def handleVideoChapter(self, raw_json):
        video_chapter_raw = raw_json.get('video_chapter')
        if not video_chapter_raw:
            raise ValidationError(
                {"video_chapter": ["video_chapter is required"]})

        video_chapter_serializer = VideoChapterSerializer(
            data=video_chapter_raw)

        if video_chapter_serializer.is_valid():
            return VideoChapter(**video_chapter_serializer.validated_data )
        else:
            raise ValidationError(
                {"video_chapter": video_chapter_serializer.errors})


class ChapterDetailSerializer(Serializer):
    index = serializers.IntegerField(required=False)
    heading_chapter = HeadingChapterSerializer(read_only=True)
    link_chapter = LinkChapterSerializer(read_only=True)
    video_chapter = VideoChapterSerializer(read_only=True)
    text_chapter = TextChapterSerializer(read_only=True)

                     
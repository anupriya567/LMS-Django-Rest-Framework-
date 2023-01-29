# LMS-Django-Rest-Framework-

## Learning Management System(LMS) using Django RestFramework-
I build rest apis to handle CRUD and other requests

### Basic Endpoint 
/courses/ => list of all courses</br>
/course/1 => course detail of course with id = 1</br>


### Structure that we want to show in our project
</br>
Module 1 - Installation</br>
             1. set up VS code</br>
             2. virtual env set up</br>
             3. install python & django</br>

</br>
Module 2 - .............</br>
          -</br>
          -</br>
          -</br>
</br>
How we can do this-            
```             
model:
 Mainchapter(heading type)
 
 SubChapter(video, text, link) 
```

or

```
model - Chapter(heading, video, text, link)
```
</br>

### Why making tag app? 
Tag for searching a course
</br>

### Why creating multiple apps in project?
Creating apps-

dividing the whole big project into different smaller apps makes it managable, less complex and easy to debug
  ```
  'coupon',
    'chapter',
    'doubt',
    'review',
    'course',
    'order'
```
</br>

### Database
</br>
Database -> MySQL</br>
to view tables and db -> MySQLWorkbench</br>
to test api, we need a client -> (Postman)[https://www.postman.com/]</br>
Postman is an API platform for developers to design, build, test and iterate their APIs.
</br>

```
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : DB_NAME,
        'PORT' : DB_PORT,
        'HOST' : DB_HOST,
        'USER' : DB_USER,
        'PASSWORD' : DB_PASSWORD
    },
```
> client = postman</br>
> server = MySQL server</br>
> Db = MySql</br>
> client, server, db on same computer = > tier 1 architecture</br>


</br>

### Error - not use @api_view decorator

```
AssertionError at /api/course/test
.accepted_renderer not set on Response
Request Method:	GET
Request URL:	http://127.0.0.1:8000/api/course/test
Django Version:	4.1.4
Exception Type:	AssertionError
Exception Value:	
.accepted_renderer not set on Response
```

### *Why we are using 'slug' if we are having 'id' to uniquely identify a category or a course

for URL Mapping

endpoint for fetching course-detail
using id - 
> api/course/2

using slug - 
> api/course/pythonDevelopment

url using slug is much understandable

SlugField
```
class SlugField(max_length=50, **options)
```
Slug is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs.

### Django Generic Views [https://www.django-rest-framework.org/api-guide/generic-views/]

Django’s generic views were developed to ease that pain. They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to write too much code.


### Returning URLs[https://www.django-rest-framework.org/api-guide/reverse/]
It's probably better practice to return absolute URIs from your Web APIs, such as http://example.com/foobar, 
rather than returning relative URIs, such as /foobar

### Why use namespace?

test-api, present in multiple apps

for getting absolute url - 
```
reverse(view-name, request = request)
{
   "API Test" : reverse('test-api', request = request)
}
```
o/p - api/coupons/test</br>
test api coupons app ki choose kr li h</br>

but if we want ki course app ki hi test api ho</br>
so add namespace also</br>
```
 path('api/', include(('course.urls', 'course'), namespace = 'course'))
```
### Getting view name from viewsets

basename = course</br>

for getting complete list of courses</br>
view name = course-list</br>

detail of a course</br>
view name = course-detail</br>
```
{
'CourseList' : reverse('course: course-list', request = request),
'CourseDetail' : reverse('course: course-detail', request = request),
}
```

```
course_router = DefaultRouter()
course_router.register('',views.CourseVS,basename="course")

```

### 1)  Same App but used with different Base Urls

- We want to add subscription in Order App
- Subscription list, subscription detail
but 

url will be like (baseurl for Order app is:- /api/orders/):-

```
/api/orders/subscription-list
/api/orders/subscription-detail
```
but we want something like 
```
/api/subscription/list
/api/subscription/detail
```
how can we do so as 
url is of Order App, so base url will be ```/api/orders```
Can be done as follows:-

models.py:-
```
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
```





base url:-  /api/orders/
```
OrderUrls = [
   
path('create-order/',views.CreateOrder.as_view(),name = 'create-order'),
path('validate-payment/',views.ValidatePayment.as_view(),name = "validate-payment")

]
SubscriptionUrls= [
   
path('',views.SubscriptionList.as_view(),name = 'subscription-list'),


]
```

### 2) If field is foreign key in models.py, and we display the model object

```
class Subscription(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='subscriptions')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'   

```
```
class SubscriptionSerializer(ModelSerializer):
   
    class Meta:
        model = Subscription
        fields = '__all__'
```

Initially result will be like:-

```
Subscription List
GET /api/subscriptions/
HTTP 200 OK
Allow: GET, HEAD, OPTIONS

[
    {
        "id": "6542e4e1-936e-471b-9aec-e2d1de1b540d",
        "time": "2021-10-18T14:44:51.992461Z",
        "course": "1d5fc6bd-9376-499f-a4b8-3a59a3893ceb",
        "order": "6b454a13-4735-4e1f-8d11-669550d9d2f3",
        "user": 1
    },
    {
        "id": "eab14832-f5bf-4846-8328-135fd71aea68",
        "time": "2021-10-18T14:44:51.592670Z",
        "course": "133cc1de-7e0e-489e-9e6e-e72fa9dc1f9e",
        "order": "6b454a13-4735-4e1f-8d11-669550d9d2f3",
        "user": 1
    }
]
```

Doing these changes in serializers.py
```
class SubscriptionSerializer(ModelSerializer):
    # course = serializers.CharField(source = 'course.title')
    course = CourseSerializer(read_only = True)
    user = serializers.CharField(source = 'user.username')
    order = serializers.CharField(source = 'order.order_id')
  
    class Meta:
        model = Subscription
        fields = '__all__'
```
Output - 
- entire course object is displayed
- instead of user id, username is displayed
- instead of order id, order_id is displayed
```
Subscription List
GET /api/subscriptions/
HTTP 200 OK


[
    {
        "id": "6542e4e1-936e-471b-9aec-e2d1de1b540d",
        "course": {
            "id": "1d5fc6bd-9376-499f-a4b8-3a59a3893ceb",
            "tags": [],
            "category": "Dance",
            "title": "Hip Hop Bootcamp",
            "slug": "hip-hop-bootcamp",
            "instructor": "Anupriya",
            "language": "English/Hindi",
            "description": "Easy to learn",
            "tagline": "Let's get started",
            "price": 500,
            "active": true,
            "discount": 0,
            "duration": 10,
            "thumbnail": "http://127.0.0.1:8000/media/thumbnails/pexels-haste-leart-v-690597.jpg",
            "resource": "http://127.0.0.1:8000/media/resource/certificate.pdf",
            "is_enrolled": true,
            "students_enrolled": 1
        },
        "user": "flyhigh",
        "order": "order_IApnQeMIQhAQgb",
        "time": "2021-10-18T14:44:51.992461Z"
    }
]
```

### 3)  Remove field which you do not want to display, but they are part of model it is the part of mode

> Data of json representation will be like-
```
 def to_representation(self, instance):
        json = super().to_representation(instance)
        json.pop('user')
        return json
```
### 4) Display fields in Admin Panel

```
from django.contrib import admin
from .models import Review

class ReviewAdminModel(admin.ModelAdmin):
    model = Review
    list_editable = ['active']
    list_display = ['course','user','rating','active']


admin.site.register(Review,ReviewAdminModel)
```

### Getting user from context

> not always you can get user from
```
user = request.user
```
- here, how can we get request -> context k pass se hai
- and how'll can we target context -> self.context

  ``` user = self.context.get('request').user```
```
class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get('request').user
        course = validated_data.get('course')
        try:
            review = user.reviews.all().get(course=course)
            return super().update(review, validated_data=validated_data)
        except Review.DoesNotExist:
            pass

        return super().create(validated_data)
```
### 5) What is the significance of related_name

- course model doesn't have any field for reviews
- Let'say, that we are haivng an object of course model then how can we get all its reviews
- by using course.reviews
- how it is possible??
- course is Fk in review model and having related_name = reviews

```
class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')   
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=500)
    active = models.BooleanField(default= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} | {self.rating}'
```
> from the above model how can we get all reviews of a particular user
   ``` review = user.reviews.all().get(course=course)```





### 6) Discussing error in this
- suppose you are logged in with ironman 
- print(logged_in_user)
- print(body_user)
- print(logged_in_user == body_user)

o/p-

- ironman
- ironman
- False

***Why this error?***

> POST req. on ``` http://127.0.0.1:8000/api/reviews/ ```
```
    {
        "user": ironman",
        "rating": 5,
        "description": "5 star",
        "course": "1d5fc6bd-9376-499f-a4b8-3a59a3893ceb"
    }
 ```
 ```
class AddOwnReviewOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'POST' :
            logged_in_user = request.user
            body_user = request.data.get('user')
            if logged_in_user != body_user:
                raise ValidationError("You cannot add a review  
        return True   
 ```
- body_user is string
- logged_in_user is object

``` print(logged_in_user.username == body_user)```
 True


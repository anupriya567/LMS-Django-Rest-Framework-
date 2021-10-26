from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from orders.serializers import OrderSerializer, OrderItemSerializer, SubscriptionSerializer, OrderValidateSerializer,OrderCreateSerializer
from courses.serializers import CourseSerializer
from orders.models import Order, OrderItem, Subscription
from coupons.models import Coupon
from courses.models import Course
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
import razorpay
from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from shortuuid import ShortUUID
import traceback

# Create your views here.

KEY = "rzp_test_6zxl3GT14gCLe6"
SECRET = "zSN2jj9lctlgPCclradT0egb"

class CreateOrder(APIView):
    # permission_classes = [IsAuthenticated]

    def createRazorpayOrder(self ,user,amount):
        client = razorpay.Client(auth=(KEY, SECRET))
        DATA = {
            "amount": amount,
            "currency": "INR",
            "receipt": f'feelfreetocode-{ShortUUID().random(length=6).upper()}',
            "notes": {
                "id": user.id,
                "username": user.username,
            }
           
            }
        order = client.order.create(data=DATA)
        return order
    
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            course = data.get('course')
            d_courses = data.get('courses')
            coupon_code = data.get('coupon')
            courses = set()

            if course:
                courses = {course}

            if d_courses:
                courses = set(d_courses)
            
            coupon_available  = False
            cdiscounts = []
            for course in courses:
                course = Course.objects.get(id=course)
                coupon = Coupon.objects.get(active=True, course = course, code = coupon_code)
                if coupon:
                    coupon_available  = True
                    cdiscounts.append(coupon.discount)
                else:
                    return Response("Coupon not applicable")  
                   
            
            # if not coupon_available:
            #     return Response("Coupon not applicable")

            coupon_dicount =  max(cdiscounts) 
            selling_price = 0
            for course in courses:
                course = Course.objects.get(id=course)
                discount = course.price * course.discount * 0.01
                selling_price+= course.price - discount

            coupon_discount = selling_price * coupon_dicount * 0.01   
            selling_price = selling_price - coupon_discount 
            print(selling_price)    
            print(request.user)

            rp_order = self.createRazorpayOrder(request.user, selling_price*100)
            order = Order(order_id = rp_order.get('id'), user=request.user)
            order.save()
            context = {"Success": "done","order": rp_order}

            # creating order item
            for course in courses:
                course = Course.objects.get(id=course)
                order_item = OrderItem(course = course, order = order,price = course.price, discount = course.discount)
                if coupon_available:
                  order_item.coupon = Coupon.objects.get(active=True, course = course, code = coupon_code)
                order_item.save()
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    


class ValidatePayment(APIView):
    def post(self, request):
        serializer = OrderValidateSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            payment_id = data.get('razorpay_payment_id')
            order_id = data.get('razorpay_order_id')
            signature = data.get('razorpay_signature')

            try:
                order = Order.objects.get(order_id=order_id)
                if(order.order_status == "S"):
                    return Response({'order': "Order Already Completed"}, status=status.HTTP_400_BAD_REQUEST)
                params_dict = {
                    'razorpay_order_id': order.order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                client = razorpay.Client(auth=(KEY, SECRET))
                client.utility.verify_payment_signature(params_dict)
                order.order_status = "S"
                order.payment_id = payment_id
                order.save()
                
                
            except:
                traceback.print_exc()
                return Response({"order": "order is not valid"},  status=status.HTTP_400_BAD_REQUEST)

            return Response(OrderSerializer(order).data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
                
class SubscriptionList(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAdminUser]
       
class CourseSubscribedByUser(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        
        # courses ki id hai
        courses = Subscription.objects.filter(user__username=pk).values_list('course')

        # course object hai
        self.queryset = Course.objects.filter(pk__in = courses)

        if not user.is_superuser:
            if pk != user.username:
                return Response({"detail": "You are not authorized."},  status=status.HTTP_403_FORBIDDEN)

        return super().get(request, *args, **kwargs)



   


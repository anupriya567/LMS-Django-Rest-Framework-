from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from orders.models import Subscription
from . models import Review


class AddOwnReviewOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'POST' :
            logged_in_user = request.user
            body_user = request.data.get('user')
            if logged_in_user.username != body_user:
                raise ValidationError("You cannot add a review")
        return True   


class AddUpdateReviewToEnrolledCourseOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):

        if request.method == 'POST' :
            logged_in_user = request.user
            body_course = request.data.get('course')
            enrolled = Subscription.objects.get(user = logged_in_user , course = body_course)
            # print(logged_in_user)
            # body_user = request.data.get('user')
            
            message = {
                    "course": "Cant add review in this course , you are not enrolled."}

            if enrolled == None:
                raise ValidationError(message)

            
        if request.method == 'PUT' :
            logged_in_user = request.user
            body_course = request.data.get('course')
            enrolled = Subscription.objects.get(user = logged_in_user , course = body_course)
            
            
            message = {
                    "course": "Cant update review in this course , you are not enrolled."}

            if enrolled == None:
                raise ValidationError(message)


        return True           


class DeleteOwnReviewOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):

        if request.method == 'DELETE':
                    review_pk = view.kwargs.get('pk')
                    if Review.objects.filter(pk=review_pk, user=request.user).count() == 0:
                        raise ValidationError(
                            {'details': 'you are not authorized to delete tis review'})

        return True
           
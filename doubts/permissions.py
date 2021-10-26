from rest_framework import permissions
from . models import Doubt,DoubtAnswers
from rest_framework.exceptions import ValidationError

class UpdateDeleteOwnDoubtOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        method = request.method
        if method in ['PUT','DELETE','PATCH']:
            user = request.user
            if user.is_superuser:
                return True

            doubt_id = view.kwargs.get('pk')
            try:
                doubt = Doubt.objects.get(id = doubt_id)
                return doubt.user == user
            except Doubt.DoesNotExist:
                return ValidationError("You do not have permission to do this task")    

        return True


class UpdateDeleteOwnDoubtAnsOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        method = request.method
        if method in ['PUT','DELETE','PATCH']:
            user = request.user
            if user.is_superuser:
                return True

            doubt_id = view.kwargs.get('pk')
            try:
                doubtanswer = DoubtAnswers.objects.get(id = doubt_id)
                return doubtanswer.user == user
            except DoubtAnswers.DoesNotExist:
                return ValidationError("You do not have permission to do this task")    

        return True

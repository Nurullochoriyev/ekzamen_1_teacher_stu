from rest_framework import serializers
from ..models.model_student import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['user','group','is_line','descriptions']


class StudentUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    class Meta:
        abstract=True
        model=User
        fields=('id','phone_number','password','email','is_active', 'is_teacher', 'is_student', 'is_staff','is_admin')
class StudentSerializerPost(serializers.Serializer):
    user=StudentUserSerializer()
    student=StudentSerializer()

from ..models.model_teacher import *
from rest_framework import serializers
class Teacher_Serializers(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=['id','user','departments','course','descriptions']
class TeacherUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    class Meta:
        abstract=True
        model=User
        fields=('id','phone_number','password','email','is_active', 'is_teacher', 'is_student', 'is_staff','is_admin')
class TeacherSerializerPost(serializers.Serializer):
    user=TeacherUserSerializer()
    teacher=Teacher_Serializers()






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'id', 'phone_number', 'password','email', 'is_active', 'is_staff', "is_teacher", 'is_admin', 'is_student')

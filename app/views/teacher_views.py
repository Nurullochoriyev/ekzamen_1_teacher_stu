from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers.teacher_serializers import *
from app.serializers.teacher_serializers import Teacher_Serializers
from ..models import *
from django.shortcuts import get_object_or_404





class Teacher_api(APIView):
    @swagger_auto_schema(
        responses={
            200: TeacherSerializerPost(many=True),
            400: "Noto'g'ri so'rov"
        }
    )
    def get(self,request):
        data={'success':True}
        teacher=Teacher.objects.all()
        serializers=Teacher_Serializers(teacher,many=True)
        data["teacher"]=serializers.data
        return Response(data=data)

    @swagger_auto_schema(request_body=TeacherSerializerPost)
    def post(self,request):
        data={'success':True}
        try:
            user=request.data['user']
            teacher=request.data['teacher']


            user_serializer=UserSerializer(data=user)
            if not user_serializer.is_valid():
                return Response(
                    data={'success':False,'hatolar':user_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST

                )
            malumot=user_serializer.validated_data
            malumot['password']=make_password(malumot.get('password'))
            malumot['is_teacher']=True
            malumot['is_active']=True

            foydalanuvchi=user_serializer.save()

            teacher['user']=foydalanuvchi.id
            uqtuvchi_serializer=Teacher_Serializers(data=teacher)
            if not uqtuvchi_serializer.is_valid():
                return  Response(
                    data={'success':False,'hatoliklar':uqtuvchi_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            uqtuvchi_serializer.save()
            data['data']=user_serializer.data
            return Response(data=data,status=status.HTTP_201_CREATED)
        except KeyError as hato:
            return Response(
                data={'success':False,'habar':f"sorovda yetishmayotgan kalit {str(hato)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as hato:
            return Response(
                data={'success':False,"habar":str(hato)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="O'chiriladigan o'qituvchi IDsi",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Muvaffaqiyatli o'chirildi",
            404: "O'qituvchi topilmadi",
            500: "Server xatosi"
        }
    )
    def delete(self,request):
        data={'success':True}
        try:
            teach_id=request.GET.get('id')
            if not teach_id:
                return Response(
                    data={'success':False,'hatolik':'id talab qilinadi'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            techer=get_object_or_404(Teacher,id=teach_id)
            user=techer.user
            with transaction.atomic():
                techer.delete()
                user.delete()
            return Response(
                data={'success':True,'habar':'oqtuvchi mufaqiyatli ochrildi'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Teacher.DoesNotExist:
            return Response(
                data={'success':False,'habar':'uqtuvchi topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        except  Exception as hato:
            return Response(
                data={'success':False,"habar":str(hato)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
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

    def put(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = Teacher_Serializers(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = Teacher_Serializers(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)















    #
    # @swagger_auto_schema(
    #     operation_description="O'qituvchi ma'lumotlarini to'liq yangilash (PUT)",
    #     request_body=TeacherSerializerPut,  # Yangi serializer yaratishingiz kerak
    #     responses={
    #         200: Teacher_Serializers(),
    #         400: "Validation error",
    #         404: "Not found"
    #     }
    # )
    # def put(self, request, pk):
    #     data = {'success': True}
    #     try:
    #         print('tttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
    #         # O'qituvchini topamiz
    #         teacher = get_object_or_404(Teacher, pk=pk)
    #         print(teacher,"saloooooooooooooooooooooooooooooooooooooooooooooom")
    #         # Ma'lumotlarni validatsiya qilamiz
    #         serializer = Teacher_Serializers(teacher, data=request.data)
    #         print(serializer,'ttttttttttttttgggggggggggg========================')
    #         if not serializer.is_valid():
    #             print('))))))))))))))))))))))))))))))))))))))))))))))))______________________')
    #             return Response(
    #                 {'success': False, 'errors': serializer.errors},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #
    #         # Yangilashni transaction ichida bajaramiz
    #         with transaction.atomic():
    #             serializer.save()
    #
    #             # Agar user ma'lumotlari ham yangilansa
    #             if 'user' in request.data:
    #                 user = teacher.user
    #                 user_serializer = UserSerializer(user, data=request.data['user'], partial=True)
    #                 if not user_serializer.is_valid():
    #                     return Response(
    #                         data={'success': False, 'errors': user_serializer.errors},
    #                         status=status.HTTP_400_BAD_REQUEST
    #                     )
    #                 user_serializer.save()
    #
    #         data['data'] = serializer.data
    #         data['message'] = "O'qituvchi ma'lumotlari muvaffaqiyatli yangilandi"
    #         return Response(data=data, status=status.HTTP_200_OK)
    #
    #     except Exception as error:
    #         print('================================================')
    #         return Response(
    #             {'success': False, 'message': str(error)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )
















    # def put(self, request, pk):
    #     try:
    #         teacher = Teacher.objects.get(pk=pk)
    #     except Teacher.DoesNotExist:
    #         return Response(
    #             {"success": False, "error": "O'qituvchi topilmadi"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #
    #     serializer = Teacher_Serializers(teacher, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {"success": True, "data": serializer.data},
    #             status=status.HTTP_200_OK
    #         )
    #     return Response(
    #         {"success": False, "errors": serializer.errors},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
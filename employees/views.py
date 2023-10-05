from django.shortcuts import render,redirect
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from .serializers import UserSerializer,EmployeeSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt,datetime
from .models import *

class RegisterEmployee(APIView):
    def post(self, request):
        alredy_exist_email = User.objects.filter(email=request.data['email']).first()
        if alredy_exist_email is None:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors':serializer.errors ,'message':'data not valid'})
            employee_details = serializer.save()
            employee = Employee(employee=employee_details,department=request.data['department'],photo=request.data['photo'])
            employee.save()
            employee =User.objects.get(username = serializer.data['username'], email = serializer.data['email'])
            token_obj , _ = Token.objects.get_or_create(user=employee)
            return Response({'status': 200, 'payload':serializer.data ,'message':'data saved successfully'})
        else:
            return Response({'status': 403, 'message': 'email is alreday taken'})


# class EmployeeDetails(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self):
#         employees = User.objects.all()
#         serializers = UserSerializer(employees,many=True)
#         return Response(serializers.data)

class LoginEmployee(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')

        payload = {
            'name': user.username,
            'id': user.id,
            'is_superuser':user.is_superuser,
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                'jwt': token,
                'is_superuser': payload['is_superuser'],
            }

        return response


class EmployeeView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
           payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AdminView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        print(payload)
        if payload['is_superuser'] is True:
            employee_details = Employee.objects.all()
            employee_serializer=EmployeeSerializer(employee_details, many=True)
            # serializer = UserSerializer(employees, many=True)
            # return Response({'employee' : serializer.data,'employee_details': employee_serializer.data})
            return Response({'employee_details': employee_serializer.data})
        else:
            return Response({'message': 'Unauthenticated or you are not admin'})

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout Success'
        }
        return response

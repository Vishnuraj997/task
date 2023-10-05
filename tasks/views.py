import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from employees.serializers import TaskSerializer
from .models import *


class TaskAssignView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        print(payload)
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'data not valid'})
        serializer.save()
        return Response({'token': token, 'payload': payload, 'message': 'Task assigned Successfully', })


class TaskDetailsAdminView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        if payload['is_superuser'] is True:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)

            return Response(serializer.data)
        else:
            return Response({'message': 'Unauthenticated or you are not admin'})


class TaskDetailsEmployeeView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        tasks = Task.objects.filter(assigned_to=payload['id']).exclude(task_status="completed")
        if not tasks:
            return Response({'message': 'You have no task pending'})
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class UpdateTask(APIView):
    def post(self, request, pk):

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=404)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'data': serializer.data, 'message': 'task updated'})


class DeleteTask(APIView):
    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=404)
        task.delete()
        return Response({'message': 'Task deleted.'})

from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import action

from projects.serializers import UserListSerializer, UserDetailSerializer, TaskListSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from projects.models import User, Task

class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(deleted_at=None)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted_at = now()
        user.save()
        return Response({'detail': 'User has been deleted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def tasks(self, request, *args, **kwargs):
        obj = self.get_object()
        task = Task.objects.filter(assignee=obj)
        serializer = TaskListSerializer(task, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'patch'])
    def deactivate(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_active:
            obj.is_active = False
            obj.save()
            serializer = self.get_serializer(obj)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="User is already inactive", status=status.HTTP_400_BAD_REQUEST)








"""Кастомные экшны на UserViewSet
На существующий UserViewSet добавить два действия.
Что нужно реализовать
Экшн tasks — список задач пользователя:
Работает с конкретным объектом
GET /users/{pk}/tasks/ — вернуть все задачи, где пользователь является assignee
Сериализовать через TaskListSerializer
Экшн deactivate — деактивация пользователя:
Работает с конкретным объектом
POST /users/{pk}/deactivate/
Если is_active уже False — вернуть 400 с сообщением "User is already inactive"
Иначе выставить is_active = False, сохранить, вернуть 200"""
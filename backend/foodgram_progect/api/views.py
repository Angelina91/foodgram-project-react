from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

...
from users.models import User

from .serializers import CustomUserSerializer

...


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)

#  @action(detail=False, url_path='recent-white-cats')
#     def recent_white_cats(self, request):
#         # Нужны только последние пять котиков белого цвета
#         cats = Cat.objects.filter(color='White')[:5]
#         # Передадим queryset cats сериализатору 
#         # и разрешим работу со списком объектов
#         serializer = self.get_serializer(cats, many=True)
#         return Response(serializer.data) 


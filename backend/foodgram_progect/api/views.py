from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from http import HTTPStatus
from djoser.views import UserViewSet
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

...
from users.models import User
from posts.models import FavoriteAuthor

from .serializers import CustomUserSerializer, SubscriptionsSerializer

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

class SubscriptionsView(APIView):
    """ Подписка на автора/ отписка"""

    #permisson_classes = (IsAuthenticated,)
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        serializer = SubscriptionsSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if FavoriteAuthor.objects.filter(
            user=request.user, author=author
        ).exists():
            subscription = get_object_or_404(
                FavoriteAuthor, user=request.user, author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

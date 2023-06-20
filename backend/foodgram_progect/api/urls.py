from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, SubscriptionsView

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet, basename='users')
# router_v1.register('groups', GroupViewSet, basename='group')
# router_v1.register('follow', FollowViewSet, basename='follow')
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )

urlpatterns = [
    path(
        'v1/users/<int:id>/subscriptions/',
        SubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
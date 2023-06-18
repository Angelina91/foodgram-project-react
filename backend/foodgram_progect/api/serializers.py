from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
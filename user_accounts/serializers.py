from rest_framework import serializers

from .models import User
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'first_name', 'last_name']

    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        obj.save()
        return obj


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']


class UserImageSerializer(ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['profile_img']

    def get_profile_img(self, user):
        request = self.context.get('request')
        profile_img = user.profile_img.url
        return request.build_absolute_uri(profile_img)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

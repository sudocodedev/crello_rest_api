from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer,
    AppModelSerializer
)
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserSerializer(AppModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'profile_pic_name']

class UserInfoSerializer(AppModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uuid', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'title']

class UserLoginResponseSerializer(AppReadOnlyModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = User
        fields = ['id', 'uuid', 'email','token']

    def get_token(self, request):
        user = self.instance
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("All fields are required")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User doesn't exists")
        
        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")
        
        data['user'] = user

        return data

class UserRegisterSerializer(AppWriteOnlyModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = User
        fields = ['email', 'phone_number', 'username', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Entered passwords didn't match")
        
        return data
    
    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError("Password should be atleast 6 characters in length")
        
        return password
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_numer'),
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )

        return user
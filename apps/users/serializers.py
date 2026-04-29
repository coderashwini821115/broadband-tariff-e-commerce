# Create your serializers here.
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import CustomUser
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password_confirm', 'full_name', 'phone_number']
    password_confirm = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        return CustomUser.objects.create_user(**validated_data)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({"refresh": "The token is invalid or expired"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'phone_number', 'role']
        read_only_fields = ['id', 'email', 'role']
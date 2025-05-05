from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)  # 👈 أضف هذا السطر لو عايز تتحكم في النوع من هنا

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'is_staff']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', '')
        )
        user.is_staff = validated_data.get('is_staff', False)
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

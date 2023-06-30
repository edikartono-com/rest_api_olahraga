from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import Model

class SerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(
        write_only = True,
        required = True
    )

    class Meta:
        model = User
        fields = [
            'first_name','username',
            'password','password2','email',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if not attrs['password'] == attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Password field tidak sama'
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
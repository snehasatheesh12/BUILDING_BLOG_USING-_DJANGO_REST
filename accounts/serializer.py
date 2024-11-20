from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerialzer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is taken')
        return data
    
    def create(self, validated_data):
        user=User.objects.create(first_name=validated_data['first_name'],
                                 last_name=validated_data['last_name'],
                                 username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class loginSerilizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account not found')
        return data

    def get_jwt_token(self):
        validated_data = self.validated_data
        username = validated_data['username']
        password = validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'message': 'Invalid credentials'})

        refresh = RefreshToken.for_user(user)
        return {
            'message': 'Login successful',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }

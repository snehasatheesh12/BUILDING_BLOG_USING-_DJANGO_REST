from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *

class Blogserializers(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields='__all__'       
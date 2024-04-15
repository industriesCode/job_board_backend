from rest_framework import serializers
from .models import Job
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class JobSerializer(serializers.ModelSerializer):
    applicants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'location', 'experience', 'created_by', 'applicants']

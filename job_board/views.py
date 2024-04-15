from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from job_board.models import Job
from job_board.serializers import JobSerializer


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': username,
                'user_pk': user.pk
            }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class AllJobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class UserJobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(created_by=self.request.user)


class JobListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        # Retrieve the current authenticated user (assuming you're using token authentication)
        user = self.request.user

        # Filter jobs based on the user who created them
        queryset = Job.objects.filter(created_by=user)

        return queryset


class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

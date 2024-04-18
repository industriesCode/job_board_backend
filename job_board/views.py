from job_board.models import Job
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from job_board.serializers import JobSerializer
from rest_framework.authtoken.models import Token

"""
    Dependencies:
        rest_framework: Provides tools and libraries for building RESTful APIs.
        django.contrib.auth: Django's built-in authentication system for managing users and permissions.
        Token: Token-based authentication provided by Django REST framework.
        Models and Serializers:
        Job: Presumably a model representing job listings.
        JobSerializer: Serializer for the Job model, likely handling serialization and deserialization of job data.
"""

@api_view(['POST'])
def signup(request):
    """
        signup(request):
            1. API view for user registration.
            2. Accepts POST requests with 'username' and 'password' in the request data.
            3. Checks if the username already exists, and if not, creates a new user.
            4. Generates an authentication token for the user.
    """
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
    """
        login(request):
            1. API view for user login.
            2. Accepts POST requests with 'username' and 'password' in the request data.
            3. Authenticates the user with the provided credentials.
            4. If authentication succeeds, generates an authentication token for the user.
    """
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
    """
        AllJobListAPIView:
            1. API view to retrieve a list of all jobs.
            2. Inherits from generics.ListAPIView.
            3. Serializes and returns all job instances from the database.
    """
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class UserJobListAPIView(generics.ListAPIView):
    """
        UserJobListAPIView:
            1. API view to retrieve a list of jobs created by the current user.
            2. Inherits from generics.ListAPIView.
            3. Filters job instances based on the currently authenticated user.
    """
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(created_by=self.request.user)


class JobListCreateAPIView(generics.ListCreateAPIView):
    """
        JobListCreateAPIView:
            1. API view to retrieve a list of jobs created by the current user and create new jobs.
            2. Inherits from generics.ListCreateAPIView.
            3. Filters job instances based on the currently authenticated user and allows creating new job instances.
    """
    serializer_class = JobSerializer

    def get_queryset(self):
        # Retrieve the current authenticated user (assuming you're using token authentication)
        user = self.request.user

        # Filter jobs based on the user who created them
        queryset = Job.objects.filter(created_by=user)

        return queryset


class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        JobRetrieveUpdateDestroyAPIView:
            1. API view to retrieve, update, or delete a specific job instance.
            2. Inherits from generics.RetrieveUpdateDestroyAPIView.
            3. Provides endpoints for retrieving, updating, and deleting job instances.
            4. Overrides the put method to handle job application logic, where users can apply to jobs created by others.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, *args, **kwargs):
        job = self.get_object()
        user = request.user
        if user.pk == job.created_by:
            return Response({"error": "You cannot apply to your own job."}, status=status.HTTP_400_BAD_REQUEST)

        job.applicants.add(user)
        job.save()

        serializer = self.get_serializer(job)
        return Response(serializer.data)

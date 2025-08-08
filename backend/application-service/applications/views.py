from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Application, Interview
from .serializers import ApplicationSerializer, InterviewSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_list(request):
    """List applications for the current user"""
    if request.user.user_type == 'employer':
        applications = Application.objects.filter(employer_id=request.user.id)
    else:
        applications = Application.objects.filter(applicant_id=request.user.id)
    
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_detail(request, application_id):
    """Get application details"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user has permission to view this application
    if request.user.id not in [application.applicant_id, application.employer_id]:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_create(request):
    """Create a new application"""
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(applicant_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def application_update(request, application_id):
    """Update an application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user has permission to update this application
    if request.user.id not in [application.applicant_id, application.employer_id]:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = ApplicationSerializer(application, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def application_delete(request, application_id):
    """Delete an application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user has permission to delete this application
    if request.user.id != application.applicant_id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    application.is_active = False
    application.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_list(request, application_id):
    """List interviews for an application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user has permission to view interviews
    if request.user.id not in [application.applicant_id, application.employer_id]:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    interviews = Interview.objects.filter(application=application)
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interview_create(request, application_id):
    """Create a new interview"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user has permission to create interviews
    if request.user.id != application.employer_id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = InterviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(application=application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_detail(request, interview_id):
    """Get interview details"""
    interview = get_object_or_404(Interview, id=interview_id)
    application = interview.application
    
    # Check if user has permission to view this interview
    if request.user.id not in [application.applicant_id, application.employer_id]:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = InterviewSerializer(interview)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def interview_update(request, interview_id):
    """Update an interview"""
    interview = get_object_or_404(Interview, id=interview_id)
    application = interview.application
    
    # Check if user has permission to update this interview
    if request.user.id != application.employer_id:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = InterviewSerializer(interview, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
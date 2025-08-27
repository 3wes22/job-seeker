from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Job, Company, JobCategory, JobSkill
from .serializers import JobSerializer, CompanySerializer, JobCategorySerializer, JobSkillSerializer
from django.db import models


@api_view(['GET'])
@permission_classes([AllowAny])
def job_list(request):
    """List all jobs with optional search and filtering"""
    jobs = Job.objects.all()  # Removed is_active filter since field doesn't exist
    
    # Handle search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(location__icontains=search_query) |
            models.Q(job_type__icontains=search_query) |
            models.Q(experience_level__icontains=search_query)
        )
    
    # Handle category filter
    category = request.GET.get('category')
    if category and category != 'all':
        jobs = jobs.filter(categories__name__icontains=category)
    
    # Handle location filter
    location = request.GET.get('location')
    if location and location != 'all':
        if location.lower() == 'remote':
            jobs = jobs.filter(is_remote=True)
        elif location.lower() == 'on-site':
            jobs = jobs.filter(is_remote=False)
        # elif location.lower() == 'hybrid':
        #     jobs = jobs.filter(remote_type='hybrid')
    
    # Handle experience level filter
    experience = request.GET.get('experience')
    if experience and experience != 'all':
        jobs = jobs.filter(experience_level__icontains=experience)
    
    # Handle employment type filter
    employment_type = request.GET.get('employment_type')
    if employment_type and employment_type != 'all':
        jobs = jobs.filter(job_type__icontains=employment_type)
    
    # Order by creation date (newest first)
    jobs = jobs.order_by('-created_at')
    
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def job_detail(request, job_id):
    """Get job details"""
    job = get_object_or_404(Job, id=job_id)  # Removed is_active filter
    serializer = JobSerializer(job)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create(request):
    """Create a new job"""
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        # Extract user ID from JWT token manually
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        user_id = None
        
        if auth_header.startswith('Bearer '):
            try:
                token = auth_header.split(' ')[1]
                # Decode JWT token without verification (since we're in the same system)
                # In production, you should verify the token
                payload = AccessToken(token).payload
                user_id = payload.get('user_id')
                print(f"🔑 Decoded JWT payload: {payload}")
                print(f"🔑 User ID from token: {user_id}")
            except Exception as e:
                print(f"⚠️ Failed to decode JWT token: {e}")
                user_id = 1  # Fallback
        
        if user_id is None:
            user_id = 1  # Default fallback
        
        print(f"🔑 Using user ID: {user_id}")
        serializer.save(employer_id=user_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employer_jobs(request):
    """Get all jobs posted by the authenticated employer"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = None
    
    if auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = AccessToken(token).payload
            user_id = payload.get('user_id')
        except Exception as e:
            print(f"⚠️ Failed to decode JWT token: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user_id is None:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get jobs posted by this employer
    jobs = Job.objects.filter(employer_id=user_id).order_by('-created_at')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def job_update(request, job_id):
    """Update a job - only by the employer who posted it"""
    job = get_object_or_404(Job, id=job_id)
    
    # Verify the user owns this job
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = None
    
    if auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = AccessToken(token).payload
            user_id = payload.get('user_id')
        except Exception as e:
            print(f"⚠️ Failed to decode JWT token: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user_id != job.employer_id:
        return Response({'error': 'You can only edit your own jobs'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = JobSerializer(job, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_withdraw(request, job_id):
    """Withdraw a job posting - only by the employer who posted it"""
    job = get_object_or_404(Job, id=job_id)
    
    # Verify the user owns this job
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = None
    
    if auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = AccessToken(token).payload
            user_id = payload.get('user_id')
        except Exception as e:
            print(f"⚠️ Failed to decode JWT token: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user_id != job.employer_id:
        return Response({'error': 'You can only withdraw your own jobs'}, status=status.HTTP_403_FORBIDDEN)
    
    # Withdraw the job (set status to withdrawn and deactivate)
    job.status = 'withdrawn'
    job.is_active = False
    job.save()
    
    return Response({
        'message': 'Job withdrawn successfully',
        'job_id': job.id,
        'status': job.status
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def job_delete(request, job_id):
    """Delete a job - only by the employer who posted it"""
    job = get_object_or_404(Job, id=job_id)
    
    # Verify the user owns this job
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = None
    
    if auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = AccessToken(token).payload
            user_id = payload.get('user_id')
        except Exception as e:
            print(f"⚠️ Failed to decode JWT token: {e}")
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user_id != job.employer_id:
        return Response({'error': 'You can only delete your own jobs'}, status=status.HTTP_403_FORBIDDEN)
    
    job.is_active = False
    job.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def company_list(request):
    """List all companies"""
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def company_detail(request, company_id):
    """Get company details"""
    company = get_object_or_404(Company, id=company_id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def company_create(request):
    """Create a new company"""
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """List all job categories"""
    categories = JobCategory.objects.all()
    serializer = JobCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def skill_list(request):
    """List all job skills"""
    skills = JobSkill.objects.all()
    serializer = JobSkillSerializer(skills, many=True)
    return Response(serializer.data) 
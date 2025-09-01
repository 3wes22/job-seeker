from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job, Company
# from .models import Job, Company, JobCategory, JobSkill
from .serializers import JobSerializer, CompanySerializer
# from .serializers import JobSerializer, CompanySerializer, JobCategorySerializer, JobSkillSerializer
from django.http import JsonResponse
import json
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
    
    # Handle category filter (commented out - categories table doesn't exist)
    # category = request.GET.get('category')
    # if category and category != 'all':
    #     jobs = jobs.filter(categories__name__icontains=category)
    
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
@permission_classes([IsAuthenticated])  # SECURITY FIX: Re-enabled authentication
def job_create(request):
    """Create a new job"""
    print(f"🔍 Job creation request data: {request.data}")
    
    # Check if remote_type is in the data
    if 'remote_type' not in request.data:
        print("⚠️ remote_type field missing from request data")
    else:
        print(f"✅ remote_type field present: {request.data.get('remote_type')}")
    
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        # SECURITY FIX: Get user ID from authenticated user, not request data
        user_id = request.user.id
        if not user_id:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        print(f"🔑 Creating job for authenticated user ID: {user_id}")
        print(f"📋 Validated data: {serializer.validated_data}")
        
        # Save the job with the authenticated user ID
        job = serializer.save(employer_id=user_id)
        print(f"✅ Job created: {job.title} (ID: {job.id})")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"❌ Serializer validation errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # SECURITY FIX: Re-enabled authentication
def employer_jobs(request):
    """Get all jobs posted by the authenticated employer"""
    # SECURITY FIX: Get user ID from authenticated user, not request data
    user_id = request.user.id
    if not user_id:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    print(f"🔑 Getting jobs for authenticated employer ID: {user_id}")
    
    # Get jobs posted by this employer
    jobs = Job.objects.filter(employer_id=user_id).order_by('-created_at')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])  # SECURITY FIX: Re-enabled authentication
def job_update(request, job_id):
    """Update a job - only by the employer who posted it"""
    job = get_object_or_404(Job, id=job_id)
    
    # SECURITY FIX: Get user ID from authenticated user, not request data
    user_id = request.user.id
    if not user_id:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    print(f"🔑 Updating job {job_id} for authenticated user ID: {user_id}")
    
    # Verify the user owns this job
    if user_id != job.employer_id:
        return Response({'error': 'You can only edit your own jobs'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = JobSerializer(job, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def job_withdraw(request, job_id):
#     """Withdraw a job posting - only by the employer who posted it"""
#     job = get_object_or_404(Job, id=job_id)
#     
#     # Get the user ID from the authenticated user
#     user_id = request.user.id
#     print(f"🔑 Withdrawing job {job_id} for user ID: {user_id}")
#     
#     # Verify the user owns this job
#     if user_id != job.employer_id:
#         return Response({'error': 'You can only withdraw your own jobs'}, status=status.HTTP_403_FORBIDDEN)
#     
#     # Withdraw the job (set status to withdrawn and deactivate)
#     job.status = 'withdrawn'
#     job.is_active = False
#     job.save()
#     
#     return Response({
#         'message': 'Job withdrawn successfully',
#         'job_id': job.id,
#         'status': job.status
#     })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # SECURITY FIX: Re-enabled authentication
def job_delete(request, job_id):
    """Delete a job - only by the employer who posted it"""
    job = get_object_or_404(Job, id=job_id)
    
    # SECURITY FIX: Get user ID from authenticated user, not request data
    user_id = request.user.id
    if not user_id:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    print(f"🔑 Deleting job {job_id} for authenticated user ID: {user_id}")
    
    # Verify the user owns this job
    if user_id != job.employer_id:
        return Response({'error': 'You can only delete your own jobs'}, status=status.HTTP_403_FORBIDDEN)
    
    # DATA CONSISTENCY FIX: Update both is_active and status fields together
    job.is_active = False
    # If the job model has a status field, update it to 'closed' or 'deleted'
    if hasattr(job, 'status'):
        job.status = 'closed'
    job.save()
    
    print(f"✅ Job {job_id} marked as inactive and closed")
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
@permission_classes([IsAuthenticated])  # SECURITY FIX: Re-enabled authentication
def company_create(request):
    """Create a new company"""
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        # SECURITY FIX: Get user ID from authenticated user, not request data
        user_id = request.user.id
        if not user_id:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        print(f"🔑 Creating company for authenticated user ID: {user_id}")
        
        # Save the company with the authenticated user ID
        company = serializer.save(employer_id=user_id)
        print(f"✅ Company created: {company.name} (ID: {company.id})")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def category_list(request):
#     """List all job categories"""
#     categories = JobCategory.objects.all()
#     serializer = JobCategorySerializer(categories, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def skill_list(request):
#     """List all job skills"""
#     skills = JobSkill.objects.all()
#     serializer = JobSkillSerializer(skills, many=True)
#     return Response(serializer.data) 
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Job, Company, JobCategory, JobSkill
from .serializers import JobSerializer, CompanySerializer, JobCategorySerializer, JobSkillSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def job_list(request):
    """List all jobs"""
    jobs = Job.objects.filter(is_active=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def job_detail(request, job_id):
    """Get job details"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    serializer = JobSerializer(job)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create(request):
    """Create a new job"""
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(employer_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def job_update(request, job_id):
    """Update a job"""
    job = get_object_or_404(Job, id=job_id)
    serializer = JobSerializer(job, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def job_delete(request, job_id):
    """Delete a job"""
    job = get_object_or_404(Job, id=job_id)
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
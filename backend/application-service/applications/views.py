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
    try:
        # CRITICAL FIX: Get user info from authenticated user object
        user_id = request.user.id
        user_type = getattr(request.user, 'user_type', None)
        
        # CRITICAL FIX: Handle cases where user_type might be missing
        if not user_type or user_type == 'unknown':
            print(f"⚠️ Warning: user_type missing for user {user_id}, attempting to determine from context")
            
            # Try to determine user type from existing applications
            try:
                from .models import Application
                # Check if user has any applications as an employer
                employer_apps = Application.objects.filter(employer_id=user_id).exists()
                # Check if user has any applications as an applicant
                applicant_apps = Application.objects.filter(applicant_id=user_id).exists()
                
                if employer_apps and not applicant_apps:
                    user_type = 'employer'
                    print(f"✅ Determined user_type: {user_type} (from existing applications)")
                elif applicant_apps and not employer_apps:
                    user_type = 'job_seeker'
                    print(f"✅ Determined user_type: {user_type} (from existing applications)")
                elif employer_apps and applicant_apps:
                    # User has both types, default to job_seeker for safety
                    user_type = 'job_seeker'
                    print(f"⚠️ User has both types, defaulting to: {user_type}")
                else:
                    # No applications found, try to get from user service
                    user_type = 'job_seeker'  # Default fallback
                    print(f"⚠️ No applications found, using default user_type: {user_type}")
                    
            except Exception as e:
                print(f"⚠️ Error determining user_type from applications: {e}")
                user_type = 'job_seeker'  # Safe default
        
        if not user_id:
            return Response({
                'error': 'User ID not available in authentication',
                'details': 'Please re-authenticate to get proper user ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"🔍 Application list request - User ID: {user_id}, User Type: {user_type}")
        
        if user_type == 'employer':
            applications = Application.objects.filter(employer_id=user_id)
        else:
            applications = Application.objects.filter(applicant_id=user_id)
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"💥 Error in application_list: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application_detail(request, application_id):
    """Get application details"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to view this application
        if user_id not in [application.applicant_id, application.employer_id]:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"💥 Error in application_detail: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_create(request):
    """Create a new application"""
    try:
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'success': False,
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"📝 Creating application for user {user_id}")
        print(f"📤 Request data: {request.data}")
        
        # Validate required fields
        required_fields = ['job_id', 'employer_id']
        missing_fields = []
        
        for field in required_fields:
            if field not in request.data or request.data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return Response({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'details': {'missing_fields': missing_fields}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure proper data types
        try:
            job_id = int(request.data['job_id'])
            employer_id = int(request.data['employer_id'])
        except (ValueError, TypeError) as e:
            return Response({
                'success': False,
                'error': 'Invalid data types for job_id or employer_id',
                'details': {'job_id': request.data.get('job_id'), 'employer_id': request.data.get('employer_id')}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # SECURITY FIX: Validate that the authenticated user is NOT the employer (they can't apply to their own jobs)
        if user_id == employer_id:
            return Response({
                'success': False,
                'error': 'You cannot apply for your own job posting',
                'details': {'user_id': user_id, 'employer_id': employer_id}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user has already applied for this job
        if Application.objects.filter(job_id=job_id, applicant_id=user_id, is_active=True).exists():
            return Response({
                'success': False,
                'error': 'You have already applied for this job',
                'details': {'job_id': job_id}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Add job existence validation when job service is accessible
        # For now, we'll assume the job exists since the frontend loaded it successfully
        
        # Prepare data for serializer
        application_data = {
            'job_id': job_id,
            'employer_id': employer_id,
            'cover_letter': request.data.get('cover_letter', ''),
            'expected_salary': request.data.get('expected_salary'),
            'availability_date': request.data.get('availability_date'),
        }
        
        print(f"🔧 Prepared application data: {application_data}")
        
        # Create serializer with prepared data
        serializer = ApplicationSerializer(data=application_data, context={'applicant_id': user_id})
        
        if serializer.is_valid():
            # Create the application
            application = serializer.save()
            print(f"✅ Application created with ID: {application.id}")
            
            return Response({
                'success': True,
                'application_id': application.id,
                'message': 'Application submitted successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            print(f"❌ Validation errors: {serializer.errors}")
            return Response({
                'success': False,
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print(f"💥 Error creating application: {str(e)}")
        print(f"💥 Error type: {type(e)}")
        import traceback
        print(f"💥 Traceback: {traceback.format_exc()}")
        
        # IMPROVED ERROR HANDLING: Provide more specific error messages
        error_message = 'Server error occurred while creating application'
        if 'database' in str(e).lower():
            error_message = 'Database error occurred'
        elif 'validation' in str(e).lower():
            error_message = 'Data validation error occurred'
        elif 'permission' in str(e).lower():
            error_message = 'Permission denied'
        
        return Response({
            'success': False,
            'error': error_message,
            'details': {
                'error_type': str(type(e)),
                'error_message': str(e),
                'user_id': user_id,
                'request_data': request.data
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def application_update(request, application_id):
    """Update an application"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to update this application
        if user_id not in [application.applicant_id, application.employer_id]:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationSerializer(application, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"💥 Error in application_update: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def application_delete(request, application_id):
    """Delete an application"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to delete this application
        if user_id != application.applicant_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        application.is_active = False
        application.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        print(f"💥 Error in application_delete: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_list(request, application_id):
    """List interviews for an application"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to view interviews
        if user_id not in [application.applicant_id, application.employer_id]:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        interviews = Interview.objects.filter(application=application)
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"💥 Error in interview_list: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interview_create(request, application_id):
    """Create a new interview"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to create interviews
        if user_id != application.employer_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(application=application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"💥 Error in interview_create: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_detail(request, interview_id):
    """Get interview details"""
    try:
        interview = get_object_or_404(Interview, id=interview_id)
        application = interview.application
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to view this interview
        if user_id not in [application.applicant_id, application.employer_id]:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = InterviewSerializer(interview)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"💥 Error in interview_detail: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def interview_update(request, interview_id):
    """Update an interview"""
    try:
        interview = get_object_or_404(Interview, id=interview_id)
        application = interview.application
        
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has permission to update this interview
        if user_id != application.employer_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = InterviewSerializer(interview, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"💥 Error in interview_update: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_application_status(request, job_id):
    """Check if the current user has applied for a specific job"""
    try:
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"🔍 Checking application status for job {job_id} by user {user_id}")
        
        application = Application.objects.get(
            job_id=job_id,
            applicant_id=user_id,
            is_active=True
        )
        
        print(f"✅ Found existing application: {application.id}")
        return Response({
            'has_applied': True,
            'application_id': application.id,
            'status': application.status,
            'applied_at': application.created_at
        })
    except Application.DoesNotExist:
        print(f"ℹ️ No existing application found for job {job_id}")
        return Response({
            'has_applied': False,
            'application_id': None,
            'status': None,
            'applied_at': None
        })
    except Exception as e:
        print(f"💥 Error checking application status: {str(e)}")
        return Response(
            {'message': f'Server error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_applications(request):
    """Get all applications for the current user"""
    try:
        # Safely extract user_id
        user_id = request.user.id if hasattr(request.user, 'id') else None
        if user_id is None:
            return Response({
                'error': 'User ID not available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        applications = Application.objects.filter(
            applicant_id=user_id,
            is_active=True
        ).order_by('-created_at')
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        print(f"💥 Error in user_applications: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer
)

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens using proper settings
        refresh = RefreshToken.for_user(user)
        
        # Ensure tokens use the configured lifetime
        access_token = refresh.access_token
        access_token.set_exp(lifetime=api_settings.ACCESS_TOKEN_LIFETIME)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens using proper settings
        refresh = RefreshToken.for_user(user)
        
        # Ensure tokens use the configured lifetime
        access_token = refresh.access_token
        access_token.set_exp(lifetime=api_settings.ACCESS_TOKEN_LIFETIME)
        
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current user profile"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update current user profile"""
    serializer = UserUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': UserProfileSerializer(request.user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """List users (for admin/employer features later)"""
    users = User.objects.filter(is_active=True)
    
    # Filter by user type if specified
    user_type = request.query_params.get('user_type')
    if user_type:
        users = users.filter(user_type=user_type)
    
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """User logout endpoint"""
    # In a real app, you might want to blacklist the token
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refresh JWT token endpoint"""
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify and decode the refresh token
        token = RefreshToken(refresh_token)
        
        # Generate new access token with proper lifetime
        new_access_token = token.access_token
        new_access_token.set_exp(lifetime=api_settings.ACCESS_TOKEN_LIFETIME)
        
        return Response({
            'access': str(new_access_token),
            'refresh': refresh_token,  # Return the same refresh token
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
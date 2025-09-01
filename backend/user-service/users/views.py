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

def create_custom_tokens(user):
    """Create JWT tokens with custom claims including user_type"""
    print(f"🔍 DEBUG: Creating tokens for user {user.id}")
    print(f"🔍 DEBUG: User type: {getattr(user, 'user_type', 'NOT_FOUND')}")
    print(f"🔍 DEBUG: User fields: {[f.name for f in user._meta.fields]}")
    print(f"🔍 DEBUG: User data: id={user.id}, username={user.username}, email={user.email}")
    
    refresh = RefreshToken.for_user(user)
    
    # CRITICAL FIX: Use standard JWT field names for compatibility
    # Add custom claims to access token
    refresh.access_token['user_id'] = user.id
    refresh.access_token['username'] = user.username
    refresh.access_token['email'] = user.email
    
    # CRITICAL FIX: Ensure user_type is properly set
    user_type = getattr(user, 'user_type', None)
    if user_type:
        refresh.access_token['user_type'] = user_type
        print(f"✅ DEBUG: Added user_type to token: {user_type}")
    else:
        print(f"❌ DEBUG: user_type not found on user object")
        # Try to get from database
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            db_user = User.objects.get(id=user.id)
            user_type = db_user.user_type
            refresh.access_token['user_type'] = user_type
            print(f"✅ DEBUG: Retrieved user_type from database: {user_type}")
        except Exception as e:
            print(f"❌ DEBUG: Failed to get user_type from database: {e}")
            # Set a default value
            refresh.access_token['user_type'] = 'unknown'
            print(f"⚠️ DEBUG: Set default user_type: unknown")
    
    # CRITICAL FIX: Also add standard JWT fields for compatibility
    refresh.access_token['sub'] = str(user.id)  # Standard JWT subject field
    refresh.access_token['name'] = user.username  # Standard JWT name field
    
    # Add user_id to refresh token payload for refresh endpoint
    refresh['user_id'] = user.id
    refresh['sub'] = str(user.id)  # Standard JWT subject field
    
    # Ensure tokens use the configured lifetime
    access_token = refresh.access_token
    access_token.set_exp(lifetime=api_settings.ACCESS_TOKEN_LIFETIME)
    
    # CRITICAL FIX: Remove the problematic dict() conversion
    # The token objects can't be converted to dict directly
    print(f"🔍 DEBUG: Token created successfully for user {user.id}")
    
    return {
        'access': str(access_token),
        'refresh': str(refresh),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens using proper settings
        tokens = create_custom_tokens(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
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
        tokens = create_custom_tokens(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
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
        
        # CRITICAL FIX: Access custom claims safely from the token object
        # The token object itself has the custom claims as attributes
        user_id = getattr(token, 'user_id', None)
        if not user_id:
            # Fallback: try to get from payload
            try:
                user_id = token.payload.get('user_id')
            except (KeyError, AttributeError):
                pass
        
        if not user_id:
            return Response(
                {'error': 'Invalid refresh token - missing user information'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get the user to recreate tokens with custom claims
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate new tokens with custom claims
        new_tokens = create_custom_tokens(user)
        
        return Response({
            'access': new_tokens['access'],
            'refresh': new_tokens['refresh'],  # Return new refresh token
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Token refresh error: {str(e)}")
        return Response(
            {'error': 'Invalid refresh token'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
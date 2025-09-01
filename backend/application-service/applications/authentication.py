from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for the application service.
    This class validates JWT tokens and creates a simple user object.
    """
    
    def authenticate(self, request):
        # Get the authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return None
            
        # Extract the token
        token = auth_header.split(' ')[1]
        
        try:
            # CRITICAL FIX: Use proper JWT library and extract all required fields
            payload = jwt.decode(
                token, 
                settings.SIMPLE_JWT['SIGNING_KEY'], 
                algorithms=['HS256']
            )
            
            # CRITICAL FIX: Extract required fields with fallbacks for compatibility
            # Try custom fields first, then fall back to standard JWT fields
            user_id = payload.get('user_id') or payload.get('sub')
            user_type = payload.get('user_type') or payload.get('type') or 'unknown'
            username = payload.get('username') or payload.get('name') or ''
            email = payload.get('email') or ''
            
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token payload: missing user_id/sub')
                
            # CRITICAL FIX: Don't require user_type for now to maintain compatibility
            if not user_type or user_type == 'unknown':
                print(f"⚠️ Warning: user_type not found in token for user {user_id}, using 'unknown'")
                user_type = 'unknown'
                
            # Create a simple user object with all required fields
            user = SimpleUser(
                user_id=user_id,
                user_type=user_type,
                username=username,
                email=email
            )
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Token validation failed: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer'


class SimpleUser:
    """
    Simple user object for JWT authentication.
    This provides the minimum interface needed for DRF permissions.
    """
    
    def __init__(self, user_id, user_type, username='', email=''):
        self.id = user_id
        self.user_type = user_type
        self.username = username
        self.email = email
        self.is_authenticated = True
        self.is_anonymous = False
        
    def __str__(self):
        return f"User {self.id} ({self.user_type})"

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
            # Decode and validate the JWT token
            payload = jwt.decode(
                token, 
                settings.SIMPLE_JWT['SIGNING_KEY'], 
                algorithms=['HS256']
            )
            
            # Create a simple user object with the user_id from the token
            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token payload')
                
            # Create a simple user object
            user = SimpleUser(user_id)
            
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
    
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        self.is_anonymous = False
        
    def __str__(self):
        return f"User {self.id}"

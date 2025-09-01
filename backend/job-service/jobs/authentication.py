from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
import jwt
import logging

logger = logging.getLogger(__name__)

class JobServiceJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for job service that doesn't require local user database.
    This service validates JWT tokens and creates a minimal user object for authorization.
    """
    
    def get_raw_token(self, request):
        """
        Extract the raw token from the Authorization header.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract the token
        return auth_header.split(' ')[1]
    
    def get_validated_token(self, raw_token):
        """
        Validate the JWT token and return the payload.
        """
        try:
            # Validate the JWT token using the shared secret
            from django.conf import settings
            secret_key = settings.SIMPLE_JWT.get('SIGNING_KEY', 'django-insecure-jwt-secret-key-shared-across-services')
            
            # Decode the token
            payload = jwt.decode(raw_token, secret_key, algorithms=['HS256'])
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.error('Token has expired')
            return None
        except jwt.InvalidTokenError:
            logger.error('Invalid token')
            return None
        except Exception as e:
            logger.error(f'Token validation error: {e}')
            return None

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        Returns None if the request is not authenticated.
        """
        try:
            # Get the raw token from the Authorization header
            raw_token = self.get_raw_token(request)
            if raw_token is None:
                logger.debug("No raw token found in request")
                return None
            
            logger.debug(f"Raw token extracted: {raw_token[:20]}...")
            
            # Validate the token
            validated_token = self.get_validated_token(raw_token)
            if validated_token is None:
                logger.debug("Token validation failed")
                return None
            
            logger.debug(f"Token validated successfully: {validated_token}")
            
            # Get the user from the validated token
            user = self.get_user(validated_token)
            if user is None:
                logger.debug("User creation failed")
                return None
            
            logger.debug(f"User created successfully: {user}")
            
            # Return the user and token tuple
            return (user, validated_token)
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    def get_user(self, validated_token):
        """
        Returns a user object that is created from the validated token.
        This user object is minimal and only contains the necessary fields for authorization.
        """
        try:
            # Extract user information from the token
            user_id = validated_token.get('user_id') or validated_token.get('sub')
            
            # Use available fields or provide defaults
            username = validated_token.get('username', f'user_{user_id}')
            email = validated_token.get('email', f'user_{user_id}@example.com')
            user_type = validated_token.get('user_type', 'unknown')
            
            if not user_id:
                logger.error("JWT token missing user_id or sub field")
                return None
            
            # Create a minimal user object for authorization
            user = JobServiceUser(
                id=user_id,
                username=username,
                email=email,
                user_type=user_type
            )
            
            logger.info(f"Created JobServiceUser from JWT token: {user}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user from JWT token: {e}")
            return None

    def authenticate_header(self, request):
        return 'Bearer'

class JobServiceUser:
    """
    Minimal user object for the job service.
    This provides the necessary interface for Django's authentication system
    without requiring a database connection to the user service.
    """
    
    def __init__(self, id, username, email, user_type, is_authenticated=True, is_anonymous=False):
        self.id = id
        self.username = username
        self.email = email
        self.user_type = user_type
        self.is_authenticated = is_authenticated
        self.is_anonymous = is_anonymous
        
        # Add standard Django user attributes
        self.pk = id
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
        
        # Add methods that Django expects
        self.has_perm = lambda perm, obj=None: False
        self.has_perms = lambda perm_list, obj=None: False
        self.has_module_perms = lambda app_label: False
        self.get_username = lambda: username
        self.get_full_name = lambda: username
        self.get_short_name = lambda: username
        
    def __str__(self):
        return f"JobServiceUser(id={self.id}, username='{self.username}', type='{self.user_type}')"
    
    def __repr__(self):
        return self.__str__()

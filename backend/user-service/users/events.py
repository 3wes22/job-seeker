import logging
from django.conf import settings
from shared.kafka_utils import get_event_publisher
from shared.events import UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent
import uuid
from django.utils import timezone

logger = logging.getLogger(__name__)

class UserEventPublisher:
    """Publisher for user-related events"""
    
    def __init__(self):
        self.publisher = get_event_publisher()
        self.topic = settings.KAFKA_TOPICS['USER_EVENTS']
        self.service_name = 'user-service'
    
    def publish_user_created(self, user):
        """Publish user created event"""
        try:
            event = UserCreatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                user_id=user.id,
                username=user.username,
                email=user.email,
                user_type=user.user_type,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='user_created',
                data=event.to_dict(),
                key=str(user.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published user_created event for user {user.id}")
            
        except Exception as e:
            logger.error(f"Failed to publish user_created event: {str(e)}")
            # Don't raise - we don't want to fail user creation due to event failure
    
    def publish_user_updated(self, user, changes=None):
        """Publish user updated event"""
        try:
            event = UserUpdatedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                user_id=user.id,
                username=user.username,
                email=user.email,
                user_type=user.user_type,
                first_name=user.first_name,
                last_name=user.last_name,
                changes=changes or {}
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='user_updated',
                data=event.to_dict(),
                key=str(user.id),
                service_name=self.service_name
            )
            
            logger.info(f"Published user_updated event for user {user.id}")
            
        except Exception as e:
            logger.error(f"Failed to publish user_updated event: {str(e)}")
    
    def publish_user_deleted(self, user_id, username):
        """Publish user deleted event"""
        try:
            event = UserDeletedEvent(
                event_id=str(uuid.uuid4()),
                timestamp=timezone.now().isoformat(),
                service_name=self.service_name,
                user_id=user_id,
                username=username
            )
            
            self.publisher.publish_event(
                topic=self.topic,
                event_type='user_deleted',
                data=event.to_dict(),
                key=str(user_id),
                service_name=self.service_name
            )
            
            logger.info(f"Published user_deleted event for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to publish user_deleted event: {str(e)}")

# Global instance
user_event_publisher = UserEventPublisher()
from django.core.management.base import BaseCommand
from users.consumers import user_service_consumer
import signal
import sys
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Start the Kafka consumer for the user service'
    
    def handle(self, *args, **options):
        """Start the Kafka consumer"""
        self.stdout.write(
            self.style.SUCCESS('Starting User Service Kafka Consumer...')
        )
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            self.stdout.write(
                self.style.WARNING('\nReceived shutdown signal. Stopping consumer...')
            )
            user_service_consumer.stop_consuming()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Start the consumer
            user_service_consumer.start_consuming()
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\nConsumer stopped by user')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Consumer failed: {str(e)}')
            )
            sys.exit(1)

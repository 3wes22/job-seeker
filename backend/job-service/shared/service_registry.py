import os
import requests
from typing import Dict, Optional
from urllib.parse import urljoin

class ServiceRegistry:
    """Centralized service discovery and communication"""
    
    _instance = None
    _services = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.services = {
                'user-service': os.getenv('USER_SERVICE_URL', 'http://localhost:8001'),
                'job-service': os.getenv('JOB_SERVICE_URL', 'http://localhost:8002'),
                'application-service': os.getenv('APPLICATION_SERVICE_URL', 'http://localhost:8003'),
                'search-service': os.getenv('SEARCH_SERVICE_URL', 'http://localhost:8004'),
                'notification-service': os.getenv('NOTIFICATION_SERVICE_URL', 'http://localhost:8005'),
                'analytics-service': os.getenv('ANALYTICS_SERVICE_URL', 'http://localhost:8006'),
            }
            self.initialized = True
    
    def get_service_url(self, service_name: str) -> Optional[str]:
        return self.services.get(service_name)
    
    def make_request(self, service_name: str, endpoint: str, method: str = 'GET', 
                    data: Dict = None, headers: Dict = None):
        """Make HTTP request to another service"""
        base_url = self.get_service_url(service_name)
        if not base_url:
            raise ValueError(f"Service {service_name} not found in registry")
        
        url = urljoin(base_url, endpoint)
        
        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as e:
            raise Exception(f"Service communication failed: {str(e)}")

# Global instance
service_registry = ServiceRegistry()
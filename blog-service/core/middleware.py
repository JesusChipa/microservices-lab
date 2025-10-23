import logging
import time
import json

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Logs every request in JSON format"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        log_data = {
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration_ms': round(duration * 1000, 2),
        }
        
        logger.info(json.dumps(log_data))
        
        return response


class AuthHeaderMiddleware:
    """Logs Authorization header for future JWT validation"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header:
            logger.info(f"Authorization header present: {auth_header[:20]}...")
        
        response = self.get_response(request)
        return response

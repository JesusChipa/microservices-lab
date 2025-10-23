from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache


def healthz(request):
    """Health check endpoint - verifies DB and Redis connectivity"""
    
    status = {
        'service': 'blog-service',
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['checks']['database'] = 'ok'
    except Exception as e:
        status['status'] = 'unhealthy'
        status['checks']['database'] = f'error: {str(e)}'
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        if result == 'ok':
            status['checks']['redis'] = 'ok'
        else:
            status['checks']['redis'] = 'error: unexpected value'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['status'] = 'unhealthy'
        status['checks']['redis'] = f'error: {str(e)}'
    
    status_code = 200 if status['status'] == 'healthy' else 503
    return JsonResponse(status, status=status_code)

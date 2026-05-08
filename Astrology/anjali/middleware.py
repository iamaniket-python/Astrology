import time
import logging

logger = logging.getLogger(__name__)

# Requests slower than this (in seconds) are logged as warnings
SLOW_REQUEST_THRESHOLD = 2.0

# Paths to skip logging entirely (static files, favicon, etc.)
IGNORED_PATHS = ("/static/", "/media/", "/favicon.ico")


class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip noisy static / media requests
        if request.path.startswith(IGNORED_PATHS):
            return self.get_response(request)

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        # Grab client IP (works behind proxies / load balancers too)
        ip = (
            request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            or request.META.get("REMOTE_ADDR", "-")
        )

        # Build a compact single-line log entry
        query = f"?{request.META['QUERY_STRING']}" if request.META.get("QUERY_STRING") else ""
        log_msg = (
            f"{request.method} {request.path}{query} "
            f"→ {response.status_code} "
            f"[{duration * 1000:.1f}ms] "
            f"ip={ip}"
        )

        # Choose log level based on status code and response time
        if response.status_code >= 500:
            logger.error(log_msg)
        elif response.status_code >= 400:
            logger.warning(log_msg)
        elif duration >= SLOW_REQUEST_THRESHOLD:
            logger.warning(f"SLOW REQUEST — {log_msg}")
        else:
            logger.info(log_msg)

        return response
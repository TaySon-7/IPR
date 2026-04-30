import time

from .metrics import http_request_duration_seconds, http_requests_total


class HttpMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - started_at

        route = self._get_route(request)
        method = request.method
        status_code = str(response.status_code)

        http_requests_total.labels(
            method=method,
            route=route,
            status_code=status_code,
        ).inc()
        http_request_duration_seconds.labels(method=method, route=route).observe(duration)

        return response

    @staticmethod
    def _get_route(request):
        match = getattr(request, "resolver_match", None)
        if match and match.route:
            return match.route
        return "unresolved"

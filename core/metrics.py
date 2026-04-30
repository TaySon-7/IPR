from prometheus_client import Counter, Histogram


http_requests_total = Counter(
    "app_http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status_code"],
)

http_request_duration_seconds = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "route"],
)

health_checks_total = Counter(
    "app_health_checks_total",
    "Total number of health endpoint checks",
    ["database_status"],
)

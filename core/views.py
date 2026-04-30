from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from .metrics import health_checks_total


@require_GET
def home(request):
    return HttpResponse("""
        <h1>Django + PostgreSQL</h1>
        <p>Приложение работает!</p>
        <p><a href="/health/">Проверка здоровья</a></p>
    """)


@require_GET
def health(request):
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"

    health_checks_total.labels(database_status=db_status).inc()

    return JsonResponse({"status": "healthy", "database": db_status})
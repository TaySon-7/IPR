from django.shortcuts import render

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    """Главная страница"""
    return render(request, "core/home.html")


@require_GET
def live(request):
    """Liveness endpoint: приложение отвечает на HTTP-запросы."""
    return JsonResponse({
        "status": "alive",
    })


@require_GET
def health(request):
    """Эндпоинт для проверки здоровья приложения и БД"""
    db_status = "ok"
    status_code = 200
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
        status_code = 503

    return JsonResponse({
        "status": "healthy" if status_code == 200 else "unhealthy",
        "database": db_status,
    }, status=status_code)

from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    """Главная страница"""
    return HttpResponse("""
        <h1>Django + PostgreSQL</h1>
        <p>Приложение работает32!</p>
        <p><a href="/health/">Проверка здоровья</a></p>
        <p><a href="/admin/">Админка</a></p>
    """)


@require_GET
def health(request):
    """Эндпоинт для проверки здоровья приложения и БД"""
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"

    return JsonResponse({
        "status": "healthy",
        "database": db_status,
    })
# Лабораторная работа №5

Django backend и отдельный React frontend на Kubernetes.
## Описание проекта

Реализованы:

- Django backend с endpoints `/live/` и `/health/`;
- отдельный React frontend в своем Docker image;
- Kubernetes Deployment/Service для backend, frontend и PostgreSQL;
- Kubernetes probes для Django, React frontend и PostgreSQL.

В проекте есть docker-compose1 для отдельного запуска PostgreSQL, docker-compose для полного запуска и бд, и приложения.
Также есть возможность развернуть приложение на kubernetes: есть deployment и service под django, React frontend и PostgreSQL.

## Сборка и публикация образов

Backend:

```commandline
docker buildx build --platform linux/amd64 -t ghcr.io/tayson-7/django-app:runserver --push .
```

Frontend:

```commandline
docker buildx build --platform linux/amd64 -t ghcr.io/tayson-7/django-app:frontend-react -f frontend/Dockerfile --push frontend
```

## Запуск Kubernetes

Образы приложения находятся в Github container registry.

```commandline
kubectl apply -f k8s/namespace
```

Подставьте свои секреты в файл `secrets-example.yml` по желанию.

```commandline
kubectl apply -f k8s/base
```

Проверка запуска:

```commandline
kubectl get pods -n django-app
kubectl get svc -n django-app
kubectl rollout status deployment/django -n django-app
kubectl rollout status deployment/frontend -n django-app
```

Frontend открывается снаружи:

```text
http://localhost:3000/
```

Backend остается внутренним сервисом Kubernetes `service-django:8000`.
React frontend обращается к нему через Nginx proxy по путям:

```text
/api/live/
/api/health/
```

## Разработчик

Туревич Максим
Email: miturevich@mai.education

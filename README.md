# Лабораторная работа №6

Django backend, отдельный React frontend и PostgreSQL-инфраструктура на Kubernetes.
## Описание проекта

Реализовано:

- Django backend с endpoints `/` и `/health/`;
- отдельный React frontend в своем контейнере;
- Kustomize overlays `dev` и `prod` для приложения;
- Helm chart приложения с `values-dev.yaml` и `values-prod.yaml`;
- отдельная PostgreSQL-инфраструктура в `infra/` через Helm и Kustomize.

В `k8s/kustomization` и `k8s/helm` нет манифестов базы данных. Приложение получает параметры подключения к PostgreSQL через `DB_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` из overlays/values.

## Сборка образов

Backend:

```commandline
docker buildx build -t ghcr.io/tayson-7/django-app:lab6-backend --push .
```

Frontend:

```commandline
docker buildx build -t ghcr.io/tayson-7/django-app:lab6-frontend -f frontend/Dockerfile --push frontend
```


## Запуск Kubernetes

### Сначала запускаете инфраструктуру

1. База данных вынесена как отдельная инфраструктура в infra:
- infra/helm
- infra/kustomization

# PostgreSQL Infrastructure

## Контракт для приложения

| Параметр | Dev                                            | Prod                                             |
|----------|------------------------------------------------|--------------------------------------------------|
| Хост | postgres-0.postgres.django-dev.svc.cluster.local | postgres-0.postgres.django-prod.svc.cluster.local |
| Порт | 5432                                           | 5432                                             |
| База | django-db                                      | django-db                                        |
| Пользователь | postgres                                       | postgres                                         |
| Пароль | В Secret `dev-password` namespace `django-dev` | В Secret `prod-password` namespace `django-prod` |

перейдите в каталог `infra/helm/postgres-infra`:

для запуска через helm:

dev-запуск
```commandline
helm upgrade --install postgres-db . --namespace=django-dev --create-namespace -f values-dev.yaml
```

prod-запуск
```commandline
helm upgrade --install postgres-db . --namespace=django-prod --create-namespace -f values-prod.yaml
```

для запуска через kustomize:
перейдите в каталог infra/:
dev-запуск:
создайте namespace 
```commandline
kubectl create namespace django-dev
```

```commandline
kubectl apply -k kustomization/overlays/dev
```

prod-запуск:
создайте namespace 
```commandline
kubectl create namespace django-prod
```

```commandline
kubectl apply -k kustomization/overlays/prod
```

### Далее запускаете приложение

2. Django backend и React frontend в k8s:
- k8s/helm
- k8s/kustomization

перейдите в каталог k8s/helm/django-app: 

для запуска через helm:

dev-запуск
```commandline
helm upgrade --install django-app . --set django.SECRET_KEY="your_key" --namespace=django-dev --create-namespace -f values-dev.yaml
```

prod-запуск
```commandline
helm upgrade --install django-app . --set django.SECRET_KEY="your_key" --namespace=django-prod --create-namespace -f values-prod.yaml
```

для запуска через kustomize:
перейдите в каталог k8s/
Если инфраструктуру запускали через kustomization, то namespace создавать уже не надо.

dev-запуск:
создайте namespace 
```commandline
kubectl create namespace django-dev
```

```commandline
kubectl apply -k kustomization/overlays/dev
```

Проверка dev:

```commandline
kubectl get pods -n django-dev
kubectl get svc -n django-dev
kubectl port-forward -n django-dev service/service-frontend 3000:3000
```

Если локальный порт `3000` уже занят, используйте:

```commandline
kubectl port-forward -n django-dev service/service-frontend 3001:3000
```

Откройте frontend:

```text
http://localhost:3000/
```

или `http://localhost:3001/`, если использовали порт `3001`.

Backend health-check доступен через frontend proxy:

```text
http://localhost:3000/api/health/
```

или `http://localhost:3001/api/health/`, если использовали порт `3001`.

prod-запуск:
создайте namespace 
```commandline
kubectl create namespace django-prod
```

```commandline
kubectl apply -k kustomization/overlays/prod
```

## Разработчик

Туревич Максим
Email: miturevich@mai.education

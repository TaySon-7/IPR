# Лабораторная работа №7: Observability

Проект расширен метриками Prometheus, дашбордом Grafana и распределенным трейсингом через OpenTelemetry + Grafana Tempo.

## Что реализовано

- `/metrics` через `django-prometheus`.
- HTTP-метрики приложения:
  - `app_http_requests_total` (counter),
  - `app_http_request_duration_seconds` (histogram).
- Бизнес-метрика `app_health_checks_total`.
- Экспорт трейсов через OTLP (HTTP/gRPC), включается переменными окружения.
- Локальный observability stack через `docker-compose.observability.yml`:
  - Prometheus,
  - Grafana,
  - Tempo.
- K8s манифест `ServiceMonitor` для Prometheus Operator.

## Запуск локально (Docker Compose)

1) Подготовьте `.env` (минимум `SECRET_KEY`, `POSTGRES_*`).

2) Запустите приложение + observability:

```bash
docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d --build
```

3) Проверьте endpoints:

- API health: `http://localhost:8080/health/`
- Метрики: `http://localhost:8080/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (`admin/admin`)
- Tempo API: `http://localhost:3200`

4) Сгенерируйте нагрузку:

```bash
for i in {1..10}; do curl -s http://localhost:8080/health/ > /dev/null; done
```

После этого:
- в Prometheus (`Status -> Targets`) цель приложения должна быть `UP`,
- в Grafana в папке `Lab7` должен появиться дашборд `Lab7 Observability`,
- в Grafana Explore (datasource `Tempo`) должны быть trace'ы.

## Kubernetes (кратко)

1) Разверните БД (из `infra`), затем приложение (`k8s`).
2) Разверните стек наблюдаемости (Prometheus Operator / Tempo / Grafana) в namespace `observability`.
3) Примените `ServiceMonitor`:

```bash
kubectl apply -k k8s/kustomization/base
```

4) Проверьте, что в deployment backend заданы:

- `OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo.observability.svc.cluster.local:4318`
- `OTEL_SERVICE_NAME=django-backend`

## Структура observability-конфигов

- `observability/prometheus.yml` — scrape-конфигурация.
- `observability/tempo.yaml` — Tempo receiver/storage.
- `observability/grafana/datasources/datasources.yaml` — datasource provisioning.
- `observability/grafana/dashboards/` — dashboard provisioning + JSON дашборд.
- `k8s/kustomization/base/django-servicemonitor.yaml` — ServiceMonitor для Prometheus Operator.

## Скриншоты для отчета

Положите скриншоты в `docs/screenshots/lab7/`:

- `prometheus-targets.png` — Targets с `UP`.
- `grafana-dashboard.png` — дашборд метрик backend.
- `tempo-trace.png` — полный trace в Explore -> Tempo.
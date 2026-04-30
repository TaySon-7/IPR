import os

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

load_dotenv()

def setup_tracing():
    otlp_endpoint = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')
    if not otlp_endpoint:
        return

    service_name = os.environ.get('OTEL_SERVICE_NAME', 'django-app')

    resource = Resource(attributes={
        "service.name": service_name
    })

    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()
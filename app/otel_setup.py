# app/otel_setup.py
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from azure.monitor.opentelemetry import configure_azure_monitor


def configure_telemetry(service_name: str = "visa-api"):
    """
    Configura OpenTelemetry para enviar trazas a Grafana Cloud y/o Azure Application Insights.
    """

    # 🔹 Recurso base
    resource = Resource.create({
        SERVICE_NAME: service_name,
        "service.namespace": "visa-api-group",
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
    })

    # 🔹 Configura el proveedor de trazas
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # ✅ Exportador a Grafana Cloud (si existe token)
    grafana_token = os.getenv("GRAFANA_AUTH_TOKEN")
    if grafana_token:
        otlp_exporter = OTLPSpanExporter(
            endpoint="https://otlp-gateway-prod-us-east-2.grafana.net/otlp/v1/traces",
            headers={"Authorization": f"Basic {grafana_token}"},
        )
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # ✅ Exportador a Azure Application Insights (si existe variable de entorno)
    ai_conn_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if ai_conn_string:
        configure_azure_monitor(connection_string=ai_conn_string)

    # ✅ (Opcional) Exportador de consola
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    return trace.get_tracer(service_name)

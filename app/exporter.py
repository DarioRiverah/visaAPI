from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configuración directa de tus credenciales de Axiom
AXIOM_API_TOKEN = "xaat-4ed7a3ce-e0a8-441d-b8cf-0fc40e1249ab"
AXIOM_DATASET = "viseapi"

# Configurar el exportador OTLP hacia Axiom (región US)
otlp_exporter = OTLPSpanExporter(
    endpoint="https://api.axiom.co/v1/traces",  # dominio correcto de Axiom
    headers={
        "Authorization": f"Bearer {AXIOM_API_TOKEN}",
        "X-Axiom-Dataset": AXIOM_DATASET,
    },
)

# Definir el proveedor de trazas con el nombre del servicio
provider = TracerProvider(
    resource=Resource.create({
        "service.name": "vise-payments-api",
        "service.version": "1.0.0",
    })
)

# Enviar las trazas en lote al exportador
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Registrar el proveedor global de trazas
trace.set_tracer_provider(provider)

from fastapi import FastAPI, Request
from app.routers import clients, purchases  # 👈 Import absoluto, más seguro
from app.otel_setup import configure_telemetry
from opentelemetry import trace

# Configurar OpenTelemetry
configure_telemetry("visa-api")
tracer = trace.get_tracer("visa-api")

app = FastAPI(title="VISE Payments API", version="1.0.0")


# Middleware para registrar trazas de cada request
@app.middleware("http")
async def add_tracing(request: Request, call_next):
    with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
        # Agregar atributos útiles al span
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("client.host", request.client.host if request.client else "unknown")

        response = await call_next(request)

        span.set_attribute("http.status_code", response.status_code)
        return response


# Incluimos los routers
app.include_router(clients.router)
app.include_router(purchases.router)


# Endpoint simple para probar
@app.get("/ping")
async def ping():
    with tracer.start_as_current_span("ping-endpoint"):
        return {"message": "pong"}

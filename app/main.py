from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.exporter import provider
from app.routers import clients, purchases

app = FastAPI(
    title="VISE Payments API",
    version="1.0.0",
    description="API de pagos VISE con trazas enviadas a Axiom mediante OpenTelemetry"
)

app.include_router(clients.router)
app.include_router(purchases.router)

FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)

@app.get("/")
def root():
    return {"message": "✅ VISE Payments API funcionando correctamente con OpenTelemetry y Axiom"}

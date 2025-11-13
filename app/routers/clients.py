from fastapi import APIRouter
from fastapi.responses import JSONResponse
import itertools
from ..models import ClientIn
from ..rules import valid_for_card
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer(__name__)

_client_id_seq = itertools.count(1)
CLIENTS = {}

@router.post("/client")
def register_client(payload: ClientIn):
    with tracer.start_as_current_span("registro_cliente") as span:
        span.set_attribute("cliente.nombre", getattr(payload, "name", None))
        span.set_attribute("cliente.pais", payload.country)
        span.set_attribute("cliente.tipo_tarjeta", str(payload.cardType))
        span.set_attribute("cliente.ingreso_mensual", payload.monthlyIncome)
        span.set_attribute("cliente.viseClub", payload.viseClub)

        reason = valid_for_card(payload.cardType, payload.monthlyIncome, payload.viseClub, payload.country)
        if reason:
            span.set_attribute("cliente.estado", "rechazado")
            return JSONResponse(status_code=400, content={"status": "Rejected"})

        client_id = next(_client_id_seq)
        CLIENTS[client_id] = payload.model_dump()
        span.set_attribute("cliente.estado", "registrado")
        span.set_attribute("cliente.id", client_id)

        return {
            "status": "Registered",
            "cardType": payload.cardType.value,
            "clientId": client_id
        }
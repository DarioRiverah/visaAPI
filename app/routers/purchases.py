from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models import PurchaseIn, CardType
from ..routers.clients import CLIENTS
from ..rules import compute_discount, purchase_restriction
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer(__name__)

@router.post("/purchase")
def make_purchase(payload: PurchaseIn):
    with tracer.start_as_current_span("nueva_compra") as span:
        span.set_attribute("compra.id_cliente", payload.clientId)
        span.set_attribute("compra.pais_compra", payload.purchaseCountry)
        span.set_attribute("compra.monto", payload.amount)

        client = CLIENTS.get(payload.clientId)
        if not client:
            span.set_attribute("compra.estado", "rechazada_cliente_no_existe")
            return JSONResponse(status_code=404, content={"status": "Rejected"})

        card = CardType(client["cardType"])
        reason = purchase_restriction(card, payload.purchaseCountry)
        if reason:
            span.set_attribute("compra.estado", "rechazada_restriccion")
            return JSONResponse(status_code=400, content={"status": "Rejected"})

        discount, benefit_label = compute_discount(
            card=card,
            amount=payload.amount,
            purchase_dt=payload.purchaseDate,
            purchase_country=payload.purchaseCountry,
            client_country=client["country"],
        )

        final_amount = round(payload.amount - discount, 2)

        span.set_attribute("compra.estado", "aprobada")
        span.set_attribute("compra.descuento", discount)
        span.set_attribute("compra.total_final", final_amount)

        benefit_text = benefit_label or "0%"
        return {
            "status": "Approved",
            "purchase": {
                "discountApplied": discount,
                "finalAmount": final_amount,
                "benefit": benefit_text
            }
        }
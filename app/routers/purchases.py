from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models import PurchaseIn, CardType
from ..routers.clients import CLIENTS
from ..rules import compute_discount, purchase_restriction

router = APIRouter()

@router.post("/purchase")
def make_purchase(payload: PurchaseIn):
    client = CLIENTS.get(payload.clientId)
    if not client:
        return JSONResponse(status_code=404, content={"status": "Rejected"})

    card = CardType(client["cardType"])
    reason = purchase_restriction(card, payload.purchaseCountry)
    if reason:
        return JSONResponse(status_code=400, content={"status": "Rejected"})

    discount, benefit_label = compute_discount(
        card=card,
        amount=payload.amount,
        purchase_dt=payload.purchaseDate,
        purchase_country=payload.purchaseCountry,
        client_country=client["country"],
    )

    final_amount = round(payload.amount - discount, 2)

    # benefit solo necesita CONTENER el porcentaje; tus labels ya lo contienen ("... 15%")
    benefit_text = benefit_label or "0%"

    return {
        "status": "Approved",
        "purchase": {
            "discountApplied": discount,  # compute_discount ya redondea a 2
            "finalAmount": final_amount,
            "benefit": benefit_text
        }
    }

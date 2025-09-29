from fastapi import APIRouter
from fastapi.responses import JSONResponse
import itertools
from ..models import ClientIn  # ya no usamos ClientOut/ErrorOut aquí
from ..rules import valid_for_card

router = APIRouter()

_client_id_seq = itertools.count(1)
CLIENTS = {}

@router.post("/client")
def register_client(payload: ClientIn):
    reason = valid_for_card(payload.cardType, payload.monthlyIncome, payload.viseClub, payload.country)
    if reason:
        # Rechazo PLANO, sin "detail"
        return JSONResponse(status_code=400, content={"status": "Rejected"})

    client_id = next(_client_id_seq)
    # guardamos lo necesario para /purchase
    CLIENTS[client_id] = payload.model_dump()
    return {
        "status": "Registered",
        "cardType": payload.cardType.value,
        "clientId": client_id
    }

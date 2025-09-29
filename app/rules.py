from typing import Optional
from datetime import datetime
from .models import CardType

BANNED_COUNTRIES = {"China", "Vietnam", "India", "Irán", "Iran"}

def valid_for_card(card_type: CardType, income: float, club: bool, country: str) -> Optional[str]:
    if card_type == CardType.classic:
        return None
    if card_type == CardType.gold:
        if income < 500:
            return "El cliente no cumple con el ingreso mínimo de 500 USD para Gold"
    if card_type == CardType.platinum:
        if income < 1000:
            return "El cliente no cumple con el ingreso mínimo de 1000 USD para Platinum"
        if not club:
            return "El cliente no cumple con la suscripción VISE CLUB requerida para Platinum"
    if card_type in (CardType.black, CardType.white):
        if income < 2000:
            return f"El cliente no cumple con el ingreso mínimo de 2000 USD para {card_type.value}"
        if not club:
            return f"El cliente no cumple con la suscripción VISE CLUB requerida para {card_type.value}"
        if country in BANNED_COUNTRIES:
            return f"El cliente con tarjeta {card_type.value} no puede residir en {country}"
    return None

def compute_discount(card: CardType, amount: float, purchase_dt: datetime, purchase_country: str, client_country: str):
    weekday = purchase_dt.weekday()  # 0=lunes ... 6=domingo
    is_mon_to_wed = weekday in (0, 1, 2)
    is_mon_to_fri = weekday in (0, 1, 2, 3, 4)
    is_sat = weekday == 5
    is_sun = weekday == 6
    abroad = purchase_country != client_country

    candidates = []

    if card == CardType.gold:
        if is_mon_to_wed and amount > 100:
            candidates.append((0.15 * amount, "Lun-Mar-Mié >100 USD - Descuento 15%"))

    elif card == CardType.platinum:
        if is_mon_to_wed and amount > 100:
            candidates.append((0.20 * amount, "Lun-Mar-Mié >100 USD - Descuento 20%"))
        if is_sat and amount > 200:
            candidates.append((0.30 * amount, "Sábado >200 USD - Descuento 30%"))
        if abroad:
            candidates.append((0.05 * amount, "Exterior - Descuento 5%"))

    elif card == CardType.black:
        if is_mon_to_wed and amount > 100:
            candidates.append((0.25 * amount, "Lun-Mar-Mié >100 USD - Descuento 25%"))
        if is_sat and amount > 200:
            candidates.append((0.35 * amount, "Sábado >200 USD - Descuento 35%"))
        if abroad:
            candidates.append((0.05 * amount, "Exterior - Descuento 5%"))

    elif card == CardType.white:
        if is_mon_to_fri and amount > 100:
            candidates.append((0.25 * amount, "Lun-Vie >100 USD - Descuento 25%"))
        if (is_sat or is_sun) and amount > 200:
            candidates.append((0.35 * amount, "Sáb-Dom >200 USD - Descuento 35%"))
        if abroad:
            candidates.append((0.05 * amount, "Exterior - Descuento 5%"))

    if not candidates:
        return 0.0, None

    discount, label = max(candidates, key=lambda x: x[0])
    return round(discount, 2), label

def purchase_restriction(card: CardType, purchase_country: str) -> Optional[str]:
    if card in (CardType.black, CardType.white) and purchase_country in BANNED_COUNTRIES:
        return f"El cliente con tarjeta {card.value} no puede realizar compras desde {purchase_country}"
    return None

from decimal import Decimal, ROUND_HALF_UP

from rentsmart.domain.models import PropertyType, Quote, RentalRequest


class QuoteCalculator:
    def calculate(self, request: RentalRequest) -> Quote:
        base = {
            PropertyType.APARTMENT: Decimal("700.00"),
            PropertyType.HOUSE: Decimal("900.00"),
            PropertyType.STUDIO: Decimal("1200.00"),
        }[request.property_type]
        bedroom_charge = Decimal("0.00")
        if request.bedrooms == 2:
            bedroom_charge = {
                PropertyType.APARTMENT: Decimal("200.00"),
                PropertyType.HOUSE: Decimal("250.00"),
            }[request.property_type]
        parking_charge = Decimal("0.00")
        if request.parking_spaces:
            if request.property_type is PropertyType.STUDIO:
                parking_charge = Decimal("250.00") + Decimal("60.00") * (request.parking_spaces - 2)
            else:
                parking_charge = Decimal("300.00")
        subtotal = base + bedroom_charge + parking_charge
        discount = Decimal("0.00")
        if request.property_type is PropertyType.APARTMENT and not request.has_children:
            discount = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Quote(request, base, bedroom_charge, parking_charge, discount,
                     subtotal - discount, Decimal("2000.00"))

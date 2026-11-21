from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum


class PropertyType(Enum):
    APARTMENT = "apartamento"
    HOUSE = "casa"
    STUDIO = "estúdio"


@dataclass(frozen=True)
class RentalRequest:
    property_type: PropertyType
    bedrooms: int = 1
    parking_spaces: int = 0
    has_children: bool = True
    installments: int = 1

    def __post_init__(self):
        if not isinstance(self.property_type, PropertyType):
            raise ValueError("Tipo de imóvel inválido.")
        if type(self.bedrooms) is not int or self.bedrooms not in (1, 2):
            raise ValueError("Escolha um ou dois quartos.")
        if self.property_type is PropertyType.STUDIO and self.bedrooms != 1:
            raise ValueError("O estúdio não possui opção de dois quartos.")
        if type(self.parking_spaces) is not int or self.parking_spaces < 0:
            raise ValueError("A quantidade de vagas deve ser um inteiro não negativo.")
        if self.property_type is PropertyType.STUDIO:
            if self.parking_spaces == 1:
                raise ValueError("O pacote de estacionamento do estúdio começa com duas vagas.")
        elif self.parking_spaces > 1:
            raise ValueError("Casas e apartamentos permitem no máximo uma vaga.")
        if type(self.has_children) is not bool:
            raise ValueError("Informe se há crianças.")
        if type(self.installments) is not int or not 1 <= self.installments <= 5:
            raise ValueError("A taxa contratual pode ser dividida em uma a cinco parcelas.")


@dataclass(frozen=True)
class Quote:
    request: RentalRequest
    base_rent: Decimal
    bedroom_charge: Decimal
    parking_charge: Decimal
    discount: Decimal
    monthly_rent: Decimal
    contract_fee: Decimal

    def contract_payment(self, month: int) -> Decimal:
        if not 1 <= month <= self.request.installments:
            return Decimal("0.00")
        installment = (self.contract_fee / self.request.installments).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if month == self.request.installments:
            return self.contract_fee - installment * (self.request.installments - 1)
        return installment

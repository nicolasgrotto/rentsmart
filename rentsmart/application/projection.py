from dataclasses import dataclass
from decimal import Decimal

from rentsmart.domain.models import Quote


@dataclass(frozen=True)
class MonthlyPayment:
    month: int
    rent: Decimal
    contract_payment: Decimal

    @property
    def total(self) -> Decimal:
        return self.rent + self.contract_payment


class ProjectionService:
    def create(self, quote: Quote) -> list[MonthlyPayment]:
        return [MonthlyPayment(month, quote.monthly_rent, quote.contract_payment(month))
                for month in range(1, 13)]

import csv
from pathlib import Path

from rentsmart.application.projection import MonthlyPayment


class CsvProjectionWriter:
    def write(self, payments: list[MonthlyPayment], path: Path) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["mes", "aluguel", "parcela_contrato", "total"])
            for payment in payments:
                writer.writerow([payment.month, self._format(payment.rent),
                                 self._format(payment.contract_payment), self._format(payment.total)])

    @staticmethod
    def _format(value):
        return f"{value:.2f}".replace(".", ",")

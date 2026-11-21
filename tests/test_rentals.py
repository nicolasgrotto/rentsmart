import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from rentsmart.application.projection import ProjectionService
from rentsmart.domain.calculator import QuoteCalculator
from rentsmart.domain.models import PropertyType, RentalRequest
from rentsmart.infrastructure.csv_writer import CsvProjectionWriter


class RentalTests(unittest.TestCase):
    def setUp(self):
        self.calculator = QuoteCalculator()

    def test_apartment_discount_after_additions(self):
        quote = self.calculator.calculate(RentalRequest(PropertyType.APARTMENT, 2, 1, False, 3))
        self.assertEqual(quote.discount, Decimal("60.00"))
        self.assertEqual(quote.monthly_rent, Decimal("1140.00"))

    def test_house_and_studio_prices(self):
        house = self.calculator.calculate(RentalRequest(PropertyType.HOUSE, 2, 1))
        studio = self.calculator.calculate(RentalRequest(PropertyType.STUDIO, parking_spaces=4))
        self.assertEqual(house.monthly_rent, Decimal("1450.00"))
        self.assertEqual(studio.monthly_rent, Decimal("1570.00"))
        self.assertEqual(self.calculator.calculate(RentalRequest(PropertyType.STUDIO)).monthly_rent,
                         Decimal("1200.00"))

    def test_invalid_requests(self):
        cases = [dict(bedrooms=3), dict(parking_spaces=2), dict(installments=0),
                 dict(installments=6), dict(has_children=1)]
        for values in cases:
            with self.subTest(values=values), self.assertRaises(ValueError):
                RentalRequest(PropertyType.HOUSE, **values)
        for values in (dict(parking_spaces=1), dict(bedrooms=2)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                RentalRequest(PropertyType.STUDIO, **values)

    def test_projection_and_csv(self):
        quote = self.calculator.calculate(RentalRequest(PropertyType.APARTMENT, installments=3))
        payments = ProjectionService().create(quote)
        self.assertEqual(len(payments), 12)
        self.assertEqual([p.contract_payment for p in payments[:4]],
                         list(map(Decimal, ["666.67", "666.67", "666.66", "0.00"])))
        self.assertEqual(sum(p.contract_payment for p in payments), Decimal("2000.00"))
        self.assertEqual(sum(p.total for p in payments), Decimal("10400.00"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projection.csv"
            CsvProjectionWriter().write(payments, path)
            with path.open(encoding="utf-8-sig", newline="") as file:
                rows = list(csv.reader(file, delimiter=";"))
            self.assertEqual(len(rows), 13)
            self.assertEqual(rows[1], ["1", "700,00", "666,67", "1366,67"])
            self.assertEqual(rows[-1], ["12", "700,00", "0,00", "700,00"])


if __name__ == "__main__":
    unittest.main()

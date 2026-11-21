from pathlib import Path

from rentsmart.application.projection import ProjectionService
from rentsmart.domain.calculator import QuoteCalculator
from rentsmart.domain.models import PropertyType, RentalRequest
from rentsmart.infrastructure.csv_writer import CsvProjectionWriter


def ask_integer(prompt, valid, error):
    while True:
        try:
            value = int(input(prompt).strip())
            if valid(value):
                return value
        except ValueError:
            pass
        print(error)


def money(value):
    return "R$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def run():
    print("RentSmart — Orçamento de locação")
    print("1 - Apartamento | 2 - Casa | 3 - Estúdio")
    choice = ask_integer("Tipo de imóvel: ", lambda n: n in (1, 2, 3), "Escolha 1, 2 ou 3.")
    property_type = {1: PropertyType.APARTMENT, 2: PropertyType.HOUSE, 3: PropertyType.STUDIO}[choice]
    bedrooms = 1
    if property_type is not PropertyType.STUDIO:
        bedrooms = ask_integer("Quartos (1 ou 2): ", lambda n: n in (1, 2), "Escolha 1 ou 2.")
        parking = ask_integer("Vaga de garagem (0 ou 1): ", lambda n: n in (0, 1), "Escolha 0 ou 1.")
    else:
        parking = ask_integer("Vagas (0 ou pelo menos 2): ", lambda n: n == 0 or n >= 2,
                              "Escolha 0 ou um número inteiro a partir de 2.")
    has_children = True
    if property_type is PropertyType.APARTMENT:
        children = ask_integer("Possui crianças? (1 - Sim, 2 - Não): ", lambda n: n in (1, 2),
                               "Escolha 1 ou 2.")
        has_children = children == 1
    installments = ask_integer("Parcelas da taxa contratual (1 a 5): ", lambda n: 1 <= n <= 5,
                               "Escolha entre 1 e 5 parcelas.")
    request = RentalRequest(property_type, bedrooms, parking, has_children, installments)
    quote = QuoteCalculator().calculate(request)
    payments = ProjectionService().create(quote)
    print("\nResumo do orçamento")
    print(f"Imóvel: {property_type.value.capitalize()}")
    if property_type is not PropertyType.STUDIO:
        print(f"Quartos: {bedrooms}")
    print(f"Vagas: {parking}")
    if property_type is PropertyType.APARTMENT:
        print(f"Possui crianças: {'Sim' if has_children else 'Não'}")
    print(f"Aluguel-base: {money(quote.base_rent)}")
    print(f"Adicional de quarto: {money(quote.bedroom_charge)}")
    print(f"Adicional de garagem: {money(quote.parking_charge)}")
    print(f"Desconto: - {money(quote.discount)}")
    print(f"Aluguel mensal: {money(quote.monthly_rent)}")
    print(f"Taxa contratual: {money(quote.contract_fee)} em {installments} parcela(s)")
    for payment in payments[:installments]:
        print(f"  Parcela do mês {payment.month}: {money(payment.contract_payment)}")
    path = Path("projecao_locacao.csv")
    CsvProjectionWriter().write(payments, path)
    print(f"Projeção de 12 meses salva em: {path.resolve()}")


def main():
    try:
        run()
    except (EOFError, KeyboardInterrupt):
        print("\nOperação cancelada.")
    except OSError as error:
        print(f"Não foi possível salvar a projeção: {error}")
        raise SystemExit(1)

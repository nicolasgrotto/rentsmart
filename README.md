# RentSmart

Aplicação de linha de comando para calcular orçamentos de locação e projetar os pagamentos do primeiro ano. A análise teórica e o fluxograma estão em [docs/analise.pdf](docs/analise.pdf); a versão editável está em [docs/analise.html](docs/analise.html).

## Execução

É necessário Python 3.10 ou superior. Não há dependências externas. Na pasta do projeto, execute:

```console
python main.py
```

Responda às perguntas pelo número indicado. O programa valida as entradas, apresenta a composição do orçamento e grava `projecao_locacao.csv` no diretório atual, substituindo um arquivo existente com esse nome. Para cancelar, pressione Ctrl+C.

O CSV usa UTF-8 com BOM, ponto e vírgula como separador de campos e vírgula decimal. Cada linha apresenta mês, aluguel, parcela contratual e total. O aluguel não inclui a taxa contratual; o total mensal soma ambos.

Para executar os testes:

```console
python -m unittest discover -s tests -v
```

## Regras e premissas

- Apartamento: R$ 700,00; casa: R$ 900,00; estúdio: R$ 1.200,00.
- O segundo quarto acrescenta R$ 200,00 ao apartamento ou R$ 250,00 à casa. Uma vaga acrescenta R$ 300,00 a esses imóveis.
- No estúdio, o estacionamento é opcional. Quando escolhido, começa com o pacote de duas vagas por R$ 250,00, mais R$ 60,00 por vaga adicional. Uma vaga isolada não é oferecida.
- Para apartamento sem crianças, o desconto de 5% incide sobre o aluguel-base e os adicionais.
- A taxa contratual de R$ 2.000,00 é paga nos primeiros meses em uma a cinco parcelas. O arredondamento é feito em centavos e eventual diferença é ajustada na última parcela.
- Não há reajustes ou outros custos no período projetado. O enunciado não define quantidade de quartos para o estúdio; a interface não solicita essa informação.

## Organização

`domain` contém as entidades, validações e regras de preços; `application` monta a projeção; `infrastructure` grava o CSV; `presentation` cuida da interação. `main.py` inicia a aplicação e `tests` verifica os principais cenários.

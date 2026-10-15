# ClearBank — Análise Financeira com Python

Desafio final do módulo de Python para Análise de Dados. O notebook lê o histórico de
transações da fintech fictícia **ClearBank** (`transacoes.csv`), valida e limpa os dados,
calcula métricas financeiras mensais, sinaliza transações suspeitas (acima de R$ 10.000,00),
exibe um relatório formatado e exporta o resultado em `relatorio.json`.

## Estrutura

```
analise-de-dados-python/
├── desafio-final.ipynb   # notebook principal, com as saídas salvas
├── transacoes.csv        # dados de teste (17 válidas, 9 inválidas, 3 suspeitas)
├── relatorio.json        # relatório gerado pelo notebook
├── analise_pandas.py     # (opcional) versão com pandas + comparação com a solução nativa
├── grafico.png           # (opcional) crédito, débito e saldo por mês
└── README.md
```

## Como executar

**Google Colab**
1. Abra o `desafio-final.ipynb` no Colab (*File → Upload notebook*).
2. Envie também o `analise_pandas.py` (painel *Files*) para rodar a seção opcional de pandas.
   O `transacoes.csv` é criado automaticamente pelo notebook se não for enviado.
3. *Runtime → Run all*.

## O que o notebook faz

| Etapa | Função(ões) |
|---|---|
| Leitura com `csv.DictReader` (trata `FileNotFoundError`) | `ler_transacoes()` |
| Validação de id, cliente, data, tipo e valor; descarte de duplicados | `validar_id()`, `converter_valor()`, `converter_data()`, `validar_transacao()`, `limpar_transacoes()` |
| Período analisado e dias entre a primeira e a última transação | `calcular_periodo()` |
| Métricas mensais e transações suspeitas | `agrupar_por_mes()`, `calcular_metricas_mes()`, `identificar_suspeitas()`, `gerar_relatorio()` |
| Exportação JSON | `salvar_json()` |
| Relatório no terminal | `formatar_moeda()`, `exibir_relatorio()` |

## Saídas geradas

- **Terminal:** resumo da limpeza, período analisado, totais de válidas/inválidas, métricas por mês
  (quantidade, crédito, débito, saldo, média, maior e menor valor) e lista de transações suspeitas.
- **`relatorio.json`:** data de geração, totais, período, `resumo_mensal` e `transacoes_suspeitas`.
- **`grafico.png`** (opcional): barras de crédito e débito por mês com a linha do saldo.
- **pandas** (opcional): a mesma análise com `read_csv` + `groupby`, conferida contra o `relatorio.json`.

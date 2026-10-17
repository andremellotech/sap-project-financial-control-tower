# Contribuir e reutilizar

1. Leia o [contrato](docs/data-contract.md) e os [indicadores](docs/metrics.md).
2. Use Python 3.11+ e Node.js para os testes. Não são necessárias bibliotecas externas para gerar o relatório.
3. Para uma nova regra, acrescente um caso financeiro independente que falhe antes da alteração e passe depois. Compare os totais SQL e JavaScript; mudanças de sinal, corte, granularidade ou caixa precisam de exemplos explícitos.
4. Execute `python -m unittest discover -s tests`, `python -m finance demo`, `node --check web/app.js`, `node --check web/metrics.js` e `node tests/test_metrics.cjs`.
5. Se mudar a interface, confira todas as perspectivas, fichas, filtros vazios e larguras de 320/390 px. Tabelas podem rolar no próprio contêiner; a página não deve transbordar.
6. Mantenha exemplos fictícios e documentação coerente com o que foi implementado. Não inclua credenciais, extrações corporativas, capturas de SAP real ou dados de pagamentos reais.

Um adaptador de layout futuro deve transformar uma cópia do extrato no contrato, com mapeamento explícito e testes. Não adicione um botão de conexão SAP se ele não existir nem transforme valores CJIA em custos. Mudanças de critério de EAC/compromisso devem preservar a separação entre caixa e custo.

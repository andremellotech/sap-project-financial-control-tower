# Cenários fictícios do portfólio

Corte único: **30/09/2026**, BRL, baseline **BL-01** e forecast **FC-09**. Quatro projetos, **22 PEPs folha**, 33 nós incluindo pais e **700 linhas financeiras**. Todos os nomes, documentos, valores e vínculos são fictícios.

| Projeto | Tema | PEPs folha | Baseline | Realizado | Projetado restante | EAC | Desvio EAC − baseline |
|---|---|---:|---:|---:|---:|---:|---:|
| AURORA | Implantação industrial | 4 | 1.000.000 | 480.000 | 570.000 | 1.050.000 | +50.000 |
| HORIZONTE | Centro logístico | 6 | 2.400.000 | 850.000 | 1.470.000 | 2.320.000 | −80.000 |
| ATLAS | Eficiência energética | 6 | 1.600.000 | 1.130.000 | 690.000 | 1.820.000 | +220.000 |
| VERTICE | Modernização digital | 6 | 800.000 | 690.000 | 70.000 | 760.000 | −40.000 |
| **Portfólio** | **Valores em R$** | **22** | **5.800.000** | **3.150.000** | **2.800.000** | **5.950.000** | **+150.000** |

Projetado restante = residual CJI5 + ETC adicional. O portfólio contém residual de R$ 1.620.000 e ETC de R$ 1.180.000. A baseline até o corte é R$ 4.710.000. Não some subtotais dos pais aos valores das folhas.

## Como explorar

1. No resumo, compare os quatro cards. Clique em um projeto para aplicar o filtro global; o seletor de PEP passa a mostrar somente os elementos compatíveis.
2. Horizonte tem maior parcela de custo ainda a incorrer. Atlas concentra o maior desvio desfavorável. Vértice tem menor saldo restante, mas isso não comprova conclusão física.
3. Em Elementos PEP, abra `PRJ-03.01.02` (geração e equipamentos): baseline R$ 550 mil, realizado R$ 430 mil, compromisso R$ 140 mil, ETC R$ 130 mil e EAC R$ 700 mil.
4. Na aba Projeção, agrupe por **Projetos** para comparar os quatro projetos com o total ao final. Selecione Vértice no filtro e agrupe por **Elementos PEP**: são seis colunas e um total de R$ 690 mil já realizados + R$ 70 mil restantes. No PEP `PRJ-04.01.01`, não resta projeção de custo informada.
5. Em Aderência, investigue as diferenças de Real em V01, V2_2 e V3_2 e a diferença de Compromisso em V3_3. V2_5 e V3_5 estão declarados não comparáveis; diferenças não são calculadas. V4_5 conserva os campos opcionais de orçamento, Plan.re. e Disposto ausentes.
6. Limpar filtros retorna ao portfólio. O ranking inicial mostra até oito PEPs por desvio de EAC menos baseline; o botão abaixo abre a matriz completa.

As versões e a aprovação de baseline foram mantidas comuns aos quatro casos para simplificar a demonstração. Na adaptação, o manifesto representa um único corte e versões compatíveis; não misture versões ou snapshots sem tratamento próprio.

## Controles da base

- 232 linhas de baseline, 172 da CJI3, 56 da CJI5, 183 da CJIA e 57 de ETC: **700 fatos financeiros**.
- 166 alocações explícitas e 22 referências externas são tabelas de controle, não novos fatos somados ao EAC.
- Custo e caixa continuam separados. Pagamentos: R$ 2.491.900; alocação explícita: R$ 2.451.900. Valores sem alocação não são contas a pagar calculadas.
- Créditos em Horizonte e Atlas preservam o custo líquido. Nenhum pagamento é conciliado apenas por ter o mesmo pedido.
- R$ 255 mil de compromissos têm previsão anterior ao corte. Não foi criada reprogramação automática.
- Referências ZOVRPS005 e S_ALR_87013558 são exemplos normalizados preparados para o caso. Nenhum SAP foi consultado; não se presume fórmula de Plan.re. ou Disposto.

Veja [como usar](user-guide.md), [indicadores](metrics.md) e [contrato dos CSVs](data-contract.md).

# Da extração SAP GUI à análise por PEP

A [SAP documenta os relatórios de partidas individuais de projetos](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/69c3a05bb8d44f02bdd2abe5e822da8e/ae05b753128eb44ce10000000a174cb4.html): CJI3 para custos/receitas realizados, CJI5 para compromissos, CJI4 para custos/receitas planejados e CJIA para pagamentos realizados/compromissos de pagamento. Este projeto trabalha com o perímetro de custos e saídas, não com receitas.

| Transação | Conferência sugerida | Preparação necessária |
|---|---|---|
| CJI3 | PEP, empresa, exercício, documento/item, classe, data e valor com sinal | Classificar custo operacional e liquidação; preservar créditos/estornos e eliminar subtotais |
| CJI5 | PEP, RC/PC, item, alocação, residual e previsão | Um snapshot no corte, saldos já reduzidos, parcelas já distribuídas por PEP |
| CJIA | Natureza de pagamento/compromisso, documento, data, base monetária e referências | Separar caixa realizado e comprometido e preparar vínculos de conciliação apenas quando comprovados |
| CJI4 | Versão e horizonte do planejamento disponível | Confrontar com o plano aprovado; não assumir que cada item representa a baseline vigente |

Os nomes das colunas são os do [contrato normalizado](data-contract.md). Não há mapeamento automático de cabeçalhos SAP. Layouts, disponibilidade, critérios, uso de versões e autorizações variam por ambiente; valide com o responsável pelas extrações.

## Preparar uma execução compatível

1. Defina projetos/PEPs, moeda/base de valor, calendário, data de corte e natureza operacional que pretende controlar.
2. Exporte as bases por recursos autorizados do SAP GUI e preserve os originais e critérios. O relatório não automatiza a sessão nem muda parâmetros do sistema.
3. Remova linhas de total/subtotal da carga de fatos. Mantenha a hierarquia no cadastro PEP, com os lançamentos alocados nas folhas.
4. Na CJI3, preserve sinais e referências. Defina como tratar liquidação, capitalização, transferências, impostos e receitas conforme o perímetro. A política do exemplo não é universal.
5. Na CJI5, obtenha a posição residual de custo para a data declarada. Não misture posições históricas nem reduza de novo pelo realizado. A SAP descreve [compromissos de projeto e suas origens em compras](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/4dd8cb7b1c484b4b93af84d00f60fdb8/fa7bd0531d8b4208e10000000a174cb4.html); a interpretação e as reduções precisam ser conferidas no ambiente.
6. Na CJIA, identifique as naturezas efetivas do layout. Um compromisso de pagamento não é pagamento realizado nem compromisso de custo CJI5. Conservação de sinais e da base monetária é essencial.
7. Congele a baseline aprovada por PEP/mês/classe. A SAP explica que [itens de planejamento dependem de configuração e podem documentar alterações a partir da ativação](https://help.sap.com/docs/SAP_ERP_SPV/5ecdd9085d344e6693e65fc60c3b5b0f/5cf2d353ca9f4408e10000000a174cb4.html). Não some movimentos sem entender se representam posição ou mudança.
8. Prepare ETC adicional e vínculos custo/pagamento documentados, execute o build e confronte amostras e totais com a origem.

## Investigar no relatório

Em Elementos PEP, abra a ficha, selecione um documento e clique no roteiro CJI3/CJI5/CJIA. O quadro didático conserva PEP/documento/item. Ele não é uma captura SAP, não abre transações nem comprova que o extrato foi homologado em um ambiente real. Não há dados de credenciais ou conexão no repositório.

O número do pedido ajuda a localizar uma compra, mas não é uma chave suficiente para conciliar custo e caixa: um pedido pode ter vários itens, PEPs, documentos e parcelas. O arquivo de conciliação explicita os pares e seus valores.

## Aderência — ZOVRPS005 e S_ALR_87013558

No ZOVRPS005 do ambiente do usuário foram informados os campos **Orçamento, Real, Compromisso, Plan.re. e Disposto**. O projeto conserva os valores preparados no arquivo de referência; não conhece o código Z nem presume o cálculo de Plan.re./Disposto. O exemplo é fictício e não representa extração real.

O [catálogo SAP de relatórios PS](https://help.sap.com/docs/SUPPORT_CONTENT/prosys/3363505772.html) inclui S_ALR_87013558 como relatório hierárquico com orçamento/real/compromisso/plano remanescente/atribuído. Rótulos e alcance devem ser conferidos na versão/layout utilizada. Antes de comparar, iguale projeto/PEP, objetos subordinados, classe de custo, moeda, horizonte e corte. Não compare uma posição anual com custos de todo o projeto nem totais com subtotais replicados.

Em **Aderência**, a ficha da referência mostra os cinco campos externos, baseline e EAC calculados. Coincidência de Real/Compromisso é uma conferência numérica do recorte declarado, não homologação SAP ou autorização financeira. Para utilizar S_ALR em vez do exemplo Z, prepare o mesmo contrato com a fonte correta e campos ausentes vazios. Não some relatórios alternativos como novos custos.

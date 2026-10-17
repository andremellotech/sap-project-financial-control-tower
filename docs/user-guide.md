# Como usar

## Explorar sem instalar

1. Extraia o ZIP completo. Abra `index.html` na raiz ou acesse a demonstração publicada no Pages.
2. Na visão executiva, compare os quatro projetos: baseline consolidada R$ 5,8 milhões, realizado R$ 3,15 milhões e EAC R$ 5,95 milhões. Os cards abrem o projeto; a matriz reúne 22 PEPs folha. Compare baseline total, custo realizado, residual CJI5 e EAC. O gráfico de curva compara somente o ano civil do corte; os indicadores incluem todo o horizonte informado.
3. Para seguir os exemplos abaixo, selecione **AURORA** no filtro Projeto. Filtre subárvore PEP e classe de custo. O filtro se aplica a todas as perspectivas e fichas. Seleções incompatíveis mostram zeros; Limpar restaura tudo.
4. Em **Elementos PEP**, clique em `PRJ-01.01.01`. Confira baseline R$ 200 mil, realizado R$ 100 mil e EAC R$ 220 mil. Pais são subtotais: não some as linhas da hierarquia.
5. Na ficha, clique em `5100001002`. Esse custo é de R$ 40 mil, com R$ 20 mil explicitamente conciliados ao pagamento `2000001001`. Os R$ 20 mil restantes são custo sem alocação demonstrada, não contas a pagar calculadas.
6. Clique **Conferir no roteiro CJI3**. O guia preserva PEP, documento e item no quadro didático. Não abre uma conexão SAP. Ao trocar de roteiro manualmente, o contexto do documento é limpo.
7. Em **Realizado**, pesquise `5100001004`: o crédito de R$ 20 mil tem sinal negativo. A liquidação `5100001008` permanece visível e fora da soma de custos.
8. Em **Compromissos**, confira o saldo e a previsão de cada RC/PC; não se trata do valor original dos documentos.
9. Em **Caixa**, veja pagamentos R$ 360 mil, compromissos de caixa R$ 200 mil e alocação comprovada R$ 320 mil. Essas grandezas não são somadas ao custo.
10. Em **Projeção e build-up**, escolha **Elementos PEP**: cada PEP tem uma coluna de realizado e projetado restante. Com AURORA selecionado, são quatro colunas e o **Total do recorte** ao final: realizado de R$ 480 mil + restante de R$ 570 mil = EAC de R$ 1,05 milhão. Escolha **Projetos** para agrupar os PEPs. Com Limpar filtros, compare os quatro projetos ou todos os 22 PEPs; a região tem rolagem horizontal e o total fica à direita. A linha tracejada de cada coluna representa a sua baseline. Simule +10% de ETC: o EAC simulado é R$ 1.078.000,00. A simulação fica separada do gráfico publicado; os documentos e a baseline permanecem preservados.
11. Em **SAP e origens**, expanda a identificação da execução e confira hashes e downloads completos. O CSV de seleção em Realizado/Compromissos respeita também a busca local; a busca não altera os indicadores globais.

## Processar cópias das suas extrações

O projetado restante é o saldo residual CJI5 mais o ETC adicional. Em cada novo corte, atualize essas bases para que a execução já realizada deixe de constar na projeção restante. Não subtraia o realizado novamente do residual CJI5: o saldo já deve considerar as reduções. Se o EAC for mantido, cada aumento do realizado terá redução equivalente do restante. Mudanças de premissa podem alterar o EAC. O painel mostra um snapshot por execução, sem inventar evolução entre cortes.

1. Instale Python 3.11 ou posterior. Não há dependências externas para a geração.
2. Copie `sample-input` para `local-input` como estrutura de trabalho e substitua integralmente o exemplo por bases preparadas conforme o [contrato](data-contract.md). Não misture demonstração e extratos reais.
3. Copie `config/manifest.json` para `local-config/manifest.json`. Defina corte (último dia do mês), versões, data de aprovação, escopo e `dados_ficticios: false`.
4. Mantenha um único snapshot de compromissos no corte. Na CJIA, separe pagamento e compromisso de pagamento. A classificação dos CSVs precisa ser validada contra a origem SAP.
5. Conserve a baseline aprovada e sua evidência. Mudança de plano é nova versão com aprovação própria; não substitua o arquivo aprovado para eliminar desvios.
6. Defina ETC somente para custos futuros ainda não cobertos pelo residual CJI5. Registre premissa e responsável.
7. Preencha a conciliação apenas com vínculos demonstrados. Caso não disponha deles, deixe `conciliacoes.csv` apenas com o cabeçalho; não invente correspondências pelo número do pedido.
8. Na raiz do projeto, execute:

```bash
python -m finance build --input local-input --manifest local-config/manifest.json --output local-output/corte-2026-09
```

9. Abra o HTML da saída. Confira amostras de PEP/documentos e os totais contra as extrações. Retorno 0 significa geração concluída; não aprovação financeira. Retorno 1 indica validação/leitura/saída recusada; 2 indica erro de sintaxe dos argumentos.
10. Para outra execução, escolha uma pasta nova. Os originais não são modificados.

O HTML contém os dados e funciona sem CDN ou requisições de rede. Os downloads locais dependem de manter os arquivos gerados ao lado do HTML. `demo` sobrescreve somente os artefatos conhecidos da demonstração e o `index.html` raiz; não use para dados de trabalho.

## Se algo não funcionar

| Mensagem / sintoma | Como conferir |
|---|---|
| Cabeçalhos esperados | Renomeie/mapeie explicitamente as colunas do extrato para o contrato; um CSV bruto SAP não tem um layout único |
| Valor inválido | Remova separador de milhar e use ponto decimal: `1234.56`, preservando sinal |
| PEP folha | Separe subtotais do extrato; carregue valores nas folhas e cadastre pais sem fatos financeiros |
| Snapshot diferente do corte | Prepare uma posição compatível com a data declarada, sem somar extrações de dias diferentes |
| Sobre-alocação | Reveja o rateio custo/pagamento e sua base monetária; não force coincidência entre custo e caixa |
| Saída já existe | Escolha uma pasta nova para conservar a execução anterior |
| Página sem interação | Habilite JavaScript para este arquivo/site conforme as regras do ambiente; o JSON, CSV e SQLite continuam disponíveis para análise local |

Esta versão não exige usuário, senha ou parâmetros de conexão SAP.

## Conferir aderência

Selecione **AURORA** e abra **Aderência**. O exemplo mostra EAC/baseline de 105%, desvio de +R$ 50 mil, realizado/plano até corte de 64% e custo a incorrer de R$ 570 mil. Esses índices têm denominadores distintos e não são avanço físico.

Na tabela de referências, clique em **ZOVRPS005 · V01**: Orçamento 210 mil, Real 95 mil, Compromisso 40 mil, Plan.re. 75 mil e Disposto 210 mil são valores fictícios preparados como referência. O modelo detalhado tem realizado 100 mil, diferença +5 mil para investigar, EAC 220 mil e baseline 200 mil. Não foi feita consulta a um SAP real.

Para conferir seus totais, prepare `conferencia_sap.csv`. Declare SIM somente se a referência for comparável; caso contrário, use NAO. Se não houver totais, deixe somente cabeçalho. A grade mensal é expansível e separa compromissos até o corte sem reprogramação. O [contrato](data-contract.md) explica o tratamento dos campos externos.

## Explorar o portfólio completo

Use Limpar filtros para voltar aos quatro projetos. Veja [cenários, PEPs e números de conferência](demo-scenarios.md). No consolidado, ETC +10% resulta em EAC simulado de R$ 6.068.000,00.

## Leitura executiva da projeção

Acima do gráfico, confira o recorte aplicado e o resumo de **desvio no fechamento**, **projetado restante** e **parcela realizada do EAC**. Esta última é custo realizado dividido pelo EAC, quando o denominador é positivo e o realizado não é negativo; não mede avanço físico. Cada coluna mostra nome, composição e desvio de EAC menos baseline. O total consolidado permanece à direita.

Abra **Critérios de leitura e valores com crédito** para ver os cuidados de interpretação. A seção **Premissas do ETC adicional** fica recolhida ao final; clique na seta para conferir a tabela completa, premissas e responsáveis. A sensibilidade continua separada do gráfico publicado.

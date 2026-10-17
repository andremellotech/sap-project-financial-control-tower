# Indicadores e conciliações

Todos os valores são inteiros em centavos; não há câmbio. A análise usa as folhas da hierarquia, sem juntar custo e caixa por pedido ou documento. Os filtros de projeto, subárvore e classe atingem os fatos; os vínculos conciliados só contam se ambos os lados estiverem no recorte.

| Indicador | Regra |
|---|---|
| Baseline total | Soma do plano aprovado da versão selecionada, horizonte completo informado |
| Baseline até corte | Linhas de baseline com mês ≤ mês do corte, inclusive anos anteriores |
| Realizado | CJI3 com natureza CUSTO, valores assinados, data ≤ corte |
| Liquidações | CJI3 LIQUIDACAO, visível separadamente e fora de realizado/EAC neste perímetro |
| Compromisso de custo | CJI5 residual RC + PC, snapshot igual ao corte |
| ETC adicional | Estimativa gerencial futura não coberta pela CJI5 |
| EAC | Realizado + compromisso de custo + ETC adicional |
| Desvio final | EAC − baseline total; positivo indica projeção acima do plano |
| Desvio até corte | Realizado − baseline até corte; negativo não comprova economia |
| Compromisso com previsão vencida | Saldo CJI5 com data prevista anterior ao corte; corte do próprio dia não é vencido |
| Pagamentos | CJIA PAGAMENTO líquido, fora do custo/EAC |
| Compromisso de caixa | CJIA COMPROMISSO_PAGAMENTO, fora do custo/EAC |
| Conciliado | Soma assinada de alocações explícitas custo ↔ pagamento |
| Custo/pagamento sem alocação | Total líquido correspondente − alocação líquida; não é contas a pagar |

O EAC é uma metodologia gerencial deste projeto, não reprodução de um cálculo padrão SAP. Se o forecast recebido já for um EAC completo ou um ETC total incluindo compromissos, não o carregue diretamente no campo ETC adicional.

### Leitura da coluna de build-up

Na aba Projeção, escolha **Elementos PEP** ou **Projetos** em Agrupar colunas por. Cada coluna usa o mesmo recorte dos filtros globais. Somente folhas entram na composição; o último **Total do recorte** resume os itens anteriores e não é um novo valor a adicionar. Todas as colunas têm a mesma escala e uma marca tracejada da sua própria baseline. Com muitos PEPs, role a região horizontalmente; o total permanece à direita. Clique em uma coluna de projeto para detalhar os PEPs, em um PEP para ver a ficha ou no total para abrir a matriz. A simulação de ETC continua separada do forecast publicado.

Realizado e projetado restante ocupam a mesma coluna. A parte verde representa CJI3; a parte azul clara, residual CJI5 + ETC adicional. O topo é o EAC; a linha tracejada é a baseline independente. Exemplo: R$ 480 mil + R$ 570 mil = R$ 1,05 milhão. Com EAC constante, R$ 100 mil adicionais de execução deixam R$ 580 mil realizados e R$ 470 mil restantes. Isso exige bases do novo corte atualizadas; não é uma baixa automática nem uma segunda dedução do realizado sobre a CJI5. Revisões de forecast podem mudar o total. Valores líquidos negativos conservam o sinal; nessa situação a faixa âmbar sobre o projetado representa o crédito que reduz o EAC.

## Exemplos

Os exemplos numéricos desta seção usam o filtro **AURORA**, preservado na ampliação do portfólio. Os quatro projetos e os totais consolidados estão em [cenários da demonstração](demo-scenarios.md).

- Engenharia: baseline 200 mil; custo 100 mil; residual CJI5 40 mil; ETC adicional 80 mil. EAC 220 mil, desvio +20 mil. Pagamento 80 mil permanece separado.
- Equipamentos: 270 mil de custo e crédito de −20 mil dão realizado líquido 250 mil. Liquidação de 100 mil permanece visível e não duplica o custo. CJI5 150 mil e ETC 70 mil levam a EAC 470 mil.
- Pagamento P01 de 80 mil: 60 mil alocados a A01 e 20 mil a A02. A02 vale 40 mil, restando 20 mil de custo sem alocação demonstrada.
- Automação: pagamento P04 de 40 mil não tem vínculo explícito. Não o tratamos como pagamento do custo A07 de 30 mil apenas por ter o mesmo PEP/pedido.
- ETC global +10% na simulação: 480 mil + 290 mil + 308 mil = EAC simulado 1,078 milhão. Baseline e dados publicados não mudam.

## Tempo e escopo

A curva mostra baseline e custo acumulados somente no ano civil do corte; realizado para no corte. Os indicadores totais podem incluir anos anteriores/futuros conforme o contrato. Compromissos vencidos ficam separados no build-up sem distribuição automática no futuro. Não há projeção mensal de caixa, curva física, CPI/SPI, saldo orçamentário SAP ou reconstrução histórica por estorno retroativo. O corte dos custos usa data de lançamento; o extrato precisa representar o perímetro apropriado ao corte.

Veja o [contrato](data-contract.md) antes de comparar extratos com períodos, moedas, naturezas ou granularidades diferentes.

## Aderência e conferência externa

Percentuais e valores exemplificados abaixo referem-se a **AURORA**. O consolidado é recalculado com todos os projetos selecionados.

- **EAC / baseline:** projeção final relativa ao plano aprovado. No exemplo, 105% = desvio de +5%, não um score genérico de aderência de 95%.
- **Realizado / baseline até corte:** 64% no exemplo. Mede comparação financeira com plano, não avanço físico ou economia.
- **Baseline − realizado:** espaço matemático remanescente do plano (520 mil no exemplo), não disponibilidade de orçamento SAP.
- **EAC − realizado:** custo a incorrer (570 mil). Compromisso de custo residual / custo a incorrer = cobertura de 50,9% no exemplo. O ETC adicional cobre o restante.
- Índices com denominador não positivo ficam **Sem base**. Valores não são artificialmente limitados a 100%.
- **Real/Compromisso modelo − referência externa:** calculados somente quando comparavel=SIM. Não altera a projeção. Engenharia tem diferença fictícia de Real +5 mil para demonstrar investigação.
- **EAC − Orçamento**, **EAC − Disposto** e **ETC − Plan.re.** são apresentados na ficha da referência quando os campos existem e o recorte foi declarado comparável. As duas últimas relações são diferenças de composição; valores diferentes não comprovam erro porque as definições podem diferir.

O orçamento informado, a baseline congelada e o plano remanescente são preservados separadamente. O relatório não reproduz disponibilidade orçamentária SAP, fórmula de Disposto nem código customizado ZOVRPS005. A grade mensal usa o ano do corte; compromissos previstos até o corte são identificados à parte, sem antecipar ou reprogramar valores.

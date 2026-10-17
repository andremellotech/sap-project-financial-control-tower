# Contrato dos dados normalizados

Oito CSVs obrigatórios, mesmo que alguns contenham somente cabeçalhos. UTF-8/BOM opcional, separador `;`, datas `AAAA-MM-DD`, períodos `AAAA-MM`, decimal com ponto e até duas casas, sem separador de milhar. Campos opcionais mantêm a coluna e célula vazia. Colunas extras são ignoradas. Não é importação automática de um layout SAP universal: prepare cópias e valide a semântica dos campos.

O manifesto declara BRL, corte no último dia do mês, baseline/forecast selecionados, aprovação da baseline, escopo, caráter fictício e nomes locais dos oito arquivos. Um arquivo por função, sem caminhos absolutos/subpastas. Limites por arquivo: 25 MiB e 50 mil registros. O conjunto de fatos e referências deve caber no intervalo seguro de inteiros JavaScript (soma absoluta em centavos ≤ 9.007.199.254.740.991). Datas e calendário são civis; períodos fiscais especiais não estão implementados.

## Cadastro PEP — peps.csv

`pep;pai;projeto;descricao;responsavel`

PEP é texto e chave única, pai vazio na raiz. Não há inferência pelo prefixo do código. Pai deve existir no mesmo projeto, sem ciclos. Valores financeiros somente em **folhas**. Cadastre a hierarquia completa desejada; não importe linhas de subtotal como novos lançamentos.

## Baseline — baseline.csv

`id;versao;pep;periodo;classe_custo;valor_brl`

Plano aprovado por folha, mês e classe de custo; valor não negativo. Uma única versão selecionada, igual ao manifesto. Chave natural: versão + PEP + período + classe. Agregue antes se houver várias linhas de planejamento da mesma combinação. Períodos podem cobrir anos anteriores/futuros, mantendo o mesmo horizonte de controle da análise. Aprovação não pode ser posterior ao corte. SHA-256 conserva a identidade do arquivo lido; não substitui aprovação ou assinatura documental.

## Custo realizado — cji3.csv

`id;pep;data;empresa;exercicio;documento;item;classe_custo;descricao;valor_brl;natureza;pedido;item_pedido`

Data de lançamento até o corte; empresa/exercício/documento/item obrigatórios. `natureza`: **CUSTO** ou **LIQUIDACAO**. Não carregue receitas como custo. Valores assinados: créditos/estornos negativos preservados. `pedido` e `item_pedido` opcionais, mas preenchidos juntos. Chave natural desta normalização: empresa + exercício + documento + item + PEP. A divisão por PEP já deve vir alocada e não pode replicar o valor integral do documento em cada destino. Não assumir que exercício é igual ao ano civil da data; isso depende do exercício SAP.

O exemplo exclui LIQUIDACAO do custo operacional, conservando a linha para análise. Essa política não é uma regra contábil universal: defina o perímetro sem duplicar remetente/destinatário, sem misturar estoques, capitalização ou receitas, e homologue a classificação antes de reutilizar.

## Compromisso residual de custo — cji5.csv

`id;pep;data_snapshot;tipo;documento;item;alocacao;classe_custo;descricao;data_prevista;valor_brl`

`data_snapshot` deve ser exatamente o corte; `tipo` **RC** ou **PC**. Valor residual de custo não negativo; nunca valor bruto original. Chave natural: tipo + documento + item + alocação. Em rateios, a alocação distingue as parcelas já distribuídas por PEP. Previsão pode estar vencida; continua como posição a revisar e não é movida automaticamente para outro mês. RC parcialmente convertida conserva somente o saldo residual próprio. O programa não recalcula reduções a partir dos recebimentos nem detecta sozinho sobreposição econômica entre RC e PC de IDs diferentes.

## Caixa — cjia.csv

`id;pep;data;tipo;empresa;exercicio;documento;item;classe_custo;descricao;valor_brl;pedido;item_pedido`

`tipo` **PAGAMENTO** (data até o corte, assinado) ou **COMPROMISSO_PAGAMENTO** (saldo de caixa não negativo na posição declarada; data prevista inclusive vencida). Manifesto declara o corte do snapshot; prepare todas as linhas com esse mesmo critério. Empresa/exercício/documento/item obrigatórios. Chave natural: empresa + exercício + documento + item + PEP. Referência de pedido opcional com item. Naturezas devem estar explicitamente identificadas a partir do layout/origem; não converter todo valor CJIA em pagamento realizado.

Tributos, adiantamentos, receitas, compensações e moeda podem fazer custo e caixa diferirem. Esta versão aceita somente a base de **saídas/custos do projeto** explicitamente preparada em BRL; não é fluxo de caixa completo nem contas a pagar.

## ETC gerencial — etc.csv

`id;versao;pep;periodo;classe_custo;valor_brl;premissa;responsavel`

Estimativa adicional futura **não coberta pelo residual CJI5**. Versão igual ao manifesto, valor não negativo, mês posterior ao corte, premissa e responsável obrigatórios. Chave: versão + PEP + mês + classe; consolide premissas da mesma combinação. Não carregar ETC total que já inclua pedidos ou RCs comprometidos: isso duplicaria o EAC. Ausência de sobreposição é uma declaração gerencial que precisa de validação; o código não lê o objeto de compra para comprová-la.

## Conciliação — conciliacoes.csv

`id;custo_id;pagamento_id;valor_brl`

Vínculos explícitos, um par custo/pagamento por linha. IDs existentes com naturezas CUSTO da CJI3 e PAGAMENTO da CJIA, mesmo PEP, classe e empresa. Exercícios podem ser diferentes. Valor alocado não zero, com sinal compatível nos dois lados; soma absoluta alocada não pode exceder o valor de cada linha de custo/pagamento. Um pagamento pode ser distribuído entre vários custos e vice-versa. Não concilia entre empresas, PEPs ou classes. Tributos/ajustes que não coincidam ficam fora da alocação até tratamento apropriado.

## Identidade e rastreabilidade

IDs financeiros são globais entre as cinco bases de fatos; IDs da conciliação são únicos no seu arquivo. São chaves preparadas pelo integrador, não códigos SAP universais. Preserve zeros e use representação canônica consistente dos documentos: o programa conserva os códigos como texto e não completa zeros nem deduz equivalência entre `1` e `001`.

Cada fato carrega arquivo e linha física inicial; os bytes exatos lidos são usados para SHA-256 e parsing. Saída inclui campos mapeados, manifesto, UUID e horário UTC. Colunas extras ignoradas não são reproduzidas na tabela de fatos, mas o hash identifica o arquivo original completo. CSVs gerados contêm valores inteiros em **centavos** e protegem textos semelhantes a fórmulas; não reimporte esses CSVs gerados como se fossem os arquivos de entrada em BRL decimal.

## Referência externa — conferencia_sap.csv

`id;fonte;pep;classe_custo;data_snapshot;realizado_brl;compromisso_brl;orcamento_brl;plan_re_brl;disposto_brl;comparavel;escopo`

Conferência independente, **não adicionada aos fatos, baseline ou EAC**. Fonte declarada, como ZOVRPS005 ou S_ALR_87013558. Uma linha por fonte + PEP folha + classe de custo, no mesmo corte. Real é assinado; compromisso não negativo. Orçamento (não negativo), Plan.re. e Disposto podem ficar vazios: vazio significa ausente, não zero. Preserve esses valores como foram definidos na origem, sem recompor Disposto por uma fórmula suposta. Valores precisam estar alocados nesse mesmo recorte, sem repetir um total de PEP em todas as classes.

`comparavel`: SIM ou NAO; escopo descritivo obrigatório. SIM declara que corte, moeda, período, natureza e granularidade foram conciliados pelo preparador. O programa não comprova essa declaração contra o SAP. NAO conserva os valores e deixa as diferenças de conferência sem conclusão. Diferenças comparáveis = modelo − referência; conferir principalmente seleção de objetos/classes, liquidações, subtotais e sinais. Ausência de linha não produz status conciliado. Se não houver referência, envie somente o cabeçalho.

O exemplo fictício do ZOVRPS005 adota as colunas informadas pelo usuário: Orçamento, Real, Compromisso, Plan.re., Disposto. Não há implementação do programa Z nem homologação da sua fórmula. A baseline aprovada não é substituída por Orçamento; Plan.re. não é assumido como ETC adicional. O nome dos campos no extrato deve ser mapeado manualmente para este contrato normalizado.

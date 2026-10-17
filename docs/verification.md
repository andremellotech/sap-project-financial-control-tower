# Verificação local

## Refinamento executivo 1.2.1 — 15/10/2026

- Revisão de apresentação da aba Projeção: recorte explícito, resumo de fechamento, rótulos acima das barras, desvio por coluna e total destacado. Indicadores repetidos retirados.
- Sensibilidade Aurora +10% conferida em R$ 1.078.000; abertura das seis premissas e retorno à seção recolhida verificados.
- Portfólio agrupado em quatro projetos mais total: saldo restante de 2,8 milhões e parcela realizada de 52,9%. Clique em Atlas passou a seis PEPs mais total; ficha PRJ-03.01.02 abriu corretamente.
- Tela de 320 px: página e conteúdo com 305 px, resumo sem transbordamento e rolagem limitada ao gráfico. Viewport restaurado.
- Console sem avisos/erros observados na navegação verificada. Fórmulas, fontes, dados e hashes preservados frente ao ZIP 1.2.0.

## Colunas de build-up 1.2.0 — 15/10/2026

- Agrupamentos JavaScript conferidos com 22 PEPs e quatro projetos; soma das colunas igual ao total, sem incorporar pais novamente. Recortes por subárvore/classe, vazio e crédito líquido cobertos.
- Navegador: 23 colunas no portfólio por PEP e cinco por projeto. Clique em Horizonte passou a seis PEPs mais total de 2,32 milhões. Subárvore PRJ-01.01 mostrou três folhas mais total de 920 mil; filtro EQUIPAMENTOS reduziu para uma folha mais total de 470 mil. Combinação incompatível mostrou estado vazio.
- Rolagem horizontal conferida com deslocamento superior a 2.200 px, preservando a posição da coluna total na borda direita. Escala comum e baseline individual indicadas.
- Em 320 px, conteúdo da página e largura disponível de 305 px; rolagem limitada ao componente. Viewport restaurado após o teste.
- Coluna de engenharia abriu ficha PRJ-01.01.01; total do recorte Aurora abriu matriz com seis nós. Console sem avisos/erros observados. Captura do build-up atualizada.
- Fontes, dados, referências e totais financeiros preservados frente ao ZIP 1.1.0. Nenhuma nova conexão SAP.

## Portfólio fictício 1.1.0 — 15/10/2026

- Quatro projetos, 22 folhas, 33 nós hierárquicos e 700 fatos validados. Totais independentes: baseline 5,8 milhões, realizado 3,15 milhões, residual CJI5 1,62 milhão, ETC 1,18 milhão e EAC 5,95 milhões.
- Novo teste de cenários por projeto: Aurora 1,05 milhão, Horizonte 2,32 milhões, Atlas 1,82 milhão e Vértice 760 mil de EAC. Testes anteriores atualizados para os totais consolidados, conservando a conferência dos exemplos Aurora.
- 25 testes Python aprovados; filtros e totais JavaScript confrontados com o SQL. Custo e caixa continuam separados, sem duplicação dos pais.
- Cards de projeto clicáveis conferidos. Horizonte/Infraestrutura com EAC de 620 mil; troca para Atlas limpou o PEP incompatível. Matriz com 33 linhas e ficha PRJ-03.01.02 com EAC de 700 mil.
- Oito perspectivas abertas, sem avisos/erros de console observados. Visão executiva, Aderência e Projeção em 320 px sem transbordamento horizontal; viewport restaurado.
- Capturas e guias atualizados para o portfólio. Os exemplos permanecem inteiramente fictícios e não constituem integração ativa ou homologação SAP.

## Build-up complementar 1.0.2 — 15/10/2026

- Coluna única conferida no resumo e em Projeção: realizado 480 mil + projetado restante 570 mil = EAC 1,05 milhão; baseline de 1 milhão independente.
- Filtro Engenharia com realizado 100 mil, restante 120 mil e EAC 220 mil. Recorte Engenharia/EQUIPAMENTOS vazio, sem coluna artificial.
- Em 320 px, página e componente sem transbordamento horizontal; os três valores do build-up permaneceram completos em uma linha. Viewport restaurado após a conferência.
- Console sem avisos/erros durante a navegação verificada. Capturas de Visão executiva e Projeção atualizadas.
- Dados, totais, referências, alertas e hashes comparados com o ZIP 1.0.1 e preservados. Geração sem novas dependências.

## Refinamento visual 1.0.1 — 14/10/2026

- Dados, totais, referências, alertas, mensalização e hashes de todas as fontes comparados com a versão 1.0.0 e preservados.
- Ícones SVG incorporados ao HTML, sem novas dependências ou requisições de rede; números monetários e índices com alinhamento uniforme.
- Oito perspectivas verificadas no desktop e em 320 px; página sem transbordamento horizontal. Tabelas longas conservam rolagem própria.
- Cards de indicadores com alturas iguais no desktop padrão e em 1440 px. Valores principais conferidos em 390 px, com números completos em uma linha; ficha PEP em 320 px sem transbordamento.
- Ficha da referência V01 e trilha documento/roteiro CJI3 verificadas após as alterações. Filtros Engenharia e Engenharia/EQUIPAMENTOS mantiveram os valores esperados.
- 24 testes Python, verificações JavaScript e reprodução do build/demo na cópia extraída do pacote atualizados. Console sem avisos/erros observados durante a navegação.
- Capturas do README substituídas pela interface 1.0.1. Nenhuma nova capacidade de integração SAP é anunciada neste refinamento.

## Registro inicial 1.0.0

Verificação em 14/10/2026, Windows, Python 3.12 e Node.js 24. A matriz remota Windows/Ubuntu × Python 3.11/3.12/3.13 está configurada; não há resultado remoto de CI nesta entrega.

## Regras e artefatos

- 24 testes Python: custo/caixa/EAC distintos, sinais, liquidação, folhas/pais/ciclos, snapshot e corte mensal, versões, chaves, conciliações assinadas, limites por documento, empresa, ausência de dados, referências externas comparáveis/não comparáveis, nulos e duplicidades.
- Verificações JavaScript: confronto dos indicadores com o resultado SQL real, filtros por projeto/subárvore/classe, recorte vazio, índices sem base e seleção de referências externas.
- Build reproduzido a partir do ZIP extraído; JSON/SQLite/HTML/CSVs e hashes comparados com a entrada fictícia. Valores conferidos independentemente com Decimal a partir dos CSVs.
- Escape de dados HTML/CSV, destino existente/entrada protegidos e preservação dos bytes de origem verificados.
- Integridade, hierarquia de pastas, links locais e recursos do pacote conferidos.

## Navegador

- Oito perspectivas abertas por HTTP local, sem avisos/erros de console observados.
- Engenharia com baseline 200 mil, custo 100 mil e EAC 220 mil; combinação Engenharia/EQUIPAMENTOS com indicadores zerados.
- PEP → custo 5100001002 → roteiro CJI3: número/item preservados, 20 mil alocados e 20 mil de custo sem alocação. Compromisso 4500010003 → roteiro CJI5 preservando o documento; troca manual de guia limpa o contexto anterior.
- Referência ZOVRPS005 V01 com Orçamento/Real/Compromisso/Plan.re./Disposto fictícios; diferença de Real +5 mil exposta. Aderência EAC/baseline 105%, execução financeira/plano 64%, cobertura do restante 50,9%.
- Leitura mensal expandida, com saldo CJI5 até o corte separado dos meses futuros. Simulação ETC +10%: EAC 1.078.000 BRL e baseline preservada.
- Download real da seleção CJI3 5100001004: uma linha A04, valor −2.000.000 centavos, lida e conferida.
- Sete vistas originais conferidas em 390 px; matriz/ficha PEP e nova aderência/ficha de referência também em 320 px. Corrigido transbordamento de valores monetários em 320 px; página/ficha com largura de conteúdo igual à largura disponível após correção. Tabelas mantêm rolagem própria.
- Capturas reais da interface em `docs/images/`.

## Alcance

Não há homologação em um SAP real, execução de transações, adaptação automática do ZOVRPS005, comprovação de fórmulas locais Plan.re./Disposto, ingestão XLSX, PBIX nativo ou publicação remota. Os exemplos e os totais de referência são fictícios; a classificação e a declaração de comparabilidade dependem de quem prepara as extrações. Conferência numérica não equivale a aprovação financeira.

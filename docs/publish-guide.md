# Publicar pelo GitHub web

Repositório sugerido: **sap-project-financial-control-tower**, conta **andremellotech**.

Descrição para copiar:

```text
Controle financeiro por elemento PEP com baseline aprovada, projeção EAC, realizado CJI3, compromissos CJI5 e caixa CJIA. Python, SQL e relatório visual com dados fictícios.
```

1. Baixe e extraia o ZIP completo. Abra a pasta interna `sap-project-financial-control-tower`.
2. No GitHub, crie um repositório Public com esse nome. Não inicialize README, licença ou gitignore adicionais: o pacote já os contém.
3. Use **Add file → Upload files** e arraste o conteúdo interno, incluindo pastas inteiras. Não envie o ZIP nem junte arquivos de subpastas na raiz.
4. Antes do commit, confira caminhos como `finance/loader.py`, `sql/views.sql`, `scripts/build_site.py` e `.github/workflows/validate.yml`. Se aparecer apenas `loader.py` na raiz, corrija o envio preservando a pasta.
5. Mensagem sugerida: `Publicar SAP Project Financial Control Tower v1.2.1`. Faça o commit na branch adequada; siga eventual exigência de revisão do repositório.

O [upload web do GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) aceita até 100 arquivos por envio e 25 MiB por arquivo. O pacote foi preparado dentro desses limites. Arquivos ocultos podem exigir habilitar sua visualização no Explorador; `.github` e `.gitignore` fazem parte das fontes; o build cria `.nojekyll` em `dist`.

## Disponibilizar a demonstração visual

O repositório não ativa o GitHub Pages automaticamente. Para uso offline, execute `python scripts/build_site.py` e distribua `dist`. Se optar por hospedagem no futuro, publique somente `dist`, preservando seus caminhos.

O workflow `Validate project finance` usa permissão de leitura, testa e gera um artefato `offline-demo` com `.nojekyll`. Não contém job de deploy nem altera configurações de hospedagem.

## Conferir depois do envio

- Abra a demonstração, navegue nas oito perspectivas e os quatro cards de projeto. Selecione AURORA e confira o PEP de engenharia com EAC de R$ 220 mil. Em Aderência, confira a diferença fictícia de R$ 5 mil na referência V01.
- Abra um documento e seu roteiro; confira filtros e downloads.
- Veja a execução dos seis jobs de validação na aba Actions. Os resultados remotos só podem ser afirmados depois que o GitHub mostrar a conclusão.
- No About, configure Website com a URL confirmada e tópicos: `sap`, `sap-gui`, `project-system`, `wbs`, `financial-analysis`, `python`, `sql`, `portfolio`.
- Se mudar conta/nome, ajuste links no README e `web/template.html`, e execute `python -m finance demo` antes de enviar os artefatos atualizados.

O pacote público contém somente exemplos fictícios. O `.gitignore` não remove arquivos escolhidos em um upload manual: selecione apenas o conteúdo do ZIP da entrega, sem pastas locais de dados/saídas reais. Não há publicação automática nesta entrega.

## Fontes e artefatos gerados

Antes do envio, execute `python scripts/build_site.py` e abra `dist/index.html`. HTML, JSON, CSV, Excel e SQLite demonstrativos são derivados, ignorados pelo Git e recuperáveis a partir das fontes; os mesmos caminhos são recriados no pacote final. Para enviar as fontes pelo navegador, omita `dist`, ambientes virtuais, caches e pastas locais. Para distribuir a demonstração offline, envie `dist` inteira separadamente. Não selecione dados próprios.

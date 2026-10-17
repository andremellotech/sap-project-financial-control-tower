# Publicar pelo GitHub web

Repositório sugerido: **sap-project-financial-control-tower**, conta **andremellotech**.

Descrição para copiar:

```text
Controle financeiro por elemento PEP com baseline aprovada, projeção EAC, realizado CJI3, compromissos CJI5 e caixa CJIA. Python, SQL e relatório visual com dados fictícios.
```

1. Baixe e extraia o ZIP completo. Abra a pasta interna `sap-project-financial-control-tower`.
2. No GitHub, crie um repositório Public com esse nome. Não inicialize README, licença ou gitignore adicionais: o pacote já os contém.
3. Use **Add file → Upload files** e arraste o conteúdo interno, incluindo pastas inteiras. Não envie o ZIP nem junte arquivos de subpastas na raiz.
4. Antes do commit, confira caminhos como `finance/loader.py`, `sql/views.sql`, `reports/demo/finance.sqlite` e `.github/workflows/validate.yml`. Se aparecer apenas `loader.py` na raiz, corrija o envio preservando a pasta.
5. Mensagem sugerida: `Publicar SAP Project Financial Control Tower v1.2.1`. Faça o commit na branch adequada; siga eventual exigência de revisão do repositório.

O [upload web do GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) aceita até 100 arquivos por envio e 25 MiB por arquivo. O pacote foi preparado dentro desses limites. Arquivos ocultos podem exigir habilitar sua visualização no Explorador; `.github`, `.gitignore` e `.nojekyll` fazem parte do pacote.

## Disponibilizar a demonstração visual

Em **Settings → Pages → Source**, selecione **Deploy from a branch**, depois **main** e **/(root)**, e salve. Aguarde a publicação e use Visit site para confirmar o endereço. O esperado é `https://andremellotech.github.io/sap-project-financial-control-tower/`. A [documentação oficial explica a publicação por branch](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

O HTML já está pronto e o pacote inclui `.nojekyll`. O workflow `Validate project finance` é somente de testes; não precisa criar um workflow de deploy para usar publicação por branch. Ele usa permissão de leitura. Se `.github` não for enviada, crie `.github/workflows/validate.yml` no editor web copiando o arquivo do pacote.

## Conferir depois do envio

- Abra a demonstração, navegue nas oito perspectivas e os quatro cards de projeto. Selecione AURORA e confira o PEP de engenharia com EAC de R$ 220 mil. Em Aderência, confira a diferença fictícia de R$ 5 mil na referência V01.
- Abra um documento e seu roteiro; confira filtros e downloads.
- Veja a execução dos seis jobs de validação na aba Actions. Os resultados remotos só podem ser afirmados depois que o GitHub mostrar a conclusão.
- No About, configure Website com a URL confirmada e tópicos: `sap`, `sap-gui`, `project-system`, `wbs`, `financial-analysis`, `python`, `sql`, `portfolio`.
- Se mudar conta/nome, ajuste links no README e `web/template.html`, e execute `python -m finance demo` antes de enviar os artefatos atualizados.

O pacote público contém somente exemplos fictícios. O `.gitignore` não remove arquivos escolhidos em um upload manual: selecione apenas o conteúdo do ZIP da entrega, sem pastas locais de dados/saídas reais. Não há publicação automática nesta entrega.

# Vértice — Universo da marca

Página estática responsiva, sem dependências de execução. 23 artes criadas a partir do manual e organizadas em SVG, PNG e PDF, mais manual original e ZIP completo.

## Desenvolvimento

Na raiz do projeto: `python -m http.server 4173 --bind 0.0.0.0`. Acesse a página pelo servidor disponível na sua hospedagem. Não exige build, variáveis de ambiente ou backend.

## Publicação

Publique a raiz do projeto como site estático; inclua `assets/`, `downloads/`, `index.html`, `style.css` e `app.js`. Não publique a pasta `.git`. Os downloads são relativos e funcionam em subdiretórios, inclusive GitHub Pages.

## Geração

`tools/build.py` usa PyMuPDF e o PDF fonte indicado no script para gerar as artes. `tools/site.py` gera o HTML a partir de `catalog.json`. Os arquivos finais já estão incluídos; nenhuma geração é necessária para publicar.

Veja `downloads/LEIA-ME.txt` para escopo, fontes e especificações de produção. O escopo foi inferido do PDF, sem acesso à conversa contratual anterior. As artes impressas precisam de preparação técnica pela gráfica.

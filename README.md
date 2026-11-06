# Vértice — Identidade em cada detalhe

Site estático responsivo com seis seções: marca, papelaria, grafismos, adesivos, banner e manual. As duas versões do logotipo foram revisadas para corrigir Vértice e MODA FEMININA; o monograma foi mantido. Cartão (frente e verso), papel timbrado A4, envelope comercial, três grafismos, três adesivos e banner editorial compõem a revisão 02. Materiais de redes sociais da primeira versão foram removidos.

## Desenvolvimento e publicação

Execute `python -m http.server 4173 --bind 127.0.0.1` na raiz. Não há dependências de execução ou build. Publique `index.html`, `style.css`, `app.js`, `.nojekyll`, `assets/` e `downloads/`. Os caminhos relativos suportam GitHub Pages em subdiretório. As branches main e gh-pages recebem os arquivos de publicação.

## Geração

`python tools/build.py` usa PyMuPDF e python-docx, a matriz vetorial revisada `assets/logo-master.svg` e a fotografia em `assets/editorial-vertice.png`. Gera SVGs, PNGs, PDFs, kits individuais e kit completo. Todas as aplicações são regeneradas a partir da matriz revisada. O manual de 26 páginas é gerado por `tools/manual.py`. `python tools/site.py` recria a página com o catálogo. Os resultados já estão incluídos no repositório.

O cartão reúne frente e verso no mesmo kit e PDF de duas páginas. O papel timbrado inclui DOCX com texto editável e arte de fundo. A versão pública é institucional, sem dados pessoais e sem campos de contato pendentes. Arte do envelope corresponde à face externa, sem faca. Consulte `downloads/LEIA-ME.txt` para dimensões e preparação de impressão.

A fotografia editorial foi gerada com IA para a composição. O logotipo foi corrigido em curvas; fontes de apoio Georgia e Arial nos textos novos. As fontes completas indicadas no manual não foram fornecidas.

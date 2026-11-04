# Vértice — Identidade em cada detalhe

Site estático responsivo com seis seções: marca, papelaria, grafismos, adesivos, banner e manual. As três marcas aprovadas foram mantidas. Cartão (frente e verso), papel timbrado A4, envelope comercial, três grafismos, três adesivos e banner editorial compõem a revisão 02. Materiais de redes sociais da primeira versão foram removidos.

## Desenvolvimento e publicação

Execute `python -m http.server 4173 --bind 127.0.0.1` na raiz. Não há dependências de execução ou build. Publique `index.html`, `style.css`, `app.js`, `.nojekyll`, `assets/` e `downloads/`. Os caminhos relativos suportam GitHub Pages em subdiretório. As branches main e gh-pages recebem os arquivos de publicação.

## Geração

`python tools/build.py` usa PyMuPDF e python-docx, o manual em `downloads/` e a fotografia em `assets/editorial-vertice.png`. Gera SVGs, PNGs, PDFs, kits individuais e kit completo. As três marcas existentes são preservadas. `python tools/site.py` recria a página com o catálogo. Os resultados já estão incluídos no repositório.

O cartão reúne frente e verso no mesmo kit e PDF de duas páginas. O papel timbrado inclui DOCX com texto editável e arte de fundo. Os campos de contato estão marcados para substituição pelos dados reais. Arte do envelope corresponde à face externa, sem faca. Consulte `downloads/LEIA-ME.txt` para dimensões e preparação de impressão.

A fotografia editorial foi gerada com IA para a composição. O logotipo original foi preservado em curvas; fontes de apoio Georgia e Arial nos textos novos. As fontes completas indicadas no manual não foram fornecidas.

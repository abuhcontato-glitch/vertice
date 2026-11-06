from pathlib import Path
import re,subprocess
R=Path(__file__).resolve().parents[1]
# Pin all assets to the verified corrected revision, avoiding the stale Pages deployment.
revision='65bb0505ee09cf28e0818aa55c56d10112aa2fac'
base=f'https://raw.githubusercontent.com/abuhcontato-glitch/vertice/{revision}/'
s=(R/'index.html').read_text()
s=re.sub(r'<link rel="stylesheet"[^>]+>',lambda _: '<style>'+(R/'style.css').read_text()+'</style>',s)
js=(R/'app.js').read_text()+'''
// Download public files through a same-origin blob so the download filename is preserved.
document.querySelectorAll('a[download]').forEach(link => {
  link.addEventListener('click', async event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const old = link.innerHTML;
    link.setAttribute('aria-busy', 'true');
    try {
      const response = await fetch(link.href, {credentials: 'omit'});
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const save = document.createElement('a');
      save.href = url;
      save.download = new URL(link.href).pathname.split('/').pop();
      document.body.appendChild(save);
      save.click();
      save.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch (error) {
      window.open(link.href, '_blank', 'noopener');
    } finally {
      link.removeAttribute('aria-busy');
      link.innerHTML = old;
    }
  });
});
'''
s=re.sub(r'<script src="app.js[^\"]*"></script>',lambda _: '<script>'+js+'</script>',s)
s=re.sub(r'((?:src|href|data-preview)=")((?:assets|downloads)/[^\"]+)(")',lambda m:m[1]+base+m[2]+m[3],s)
s=s.replace('<title>Vértice — Identidade em cada detalhe</title>','<title>Vértice — Identidade visual corrigida</title>')
(R/'entrega-corrigida.html').write_text(s)
assert 'élrtice' not in s and 'Moda Femina' not in s
assert 'Ana Cláudia' not in s and 'Apartamento 107' not in s
print('Standalone corrected page created; verified public assets pinned to revision',revision)

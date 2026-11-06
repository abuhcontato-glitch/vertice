from pathlib import Path
import fitz
R=Path(__file__).resolve().parents[1];A=R/'assets';D=R/'downloads'
W=(.412,.133,.204);P=(.933,.851,.855);C=(.98,.965,.937)
manual=fitz.open()
logo=(A/'logo-master.svg').read_text()
def vector(pg,svg,box):
 d=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open('pdf',d.convert_to_pdf());pg.show_pdf_page(fitz.Rect(box),pdf,0)
def text(pg,box,t,size=15,font='helv',color=W):
 fontkey='BrandSerif' if font=='tiro' else 'BrandSans'
 fontfile='/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf' if font=='tiro' else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
 pg.insert_font(fontname=fontkey,fontfile=fontfile)
 font=fontkey
 res=-1
 while res<0 and size>=8:
  res=pg.insert_textbox(fitz.Rect(box),t,fontsize=size,fontname=font,color=color,lineheight=1.4)
  size-=.5
 assert res>=0,(t,res)
def page(title,desc='',dark=False):
 pg=manual.new_page(width=960,height=600);fg=C if dark else W
 pg.draw_rect(pg.rect,color=None,fill=W if dark else C)
 text(pg,(45,22,800,55),'VÉRTICE / MODA FEMININA',10,'helv',fg)
 text(pg,(860,22,925,55),f'{len(manual):02d} / 26',9,'helv',fg)
 if title:text(pg,(45,76,915,130),title,31,'tiro',fg)
 if desc:text(pg,(45,140,900,205),desc,12,'helv',fg)
 pg.draw_line((45,552),(915,552),color=fg,width=.4)
 text(pg,(45,562,900,595),'MANUAL DE IDENTIDADE VISUAL / REVISÃO DE GRAFIA',8,'helv',fg)
 return pg
pg=page('',dark=True);vector(pg,logo,(190,105,770,425));text(pg,(225,462,820,505),'IDENTIDADE VISUAL · VERSÃO REVISADA',14,'helv',C)
pg=page('Uma essência. Presença em cada detalhe.','A Vértice traduz elegância, feminilidade e movimento em uma identidade reconhecível.')
text(pg,(75,235,865,490),'Este manual reúne as assinaturas corrigidas e as aplicações atuais da marca. A escrita oficial é Vértice — Moda Feminina.\n\nA revisão remove uma letra extra do nome e corrige o subtítulo para MODA FEMININA. As cores, o gesto caligráfico e o conceito visual foram mantidos.',19,'tiro')
pg=page('Paleta da marca','As cores principais são vinho e rosa. O marfim é uma cor de apoio para fundos e áreas de respiro.')
for x,color,label,desc in [(45,W,'VINHO','#692234 · RGB 105 / 34 / 52'),(345,P,'ROSA','#EED9DA · RGB 238 / 217 / 218'),(645,C,'MARFIM DE APOIO','#FAF6EF · RGB 250 / 246 / 239')]:
 pg.draw_rect(fitz.Rect(x,220,x+270,420),color=W,fill=color,width=.4);text(pg,(x,440,x+280,470),label,13);text(pg,(x,476,x+280,520),desc,10)
pg=page('Assinatura principal · vinho','Usar sobre fundos claros, com contraste e área de respiro.');vector(pg,logo.replace('#fff2dd','#692234'),(180,215,780,515))
pg=page('Assinatura principal · clara','Usar sobre o vinho da marca ou fundos escuros com leitura consistente.',True);vector(pg,logo,(180,215,780,515))
pg=page('Monograma V','O gesto caligráfico funciona como símbolo, selo e elemento de apoio.');pg.insert_image(fitz.Rect(320,210,640,520),filename=str(A/'monograma.png'))
pg=page('Área de proteção','Reserve, em todos os lados, uma margem livre equivalente à altura do subtítulo.')
vector(pg,logo.replace('#fff2dd','#692234'),(235,225,725,495));pg.draw_rect(fitz.Rect(190,195,770,525),color=W,dashes='[4 4]',width=.6)
pg=page('Redução e legibilidade','Reduzir mantendo proporções. A leitura de MODA FEMININA deve permanecer clara no tamanho final.')
for box in [(75,235,475,455),(565,275,835,425)]:vector(pg,logo.replace('#fff2dd','#692234'),box)
text(pg,(75,480,875,525),'Faça uma prova no tamanho real. Quando o subtítulo perder leitura, use o monograma.',13)
pg=page('Escrita oficial da marca','Acentuação, ordem das letras e subtítulo devem ser mantidos em todas as aplicações.')
text(pg,(75,245,875,350),'Vértice',66,'tiro');text(pg,(78,375,875,425),'MODA FEMININA',28)
text(pg,(78,455,875,515),'Em textos corridos: Vértice — Moda Feminina. No logotipo: usar o arquivo vetorial revisado.',13)
pg=page('Tipografia','A identidade de origem indica Citadel Script e Wichittra.')
text(pg,(75,235,875,510),'O logotipo revisado está em curvas e não depende da instalação de fontes.\n\nOs textos de apoio das aplicações usam Georgia e Arial. Os arquivos completos e as licenças das fontes indicadas no manual de origem não foram fornecidos; não são distribuídos neste kit.\n\nEvite simular ou redigitar o logotipo com outra fonte.',17,'tiro')
def art(title,desc,slug,box=(160,215,800,525)):
 pg=page(title,desc);pg.insert_image(fitz.Rect(box),filename=str(A/f'{slug}.png'),keep_proportion=True);return pg
art('Grafismo 01 · gesto','Recorte do monograma para cantos, fundos e assinaturas.','grafismo-gesto')
art('Grafismo 02 · trama V','Repetição geométrica como textura de apoio, sem competir com o logotipo.','grafismo-trama')
art('Grafismo 03 · movimento','Linhas fluidas inspiradas no caimento dos tecidos.','grafismo-seda')
art('Cartão de visita · frente','90 × 50 mm. Contraste vinho e rosa, gesto caligráfico e assinatura clara.','cartao-frente')
art('Cartão de visita · verso','90 × 50 mm. Versão pública institucional, sem dados pessoais.','cartao-verso')
art('Papel timbrado','A4. Área de escrita livre, cabeçalho de marca e rodapé institucional.','papel-timbrado')
art('Envelope comercial','220 × 110 mm. Face externa; aplicar à faca fornecida pela gráfica.','envelope')
art('Adesivo circular','Diâmetro sugerido: 60 mm. Monograma e nome em proporção equilibrada.','adesivo-circular')
art('Adesivo horizontal','120 × 40 mm. Assinatura e grafismo em uma composição alongada.','adesivo-horizontal')
art('Adesivo vertical','45 × 75 mm. Contraste de cores e leitura em dois momentos.','adesivo-vertical')
art('Banner editorial','Fotografia, recorte orgânico e tipografia. Arte horizontal: 1920 × 1000 px.','banner-editorial', (45,215,915,530))
pg=page('Direção fotográfica','Luz suave, tecidos fluidos, tons vinho e rosa, cenários claros e presença feminina confiante.')
pg.insert_image(fitz.Rect(460,220,915,530),filename=str(A/'editorial-vertice.png'))
text(pg,(55,240,420,520),'Valorizar o caimento, o movimento e os detalhes das peças.\n\nA fotografia deste kit foi gerada com IA para a composição visual. Não representa uma coleção real da loja.',15,'tiro')
pg=page('Combinação e contraste','Priorizar pares de cores que preservem a leitura e a personalidade da marca.')
for box,bg,fg,label in [((45,235,465,485),W,C,'CLARO SOBRE VINHO'),((495,235,915,485),P,W,'VINHO SOBRE ROSA')]:
 pg.draw_rect(fitz.Rect(box),color=None,fill=bg);text(pg,(box[0]+30,box[1]+95,box[2]-20,box[3]-30),label,22,'helv',fg)
pg=page('Cuidados de aplicação','Preserve a integridade das assinaturas.')
text(pg,(75,235,875,515),'Não distorcer, inclinar ou alterar as proporções.\nNão trocar as letras ou a acentuação do nome.\nNão abreviar FEMININA no subtítulo.\nNão aplicar sobre fotografias sem contraste suficiente.\nNão usar os arquivos anteriores à revisão de grafia.',18,'tiro')
pg=page('Arquivos e produção','SVG para edição, PNG para uso digital e PDF para compartilhamento e preparação de impressão.')
text(pg,(75,225,875,520),'O papel timbrado inclui Word editável. Os kits ZIP reúnem os formatos de cada peça.\n\nOs PDFs físicos estão em tamanho final, RGB e sem sangria. A gráfica deve validar perfil de cor, sangria, corte, margens de segurança, materiais e acabamentos. O envelope é uma face de aplicação, não uma faca estrutural.\n\nA versão pública não contém nome, endereço ou documento pessoal da cliente.',16,'tiro')
pg=page('Uma marca. Uma escrita.','Use sempre os arquivos revisados, disponíveis na página da Vértice.',True);vector(pg,logo,(230,235,730,510))
assert len(manual)==26
manual.save(D/'manual-identidade-visual-vertice.pdf',garbage=4,deflate=True)
manual[0].get_pixmap(matrix=fitz.Matrix(.8,.8)).save(A/'manual.png')
print('Manual revisado: 26 páginas, com escrita e aplicações corrigidas.')

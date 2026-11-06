from pathlib import Path
import fitz, re, shutil, json, zipfile, html, sys, base64
R=Path(__file__).resolve().parents[1]; D=R/'downloads'; A=R/'assets';D.mkdir(exist_ok=True);A.mkdir(exist_ok=True)
WINE='#692234';PINK='#EED9DA';CREAM='#FAF6EF'
s=(A/'logo-master.svg').read_text()
logo_light=s
logo_dark=s.replace('#fff2dd',WINE)
(A/'logo.svg').write_text(logo_dark)
# Preserve the original monogram path, without redrawing the mark.
mono=re.search(r'(<path transform="matrix\(\.260293.*?fill="#fff2dd"/>)',s).group(1)
def monogram(color):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="390 240 330 265">'+mono.replace('#fff2dd',color)+'</svg>'
items=[]
def text(x,y,t,size=38,color=WINE,family='Georgia',anchor='start',spacing=0):
 return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" text-anchor="{anchor}" letter-spacing="{spacing}">{html.escape(t)}</text>'
def nested(svg,x,y,w,h):
 vb=[float(v) for v in re.search(r'viewBox="([^"]+)"',svg).group(1).split()]
 scale=min(w/vb[2],h/vb[3]); tx=x+(w-vb[2]*scale)/2-vb[0]*scale;ty=y+(h-vb[3]*scale)/2-vb[1]*scale
 inner=re.sub(r'^<svg[^>]*>','',svg).rsplit('</svg>',1)[0]
 return f'<g transform="translate({tx} {ty}) scale({scale})">{inner}</g>'

def rect(x,y,w,h,fill):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
def save(slug,title,category,w,h,body,desc,physical=None):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{html.escape(title)}</title>{body}</svg>'
 (D/f'{slug}.svg').write_text(svg)
 doc=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open('pdf',doc.convert_to_pdf())
 if physical:
  target=fitz.open();pg=target.new_page(width=physical[0]*72/25.4,height=physical[1]*72/25.4);pg.show_pdf_page(pg.rect,pdf,0);pdf=target
 pdf.save(D/f'{slug}.pdf')
 pix=doc[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=category=='Marca');pix.save(D/f'{slug}.png')
 thumb=doc[0].get_pixmap(matrix=fitz.Matrix(min(640/w,640/h),min(640/w,640/h)),alpha=category=='Marca');thumb.save(A/f'{slug}.png')
 items.append(dict(slug=slug,title=title,category=category,description=desc,width=w,height=h))
def base(w,h,dark=False):
 bg=WINE if dark else CREAM;fg=CREAM if dark else WINE
 return rect(0,0,w,h,bg)+f'<rect x="{w*.045}" y="{h*.04}" width="{w*.91}" height="{h*.92}" fill="none" stroke="{PINK if dark else WINE}" stroke-opacity=".35"/>',fg
save('logotipo-vinho','Logotipo · vinho','Marca',1200,660,nested(logo_dark,0,0,1200,660),'Grafia revisada: Vértice · Moda Feminina. Fundo transparente.')
save('logotipo-claro','Logotipo · claro','Marca',1200,660,nested(logo_light,0,0,1200,660),'Versão clara com fundo transparente, para superfícies escuras.')
save('monograma','Monograma V','Marca',800,800,nested(monogram(WINE),80,80,640,640),'Símbolo original extraído da construção do logotipo.')
# Three complementary graphic systems: calligraphic gesture, V lattice and silk ribbons.
def gesture(w,h,color=WINE,opacity=1):
 return f'<g opacity="{opacity}">'+nested(monogram(color),-.25*w,-.25*h,w*1.6,h*1.5)+'</g>'
def lattice(w,h,color=WINE,opacity=.24):
 lines=[]
 for row in range(-1,int(h/150)+2):
  for col in range(-1,int(w/170)+2):
   x=col*170+(85 if row%2 else 0);y=row*150
   lines.append(f'<path d="M{x-70} {y-65} L{x} {y+65} L{x+70} {y-65}" fill="none" stroke="{color}" stroke-width="1.5"/>')
 return f'<g opacity="{opacity}">'+''.join(lines)+'</g>'
def ribbons(w,h,color=WINE,opacity=.55):
 paths=[]
 for i in range(13):
  y=h*.12+i*h*.048
  paths.append(f'<path d="M{-w*.1} {y} C{w*.30} {y-h*.45} {w*.36} {y+h*.58} {w*.61} {y+h*.20} S{w*.86} {y-h*.44} {w*1.1} {y-h*.22}" fill="none" stroke="{color}" stroke-width="{1.1+i*.1}"/>')
 return f'<g opacity="{opacity}">'+''.join(paths)+'</g>'
# Stationery is the second section, following only the three approved marks.
b=rect(0,0,1080,600,WINE)+rect(0,0,155,600,PINK)+f'<path d="M155 0 C400 110 105 430 360 600 H155Z" fill="{PINK}"/>'
b+=f'<g opacity=".16">'+nested(monogram(PINK),650,-80,600,630)+'</g>'+nested(logo_light,315,135,560,308)
b+=text(350,536,'ELEGÂNCIA QUE VALORIZA QUEM VOCÊ É.',13,PINK,'Arial',spacing=1.8)
save('cartao-frente','Cartão de visita · frente','Papelaria',1080,600,b,'90 × 50 mm · composição assimétrica, assinatura em curvas e gesto caligráfico.',(90,50))
b=rect(0,0,1080,600,CREAM)+rect(0,0,1080,14,WINE)+rect(840,0,240,600,PINK)
b+=lattice(1080,600,WINE,.08)+rect(0,135,835,355,CREAM)+nested(monogram(WINE),840,195,210,180)
b+=text(72,95,'VÉRTICE / MODA FEMININA',16,WINE,'Arial',spacing=3)+text(74,213,'Seu estilo.',45)+text(74,269,'Sua essência.',45)
b+=text(74,380,'MODA FEMININA',16,WINE,'Arial',spacing=3)
b+=text(74,550,'SEU ESTILO. SUA ESSÊNCIA.',13,WINE,'Arial',spacing=2)
save('cartao-verso','Cartão de visita · verso','Papelaria',1080,600,b,'90 × 50 mm · verso institucional, sem dados pessoais ou campos pendentes.',(90,50))
w,h=1240,1754
b=rect(0,0,w,h,CREAM)+rect(0,0,w,12,WINE)+nested(logo_dark,94,75,310,170)
b+=f'<path d="M980 0H1240V520C1170 430 1030 180 980 0Z" fill="{PINK}"/>'
b+=f'<g opacity=".18">'+nested(monogram(WINE),1005,25,285,300)+'</g>'
b+=f'<path d="M0 1630C310 1585 460 1805 800 1720S1110 1570 1240 1605V1754H0Z" fill="{PINK}"/>'
b+=text(94,1635,'VÉRTICE • MODA FEMININA',13,WINE,'Arial',spacing=2)+text(94,1675,'Elegância que valoriza quem você é.',15,WINE,'Arial')
save('papel-timbrado','Papel timbrado','Papelaria',w,h,b,'A4 · cabeçalho leve, área de escrita livre e rodapé institucional.',(210,297))
w,h=1440,720
b=rect(0,0,w,h,CREAM)+rect(0,0,220,h,WINE)+f'<g opacity=".16">'+nested(monogram(PINK),-55,135,330,390)+'</g>'
b+=nested(logo_dark,285,60,370,204)+rect(285,300,145,2,WINE)+text(285,355,'DESTINATÁRIO',12,WINE,'Arial',spacing=3)
for y in [403,442,481]:b+=rect(285,y,670,1,PINK)
b+=f'<path d="M1020 720C1040 440 1330 540 1440 270V720Z" fill="{PINK}"/>'
b+=text(285,605,'REMETENTE · VÉRTICE MODA FEMININA',12,WINE,'Arial',spacing=1.4)+text(285,650,'Elegância que valoriza quem você é.',17,WINE,'Arial')
save('envelope','Envelope comercial','Papelaria',w,h,b,'220 × 110 mm · face externa. Versão institucional; área do destinatário livre. Aplicar à faca da gráfica.',(220,110))
for slug,title,desc,body in [
 ('grafismo-gesto','Grafismo 01 · gesto','Recorte expressivo do monograma. Para cantos, fundos e assinaturas.',rect(0,0,1200,900,PINK)+gesture(1200,900,WINE,.95)),
 ('grafismo-trama','Grafismo 02 · trama V','Módulo geométrico em V. Uma textura contínua para papelaria e embalagens.',rect(0,0,1200,900,WINE)+lattice(1200,900,PINK,.55)),
 ('grafismo-seda','Grafismo 03 · movimento','Curvas paralelas inspiradas no caimento dos tecidos do manual.',rect(0,0,1200,900,CREAM)+ribbons(1200,900,WINE,.75))]:
 save(slug,title,'Grafismos',1200,900,body,desc)
# Adhesives: three distinct proportions, sharing the same visual vocabulary.
b=f'<circle cx="450" cy="450" r="450" fill="{WINE}"/>'
b+=f'<circle cx="450" cy="450" r="416" fill="none" stroke="{PINK}" stroke-width="1"/>'
b+=nested(monogram(PINK),245,175,410,355)+text(450,650,'VÉRTICE',38,PINK,'Georgia','middle',8)+text(450,702,'MODA FEMININA',15,PINK,'Arial','middle',4)
save('adesivo-circular','Adesivo circular','Adesivos',900,900,b,'Ø 60 mm · selo com monograma e assinatura. Fundo externo transparente.',(60,60))
b=rect(0,0,1440,480,PINK)+rect(1100,0,340,480,WINE)+f'<g opacity=".28">'+nested(monogram(CREAM),1080,40,310,380)+'</g>'
b+=nested(logo_dark,65,50,530,292)+text(72,403,'UM DETALHE. TODA A SUA ESSÊNCIA.',16,WINE,'Arial',spacing=2)
save('adesivo-horizontal','Adesivo horizontal','Adesivos',1440,480,b,'120 × 40 mm · fechamento de embalagens com assinatura e recorte caligráfico.',(120,40))
b=rect(0,0,660,1100,CREAM)+rect(0,0,660,425,WINE)+lattice(660,425,PINK,.2)+nested(monogram(PINK),165,75,330,290)
b+=nested(logo_dark,110,485,440,242)+text(330,840,'Feito de detalhes.',32,WINE,'Georgia','middle')+text(330,909,'FEITO PARA VOCÊ.',13,WINE,'Arial','middle',3)+rect(75,1000,510,2,WINE)
save('adesivo-vertical','Adesivo vertical','Adesivos',660,1100,b,'45 × 75 mm · selo alongado com contraste de cores e dois momentos de leitura.',(45,75))
# The photograph is generated for this brand; its file is embedded in the editable SVG.
photo='data:image/png;base64,'+base64.b64encode((A/'editorial-vertice.png').read_bytes()).decode()
b=rect(0,0,1920,1000,CREAM)+f'<image x="530" y="0" width="1500" height="1000" xlink:href="{photo}"/>'
b+=f'<path d="M0 0H1050C1040 340 720 600 770 1000H0Z" fill="{CREAM}"/>'
b+=f'<g transform="translate(480 -180) rotate(30)">'+ribbons(650,550,PINK,.65)+'</g>'
b+=nested(logo_dark,105,55,390,215)+text(115,440,'Sua essência,',82)+text(115,535,'em cada',82)+text(115,630,'movimento.',82)
b+=rect(120,696,90,3,WINE)+text(120,750,'Elegância que valoriza quem você é.',23,WINE,'Arial')
b+=text(120,910,'VÉRTICE / MODA FEMININA',14,WINE,'Arial',spacing=3)
b+=rect(1780,0,140,1000,WINE)+f'<g opacity=".5">'+nested(monogram(PINK),1750,748,200,220)+'</g>'
save('banner-editorial','Banner editorial','Banner',1920,1000,b,'Composição fotográfica com modelo, curvas de seda, recorte orgânico e hierarquia editorial. 1920 × 1000 px.')
# Combined business card PDF: both sides in one download, kept with individual editable files.
card=fitz.open()
for slug in ['cartao-frente','cartao-verso']:
 with fitz.open(D/f'{slug}.pdf') as d:card.insert_pdf(d)
card.save(D/'cartao-visita-frente-verso.pdf')
for item in items:
 with zipfile.ZipFile(D/f"{item['slug']}.zip",'w',zipfile.ZIP_DEFLATED) as z:
  for ext in ['svg','png','pdf']:z.write(D/f"{item['slug']}.{ext}",f"{item['slug']}.{ext}")
# Word letterhead: full-page brand art behind editable document text.
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
bg=re.sub(r'<text\b[^>]*>.*?</text>','',(D/'papel-timbrado.svg').read_text(),flags=re.S)
bgdoc=fitz.open(stream=bg.encode(),filetype='svg')
bgdoc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(A/'papel-timbrado-fundo.png')
word=Document();sec=word.sections[0]
sec.page_width=Mm(210);sec.page_height=Mm(297)
sec.top_margin=Mm(65);sec.bottom_margin=Mm(34);sec.left_margin=Mm(18);sec.right_margin=Mm(18);sec.header_distance=Mm(0)
run=sec.header.paragraphs[0].add_run();pic=run.add_picture(str(A/'papel-timbrado-fundo.png'),width=Mm(210),height=Mm(297))
inline=pic._inline;anchor=OxmlElement('wp:anchor')
for k,v in {'distT':'0','distB':'0','distL':'0','distR':'0','simplePos':'0','relativeHeight':'0','behindDoc':'1','locked':'0','layoutInCell':'1','allowOverlap':'1'}.items():anchor.set(k,v)
simple=OxmlElement('wp:simplePos');simple.set('x','0');simple.set('y','0');anchor.append(simple)
for axis in ['H','V']:
 pos=OxmlElement('wp:position'+axis);pos.set('relativeFrom','page');off=OxmlElement('wp:posOffset');off.text='0';pos.append(off);anchor.append(pos)
anchor.append(inline.find(qn('wp:extent')))
anchor.append(OxmlElement('wp:wrapNone'))
for tag in ['wp:docPr','wp:cNvGraphicFramePr','a:graphic']:
 node=inline.find(qn(tag))
 if node is not None:anchor.append(node)
inline.getparent().replace(inline,anchor)
style=word.styles['Normal'];style.font.name='Arial';style.font.size=Pt(11);style.font.color.rgb=RGBColor.from_string('692234')
word.add_paragraph('')
footer=sec.footer.paragraphs[0];footer.text='VÉRTICE • MODA FEMININA\nElegância que valoriza quem você é.'
for r in footer.runs:r.font.size=Pt(8)
word.save(D/'papel-timbrado.docx')
with zipfile.ZipFile(D/'papel-timbrado.zip','a',zipfile.ZIP_DEFLATED) as z:z.write(D/'papel-timbrado.docx','papel-timbrado.docx')
# Dedicated card kit contains both sides.
with zipfile.ZipFile(D/'cartao-visita.zip','w',zipfile.ZIP_DEFLATED) as z:
 for slug in ['cartao-frente','cartao-verso']:
  for ext in ['svg','png','pdf']:z.write(D/f'{slug}.{ext}',f'{slug}.{ext}')
 z.write(D/'cartao-visita-frente-verso.pdf','cartao-visita-frente-verso.pdf')
notes='''VÉRTICE — IDENTIDADE E PAPELARIA / REVISÃO 05 — GRAFIA CORRIGIDA

Escopo: três marcas aprovadas, cartão (frente e verso), papel timbrado, envelope, três grafismos, três adesivos e banner editorial. Materiais de redes sociais, tag e embalagem da versão anterior foram retirados desta entrega.

Cores: vinho #692234, rosa #EED9DA e marfim de apoio #FAF6EF. Logotipo revisado em curvas: Vértice e MODA FEMININA. Monograma preservado. O manual especifica Citadel Script e Wichittra; as fontes completas e suas licenças não foram fornecidas. Textos de apoio em Georgia/Arial.

Versão pública institucional, sem dados pessoais ou campos de contato pendentes. Área de escrita do timbrado e destinatário do envelope permanecem livres para uso. Papel timbrado também inclui DOCX com texto editável e arte de fundo. SVG é editável; PDF para compartilhamento e preparação de produção; PNG para visualização. O banner incorpora uma fotografia gerada com IA para esta composição, não representa uma coleção real da loja.

Os PDFs físicos têm tamanho final indicado, em RGB e sem sangria. Validar perfil de cor, sangria, margens de segurança, faca e acabamento com a gráfica. O envelope contém a face externa, não uma faca estrutural. As dimensões dos adesivos são sugestões de produção. O banner é horizontal; medida física e distância de leitura precisam ser definidas antes da impressão em grande formato.
'''
(D/'LEIA-ME.txt').write_text(notes)
import runpy
runpy.run_path(str(R/'tools'/'manual.py'),run_name='__main__')
(R/'catalog.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
# Remove only obsolete generated deliverables known from the previous version.
keep={f"{i['slug']}.{ext}" for i in items for ext in ['svg','png','pdf','zip']}
keep.update(['manual-identidade-visual-vertice.pdf','LEIA-ME.txt','cartao-visita.zip','cartao-visita-frente-verso.pdf','vertice-kit-completo.zip','papel-timbrado.docx'])
old_slugs=['post-institucional','post-novidades','post-casual','post-verao','post-outlet','story-novidades','story-institucional','story-agradecimento','destaque-novidades','destaque-colecoes','destaque-looks','destaque-cuidados','destaque-sobre','banner-site','banner-campanha','tag','adesivo','embalagem']
for slug in old_slugs:
 for ext in ['svg','png','pdf','zip']:
  f=D/f'{slug}.{ext}'
  if f.name not in keep and f.exists():f.unlink()
 if (A/f'{slug}.png').exists():(A/f'{slug}.png').unlink()
with zipfile.ZipFile(D/'vertice-kit-completo.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(D.iterdir()):
  if f.name in keep and f.suffix!='.zip':z.write(f,f.name)
print(f'{len(items)} peças: marca 3; papelaria 4 arquivos (cartão frente/verso); grafismos 3; adesivos 3; banner 1.')

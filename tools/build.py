from pathlib import Path
import fitz, re, shutil, json, zipfile, html
R=Path(__file__).resolve().parents[1]; D=R/'downloads'; A=R/'assets';D.mkdir(exist_ok=True);A.mkdir(exist_ok=True)
source=Path('/workspace/attachments/b4bb692c-b8fa-4d93-9682-46c128c8954f/Identidade Visual - Vértice - Moda Feminina (1).pdf')
p=fitz.open(source)
WINE='#692234';PINK='#EED9DA';CREAM='#FAF6EF'
s=p[8].get_svg_image(text_as_path=True)
s=re.sub(r'<path[^>]*d="M0 0H1920V1080H0Z"[^>]*/>','',s)
s=re.sub(r' clip-path="url\(#clip_[67]\)"','',s)
s=re.sub(r'width="1440" height="810" viewBox="0 0 1440 810"','width="600" height="330" viewBox="385 235 600 330"',s, count=1)
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
 pix=doc[0].get_pixmap(matrix=fitz.Matrix(min(1600/w,1600/h),min(1600/w,1600/h)));pix.save(D/f'{slug}.png')
 thumb=doc[0].get_pixmap(matrix=fitz.Matrix(min(640/w,640/h),min(640/w,640/h)));thumb.save(A/f'{slug}.png')
 items.append(dict(slug=slug,title=title,category=category,description=desc,width=w,height=h))
def base(w,h,dark=False):
 bg=WINE if dark else CREAM;fg=CREAM if dark else WINE
 return rect(0,0,w,h,bg)+f'<rect x="{w*.045}" y="{h*.04}" width="{w*.91}" height="{h*.92}" fill="none" stroke="{PINK if dark else WINE}" stroke-opacity=".35"/>',fg
save('logotipo-vinho','Logotipo · vinho','Marca',1200,660,nested(logo_dark,0,0,1200,660),'Marca original do manual, com fundo transparente.')
save('logotipo-claro','Logotipo · claro','Marca',1200,660,nested(logo_light,0,0,1200,660),'Versão clara com fundo transparente, para superfícies escuras.')
save('monograma','Monograma V','Marca',800,800,nested(monogram(WINE),80,80,640,640),'Símbolo original extraído da construção do logotipo.')
for slug,title,lines,sub,dark in [
 ('post-institucional','Post institucional',['Elegância que valoriza','quem você é.'],'VÉRTICE • MODA FEMININA',False),
 ('post-novidades','Post · novidades',['Novos encontros.','Novas possibilidades.'],'CONHEÇA AS NOVIDADES',True),
 ('post-casual','Post · casual',['Leveza para','todos os dias.'],'SEU ESTILO, SEU RITMO',False),
 ('post-verao','Post · verão',['Vista a leveza.','Viva o verão.'],'UMA ESTAÇÃO DE POSSIBILIDADES',False),
 ('post-outlet','Post · outlet',['Seu próximo favorito','está aqui.'],'DESCUBRA A SELEÇÃO OUTLET',True)]:
 b,fg=base(1080,1080,dark);b+=nested(logo_light if dark else logo_dark,355,100,370,205)
 b+=nested(monogram(PINK),710,650,330,300)
 for i,line in enumerate(lines):b+=text(100,505+i*95,line,68,fg)
 b+=text(102,790,sub,19,fg,'Arial',spacing=3)
 save(slug,title,'Redes sociais',1080,1080,b,'Arte original para feed • 1080 × 1080 px.')
for slug,title,lines,sub,dark in [('story-novidades','Story · novidades',['Um novo olhar','para o seu estilo.'],'DESCUBRA A VÉRTICE',True),('story-institucional','Story institucional',['Você no centro.','Seu estilo em','cada detalhe.'],'ELEGÂNCIA QUE VALORIZA QUEM VOCÊ É.',False),('story-agradecimento','Story · agradecimento',['Obrigada por','escolher a Vértice.'],'É UM PRAZER FAZER PARTE DA SUA HISTÓRIA.',False)]:
 b,fg=base(1080,1920,dark);b+=nested(logo_light if dark else logo_dark,300,220,480,264)
 for i,line in enumerate(lines):b+=text(100,900+i*115,line,80,fg)
 b+=text(100,1450,sub,18,fg,'Arial',spacing=2)
 save(slug,title,'Redes sociais',1080,1920,b,'Arte vertical • 1080 × 1920 px; conteúdo centralizado para stories.')
for slug,label in [('novidades','Novidades'),('colecoes','Coleções'),('looks','Looks'),('cuidados','Cuidados'),('sobre','Sobre')]:
 b=rect(0,0,1080,1080,PINK)+f'<circle cx="540" cy="540" r="430" fill="none" stroke="{WINE}" stroke-width="2"/>'
 b+=nested(monogram(WINE),340,250,400,360)+text(540,740,label.upper(),32,WINE,'Arial','middle',5)
 save('destaque-'+slug,'Destaque · '+label,'Redes sociais',1080,1080,b,'Capa de destaque com área central segura para recorte circular.')
for slug,title,w,h,headline in [('banner-site','Banner para site',1920,800,'Elegância que valoriza quem você é.'),('banner-campanha','Banner de campanha',1600,600,'Seu estilo. Sua essência.')]:
 b,fg=base(w,h,True);b+=nested(logo_light,80,80,460,253)+text(90,h*.65,headline,59,fg)+text(93,h*.80,'VÉRTICE • MODA FEMININA',20,fg,'Arial',spacing=5)+nested(monogram(PINK),w-530,110,410,400)
 save(slug,title,'Digital',w,h,b,'Banner editorial para uso digital, sem ofertas ou dados fictícios.')
b,fg=base(900,500,True);b+=nested(logo_light,200,90,500,275)
save('cartao-frente','Cartão · frente','Papelaria',900,500,b,'Frente institucional • 90 × 50 mm; sem sangria.',(90,50))
b,fg=base(900,500);b+=text(70,170,'Elegância que valoriza',40)+text(70,225,'quem você é.',40)+text(70,380,'VÉRTICE • MODA FEMININA',18,WINE,'Arial',spacing=3)
save('cartao-verso','Cartão · verso','Papelaria',900,500,b,'Verso institucional • 90 × 50 mm; sem contatos inventados e sem sangria.',(90,50))
b,fg=base(500,900);b+=nested(logo_dark,65,170,370,205)+text(250,600,'Feita para acompanhar',25,WINE,'Georgia','middle')+text(250,640,'a sua essência.',25,WINE,'Georgia','middle')
save('tag','Tag de produto','Papelaria',500,900,b,'Arte de tag • 50 × 90 mm; posicionamento do furo a definir com a gráfica.',(50,90))
b=rect(0,0,600,600,CREAM)+f'<circle cx="300" cy="300" r="285" fill="{WINE}"/>'+nested(monogram(PINK),145,130,310,300)
save('adesivo','Adesivo circular','Embalagem',600,600,b,'Arte para adesivo circular de 60 mm; corte indicado pela borda externa.',(60,60))
b,fg=base(1200,800);b+=nested(logo_dark,330,150,540,297)+text(600,590,'Cada detalhe, pensado para você.',32,WINE,'Georgia','middle')
save('embalagem','Arte institucional para embalagem','Embalagem',1200,800,b,'Painel de marca • 240 × 160 mm. Aplicar na faca fornecida pelo fabricante.',(240,160))
shutil.copy2(source,D/'manual-identidade-visual-vertice.pdf')
# Original manual cover is a preview, clearly separate from newly created artwork.
p[0].get_pixmap(matrix=fitz.Matrix(.55,.55)).save(A/'manual.png')
(D/'LEIA-ME.txt').write_text('VÉRTICE — KIT DE IDENTIDADE VISUAL\n\nArtes criadas a partir das aplicações do manual enviado. A conversa anterior não estava acessível; o escopo segue o PDF, não uma lista contratual confirmada.\n\nSVG: edição em ferramentas compatíveis; PNG: uso digital; PDF: compartilhamento e impressão. O logotipo e o monograma preservam os traçados incorporados no PDF original. Cores: vinho #692234 e rosa #EED9DA.\n\nO manual indica Citadel Script e Wichittra. Arquivos completos e licenças das fontes não foram fornecidos. O logotipo foi preservado como curvas, e os novos textos usam Georgia/Arial como fontes de apoio. Não são distribuídos arquivos de fontes.\n\nPapelaria: os PDFs têm as dimensões indicadas, em RGB, sem sangria e sem conversão CMYK certificada. A gráfica deve validar sangria, corte, perfil de cor e materiais. Embalagem é arte de aplicação, não projeto estrutural nem faca.\n\nNão foram inventados preços, descontos, telefone, endereço ou perfis sociais. Artes de campanha precisam ser usadas quando corresponderem à coleção vigente.\n')
(R/'catalog.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
with zipfile.ZipFile(D/'vertice-kit-completo.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(D.iterdir()):
  if f.suffix in ['.svg','.png','.pdf','.txt']:z.write(f,f.name)
print(f'{len(items)} entregáveis criados + manual; {len(list(D.iterdir()))} arquivos.')

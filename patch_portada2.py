# Parche 2: sube "Nuestros menús" justo debajo de la presentación y añade el botón "Ver menús y precios".
# No hace nada si la portada ya lo tiene.
import sys
f=sys.argv[1]+'/index.html'
h=open(f,encoding='utf-8').read()
if 'id="menus"' in h or 'menus-bf' not in h: print('nada que hacer'); sys.exit(0)
i=h.index('  <div class="sec menus-bf">')
j=h.index('  <div class="sec"><div class="wrap">\n    <div class="sec-h"><div class="eyebrow">Especiales de la casa')
blk=h[i:j].replace('<div class="sec menus-bf">','<div class="sec menus-bf" id="menus">',1)
h=h[:i]+h[j:]
k=h.index('  <div class="band"><div class="wrap">\n    <div><small>Horario</small>')
h=h[:k]+blk+h[k:]
o='<div class="ctas"><a class="btn gold" href="/carta/">Ver la carta</a><a class="btn ghost" href="/reservas/">Reservar mesa</a></div>'
assert h.count(o)==1
h=h.replace(o,'<div class="ctas"><a class="btn gold" href="#menus">Ver menús y precios</a><a class="btn ghost" href="/reservas/">Reservar mesa</a><a class="btn ghost" href="/carta/">Ver la carta</a></div>',1)
h=h.replace('.menus-bf{background:var(--paper);border-bottom:1px solid var(--line)}','.menus-bf{background:var(--paper);border-bottom:1px solid var(--line);padding-block:40px;scroll-margin-top:80px}',1)
open(f,'w',encoding='utf-8').write(h); print('parche 2 aplicado')

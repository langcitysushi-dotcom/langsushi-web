# Mejoras 05/11: portada en móvil (foto + precios + noviembre arriba), reseñas de Google,
# títulos más cortos y una fuente menos (Lora → Bitter). No hace nada si ya está aplicado.
import os, sys

HPRICE = ('<div class="hprice"><span><b>17,95 €</b> buffet libre</span>'
          '<span><b>15,95 €</b> menú del día</span></div>')

CSS = ('.hprice{display:flex;flex-wrap:wrap;gap:8px 10px;margin:0 0 18px}'
       '.hprice span{border:1px solid rgba(201,154,74,.55);border-radius:999px;padding:6px 14px;font-size:14px;color:var(--on-dark)}'
       '.hprice b{font-family:var(--f-display);color:var(--gold-on-dark);font-size:17px;margin-right:2px}'
       '.resenas .rhead{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;margin-bottom:22px}'
       '.rnote{display:flex;align-items:center;gap:12px}'
       '.rnote b{font-family:var(--f-display);font-size:44px;line-height:1;color:var(--ink)}'
       '.rnote .rs{color:var(--gold);font-size:20px;letter-spacing:2px;display:block}'
       '.rnote small{color:var(--muted);font-size:14px}'
       '.rgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}'
       '.rev{margin:0;border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--paper);display:flex;flex-direction:column;gap:10px}'
       '.rev .rs{color:var(--gold);letter-spacing:1px;font-size:14px}'
       '.rev p{margin:0;font-size:15px;line-height:1.5}'
       '.rev cite{font-style:normal;font-size:13px;color:var(--muted);margin-top:auto}'
       '@media (max-width:980px){.rgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '@media (max-width:640px){'
       '.hero .wrap{padding-block:18px 32px;gap:18px}'
       '.hero .hlogo{display:none}'
       '.hero .wrap>div:first-child{display:flex;flex-direction:column;align-items:flex-start}'
       '.hero .eyebrow{order:1}.hero .tag{order:2;margin-top:8px}.hero .hprice{order:3}'
       '.hero .promo-nov{order:4;margin:0 0 16px}.hero .wrap>div:first-child>p{order:5}'
       '.hero .ctas{order:6}.hero .promo:not(.promo-nov){order:7}'
       '.hero .collage{order:-1;aspect-ratio:auto;grid-template-columns:2fr 1fr 1fr;grid-template-rows:none;height:42vw;max-height:240px;gap:8px}'
       '.hero .collage img:first-child{grid-row:auto}'
       '.rgrid{grid-template-columns:1fr}.rnote b{font-size:38px}}')

REVIEWS = '''  <div class="sec resenas" id="resenas"><div class="wrap">
    <div class="rhead"><div class="rnote"><b>4,8</b><div><span class="rs">★★★★★</span><small>Más de 400 reseñas en Google</small></div></div><a class="btn ghost" href="https://maps.google.com/?cid=9612486309576316227" target="_blank" rel="noopener">Ver todas las reseñas</a></div>
    <div class="rgrid">
      <blockquote class="rev"><span class="rs">★★★★★</span><p>“El mejor buffet de sushi que he probado en Madrid. Nigiris y makis de calidad, cantidad de arroz correcta y de pescado más que generosa en cada pieza de sushi.”</p><cite>Stephanie B. · Google</cite></blockquote>
      <blockquote class="rev"><span class="rs">★★★★★</span><p>“Calidad del salmón, atún, pez mantequilla… impresionante. […] Creaciones espectaculares y deliciosas. 100% recomendable.”</p><cite>Viktor O. · Google</cite></blockquote>
      <blockquote class="rev"><span class="rs">★★★★★</span><p>“[…] ha sido todo un acierto, atención increíble, el ambiente super bien y la calidad de la comida sin palabras. Sin duda volveremos.”</p><cite>María G. · Google</cite></blockquote>
      <blockquote class="rev"><span class="rs">★★★★★</span><p>“Reciente apertura por el barrio, con un menú buffet con sushi de una calidad muy aceptable. Merece la pena!”</p><cite>Blanca · Google</cite></blockquote>
    </div>
  </div></div>
'''

R = [
    # títulos (Google corta a ~60 caracteres)
    ('Restaurante Lang City · Sushi y buffet libre japonés junto a Plaza de España', 'Lang City · Sushi y buffet libre junto a Plaza de España'),
    ('Buffet libre japonés en Madrid desde 17,95 € · Lang City, Plaza de España', 'Buffet libre japonés en Madrid desde 17,95 € · Lang City'),
    ('Sushi para grupos y cumpleaños en Madrid · Buffet libre junto a Plaza de España · Lang City', 'Grupos y cumpleaños con buffet de sushi en Madrid · Lang City'),
    ('Sushi antes o después del cine en Princesa · Buffet libre a 5 minutos · Lang City', 'Sushi junto a los cines de Princesa, Madrid · Lang City'),
    # una fuente menos
    ('family=Bitter:wght@400;700&family=Great+Vibes&family=Lora:wght@700&family=Ubuntu:wght@400;500;700', 'family=Bitter:wght@400;700&family=Great+Vibes&family=Ubuntu:wght@400;500;700'),
    ('--f-menu:"Lora",Georgia,serif;', '--f-menu:"Bitter",Georgia,serif;'),
    # portada: precios bajo el título
    ('junto a Plaza de España</h1>\n        <p>Sushi, sashimi', 'junto a Plaza de España</h1>\n        ' + HPRICE + '\n        <p>Sushi, sashimi'),
    # estilos nuevos
    ('.promo{margin-top:26px', CSS + '.promo{margin-top:26px'),
    # reseñas antes de la franja de horario (solo portada)
    ('  <div class="band"><div class="wrap">', REVIEWS + '  <div class="band"><div class="wrap">'),
    # la primera foto ahora se ve arriba en el móvil: que no espere a cargar
    ('9A.webp" alt="" width="900" height="675" loading="lazy" decoding="async">', '9A.webp" alt="" width="900" height="675" decoding="async">'),
]
CHECK = {  # texto que indica que ese cambio ya está hecho
    6: 'class="hprice"', 7: '.hprice{', 8: 'class="sec resenas"',
}

def patch_text(t):
    for i, (a, b) in enumerate(R):
        done = CHECK.get(i)
        if (done and done in t) or (not done and a not in t):
            continue
        if i == 8:
            t = t.replace(a, b, 1)
        else:
            t = t.replace(a, b)
    return t

def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt'))]
        for p in files:
            if '/admin/' in p or os.path.basename(p) == 'admin.html':
                continue
            t = open(p, encoding='utf-8').read(); o = patch_text(t)
            if o != t:
                open(p, 'w', encoding='utf-8').write(o); n += 1
    print('patch_mejoras: archivos cambiados', n)

if __name__ == '__main__':
    main(sys.argv[1:])

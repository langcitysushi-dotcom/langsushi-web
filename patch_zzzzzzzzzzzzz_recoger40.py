# Pedidos para recoger desde la web: 40 % de descuento (antes 30 %). Desde el 25/11/2026.
# 1) Cambia el calculo del carrito y todos los textos (ES/EN/ZH, schema, llms.txt).
# 2) Añade "Pedir −40%" a la barra fija del movil (.mbar) en todas las paginas que la tienen.
# 3) Crea la pagina /sushi-para-llevar/ (a partir de /sushi-plaza-de-espana/) y la añade al sitemap.
# Va despues de patch_..._descuento30.py y patch_..._caducados.py. Nunca rompe la publicacion.
import os, re, sys

R = [
    ('const PICKUP_DISCOUNT = 0.30;', 'const PICKUP_DISCOUNT = 0.40;'),
    ('const PICKUP_DISCOUNT=0.30;', 'const PICKUP_DISCOUNT=0.40;'),
    ('Recoger (−30%)', 'Recoger (−40%)'),
    ('Descuento recogida 30%', 'Descuento recogida 40%'),
    ('<b>−30%</b>', '<b>−40%</b>'),
    ('30 % de descuento', '40 % de descuento'),
    ('with 30% off', 'with 40% off'),
    ('30% off', '40% off'),
    ('七折优惠（立减30%）', '六折优惠（立减40%）'),
]
CHECK = re.compile(r'30 ?% de descuento|−30%|recogida 30|PICKUP_DISCOUNT ?= ?0\.3|30% off|七折')

MBAR_TXT = {'en': 'Order −40%', 'zh': '自取六折'}
MBAR_CSS = ('<style id="mbar4">@media (max-width:640px){.mbar.m4{grid-template-columns:repeat(4,1fr);gap:6px}'
            '.mbar.m4 a{font-size:12.5px;padding:10px 2px;white-space:nowrap}'
            '.mbar a.pedir{background:#c8102e;color:#fff;border-color:#c8102e}}</style>')


def lang_of(p):
    q = p.replace('\\', '/')
    if '/en/' in q: return 'en'
    if '/zh/' in q: return 'zh'
    return 'es'


MBAR_NEW = {
    'es': ('Acciones rápidas', 'Llamar', 'Cómo llegar', 'Reservar'),
    'en': ('Quick actions', 'Call', 'Directions', 'Book'),
    'zh': ('快捷操作', '电话', '路线', '订座'),
}


def mbar(t, p):
    if 'class="pedir"' in t:
        return t
    if 'class="mbar"' not in t:
        # Paginas con el estilo .mbar pero sin la barra: se añade entera
        if '.mbar{' not in t or '</body>' not in t:
            return t
        lab, call, go, book = MBAR_NEW[lang_of(p)]
        nav = ('<nav class="mbar" aria-label="%s"><a href="tel:+34919414881">%s</a>'
               '<a target="_blank" rel="noopener" href="https://maps.google.com/?cid=9612486309576316227">%s</a>'
               '<a href="/reservas/" class="on">%s</a></nav>') % (lab, call, go, book)
        t = t.replace('</body>', nav + '</body>', 1)
    txt = MBAR_TXT.get(lang_of(p), 'Pedir −40%')
    t = t.replace('<nav class="mbar"', '<nav class="mbar m4"', 1)
    t = re.sub(r'(<nav class="mbar m4"[^>]*>.*?)(</nav>)',
               lambda m: m.group(1) + '<a href="/carta/" class="pedir">%s</a>' % txt + m.group(2), t, count=1, flags=re.S)
    return t.replace('</head>', MBAR_CSS + '</head>', 1)


TITLE = 'Sushi para llevar en Plaza de España · 40 % de descuento · Lang City'
DESC = ('Pide sushi para llevar en Plaza de España: elige en la carta online de 139 platos, '
        'recoge a la hora que quieras en C. de Ventura Rodríguez 5 y paga un 40 % menos.')
MAIN = '''<main><section class="hero"><div class="wrap"><div><div class="eyebrow">Sushi para llevar · Plaza de España</div> <h1 class="tag">Sushi para llevar con un 40 % de descuento</h1> <p>Elige tus platos en nuestra <a href="/carta/">carta online</a>, indica la hora y recógelo recién hecho en <b>C. de Ventura Rodríguez 5</b> (entrada por Plaza de los Cubos), a 3–4 minutos de Plaza de España. Todos los pedidos para recoger hechos desde la web tienen un <b>40 % de descuento</b>.</p> <div class="ctas"><a class="btn gold" href="/carta/">Pedir para recoger −40%</a><a class="btn ghost" href="tel:+34919414881">Llamar</a></div></div> <div class="collage" aria-hidden="true"><img src="/img/C5.webp" alt="" width="900" height="675"><img src="/img/t/9A.webp" alt="" width="480" height="360"><img src="/img/t/22B.webp" alt="" width="480" height="360"></div></div></section> <div class="band"><div class="wrap"><div><small>Descuento</small><span>40 % en pedidos para recoger</span></div><div><small>Carta</small><span>139 platos con foto, precio y alérgenos</span></div><div><small>Recogida</small><span>Todos los días · 12:00–17:00 y 19:30–24:00</span></div></div></div> <div class="sec"><div class="wrap seo-grid"><div><h2 class="h2s">Cómo pedir sushi para llevar</h2> <ol class="como"><li><b>Elige</b> en la <a href="/carta/">carta</a>: nigiris, makis, uramakis, rolls especiales, sashimi, carpaccios, bandejas para compartir, dim sum, wok y postres.</li><li><b>Marca «Recoger (−40%)»</b> en tu pedido y elige la hora de recogida.</li><li><b>Pásate por el restaurante</b> a esa hora: tu pedido estará preparado al momento.</li></ol> <h2 class="h2s">Dónde recogerlo</h2> <p>Lang City · C. de Ventura Rodríguez 5, 28008 Madrid, con entrada por C. de Santa María Micaela 6 (Plaza de los Cubos). Metro Ventura Rodríguez (L3) y Plaza de España (L2, L3, L10). Si tienes dudas, llámanos al <a href="tel:+34919414881">919 41 48 81</a>.</p> <h2 class="h2s">Preguntas frecuentes</h2> <details class="faq"><summary>¿Cuánto descuento tienen los pedidos para recoger?</summary><p>Un 40 % sobre el precio de la carta en todos los pedidos para recoger hechos desde la web.</p></details> <details class="faq"><summary>¿Cuánto tarda mi pedido?</summary><p>Lo preparamos para la hora que elijas al pedir. En horas punta te recomendamos pedir con antelación.</p></details> <details class="faq"><summary>¿Puedo ver los alérgenos?</summary><p>Sí: en la carta cada plato muestra sus alérgenos y puedes ocultar los que contengan los tuyos.</p></details> <p><a class="btn gold" href="/carta/">Ver la carta y pedir</a></p></div></div></div></main>'''
FAQ_LD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
          '{"@type":"Question","name":"¿Cuánto descuento tienen los pedidos para recoger?","acceptedAnswer":{"@type":"Answer","text":"Un 40 % sobre el precio de la carta en todos los pedidos para recoger hechos desde la web."}},'
          '{"@type":"Question","name":"¿Dónde se recoge el pedido?","acceptedAnswer":{"@type":"Answer","text":"En Lang City, C. de Ventura Rodríguez 5, 28008 Madrid (entrada por Plaza de los Cubos), junto a Plaza de España."}}]}</script>')


def pagina_llevar(site):
    src = os.path.join(site, 'sushi-plaza-de-espana', 'index.html')
    dst_dir = os.path.join(site, 'sushi-para-llevar')
    if not os.path.isfile(src) or os.path.exists(os.path.join(dst_dir, 'index.html')):
        return 0
    t = open(src, encoding='utf-8').read()
    if t.count('<main') != 1 or t.count('</main>') != 1:
        return 0
    old_t = re.search(r'<title>(.*?)</title>', t).group(1)
    old_d = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
    t = t.replace(old_t, TITLE).replace(old_d, DESC)
    t = t.replace('https://langsushi.es/sushi-plaza-de-espana/', 'https://langsushi.es/sushi-para-llevar/')
    t = t[:t.find('<main')] + MAIN + t[t.find('</main>') + len('</main>'):]
    # Quita los datos estructurados FAQ/Breadcrumb de la pagina de origen y pone los propios
    t = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*"(?:FAQPage|BreadcrumbList)"(?:(?!</script>).)*</script>', '', t, flags=re.S)
    t = t.replace('</head>', FAQ_LD + '</head>', 1)
    os.makedirs(dst_dir, exist_ok=True)
    with open(os.path.join(dst_dir, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    sm = os.path.join(site, 'sitemap.xml')
    if os.path.isfile(sm):
        s = open(sm, encoding='utf-8').read()
        if 'sushi-para-llevar' not in s and '</urlset>' in s:
            s = s.replace('</urlset>', '<url><loc>https://langsushi.es/sushi-para-llevar/</loc></url></urlset>')
            with open(sm, 'w', encoding='utf-8', newline='\n') as f:
                f.write(s)
    return 1


def main(args):
    done, left = 0, []
    for a in args:
        if os.path.isdir(a):
            done += pagina_llevar(a)
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt', '.js', '.json'))]
        for p in files:
            if '/admin/' in p.replace('\\', '/'):
                continue
            try:
                t = open(p, encoding='utf-8').read()
            except Exception:
                continue
            n = t
            for x, y in R:
                n = n.replace(x, y)
            if p.endswith('.html'):
                n = mbar(n, p)
            if n != t:
                with open(p, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(n)
                done += 1
            for m in CHECK.finditer(n):
                left.append('%s: ...%s...' % (p, n[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')))
    print('patch_recoger40: archivos cambiados', done)
    for l in left[:20]:
        print('  queda:', l)


if __name__ == '__main__':
    try:
        main(sys.argv[1:] or ['site'])
    except Exception as e:
        print('patch_recoger40: error (se ignora)', e)

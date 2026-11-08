# Página "Sushi en Plaza de España" (08/11/2026): crea /sushi-plaza-de-espana/ a partir de la página de los cines
# (misma cabecera, estilos y pie), la añade al sitemap y a llms.txt y la enlaza desde el pie de todas las páginas
# y desde la portada. No hace nada si ya está aplicado. Nunca rompe la publicación: si algo falla, lo avisa y sigue.
import json, os, re, sys

SLUG = 'sushi-plaza-de-espana'
URL = 'https://langsushi.es/' + SLUG + '/'
TITLE = 'Sushi en Plaza de España · Buffet libre japonés · Lang City'
DESC = ('Restaurante de sushi en Plaza de España: buffet libre japonés desde 17,95 € y menú del día por 15,95 €. '
        'C. de Ventura Rodríguez 5, con entrada por Plaza de los Cubos. Reserva online.')

FAQ = [
    ('¿Dónde comer sushi cerca de Plaza de España?',
     'En Lang City, C. de Ventura Rodríguez 5, a unos 3–4 minutos andando de Plaza de España. La entrada está en C. de Santa María Micaela 6, en Plaza de los Cubos.'),
    ('¿Cuánto cuesta el buffet libre de sushi?',
     '17,95 € a mediodía de martes a viernes, 23,95 € por la noche de martes a jueves y 27,95 € viernes noche, fines de semana, festivos y vísperas. Niños de 100 a 130 cm, 11,95 €; menores de 3 años, gratis. Bebida y postre aparte.'),
    ('¿Tenéis menú del día?',
     'Sí, por 15,95 € con cuatro platos a elegir, todos los días que abrimos (de martes a domingo).'),
    ('¿Qué metro me deja más cerca?',
     'Ventura Rodríguez (línea 3) es la parada más cercana. Plaza de España (líneas 2, 3 y 10) está a unos 5 minutos andando.'),
    ('¿Qué horario tenéis?',
     'De martes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. Los lunes cerramos por descanso.'),
    ('¿Se puede reservar mesa?',
     'Sí, online en langsushi.es/reservas: eliges personas, día y hora y recibes la confirmación por email. También puedes llamarnos.'),
    ('¿Hay platos vegetales y información de alérgenos?',
     'Sí. En la carta online puedes filtrar los platos vegetales y ver los alérgenos de cada plato.'),
]

MAIN = '''<main><section class="hero"><div class="wrap"><div><div class="eyebrow">Sushi · Buffet libre · Plaza de España</div>
<h1 class="tag">Sushi en Plaza de España</h1>
<p>Lang City es un restaurante japonés y de sushi fusión a unos 3–4 minutos andando de Plaza de España, en <b>C. de Ventura Rodríguez 5</b> (entrada por C. de Santa María Micaela 6, en Plaza de los Cubos). Buffet libre de sushi desde 17,95 €, menú del día por 15,95 € y una carta de 139 platos con fotos y precios.</p>
<div class="ctas"><a class="btn gold" href="/reservas/">Reservar mesa</a><a class="btn ghost" href="/carta/">Ver la carta</a></div></div>
<div class="collage" aria-hidden="true"><img src="/img/C5.webp" alt="" width="900" height="675"><img src="/img/t/9A.webp" alt="" width="480" height="360"><img src="/img/t/22B.webp" alt="" width="480" height="360"></div></div></section>
<div class="band"><div class="wrap"><div><small>Buffet libre</small><span>Desde 17,95 €</span></div><div><small>Menú del día</small><span>15,95 € · 4 platos a elegir</span></div><div><small>Metro</small><span>Ventura Rodríguez (L3) y Plaza de España (L2, L3, L10)</span></div></div></div>
<div class="sec"><div class="wrap seo-grid"><div><h2 class="h2s">Sushi y buffet libre japonés junto a Plaza de España</h2>
<p>Preparamos al momento nigiris, makis, uramakis y rolls especiales, sashimi, carpaccios, dim sum, tempuras, platos de wok, plancha y postres. Puedes venir a por el buffet libre (90 minutos, pides desde la tablet de tu mesa), al menú del día o pedir a la carta.</p>
<table class="bftab"><caption>Buffet libre · precio por persona, IVA incluido</caption><tbody><tr><th scope="row">Mediodía, de martes a viernes (no festivos ni vísperas)</th><td>17,95 €</td></tr><tr><th scope="row">Noche, de martes a jueves (no festivos ni vísperas)</th><td>23,95 €</td></tr><tr><th scope="row">Viernes noche, sábados, domingos, festivos y vísperas</th><td>27,95 €</td></tr><tr><th scope="row">Niños de 100 a 130 cm (cualquier turno)</th><td>11,95 €</td></tr><tr><th scope="row">Menores de 3 años</th><td>Gratis</td></tr><tr><th scope="row">Menú del día, de martes a domingo (4 platos a elegir)</th><td>15,95 €</td></tr></tbody></table>
<p>Más detalles en <a href="/buffet-libre/">buffet libre y menú del día</a> y en la <a href="/carta/">carta con fotos, precios y alérgenos</a>.</p>
<h2 class="h2s">Cómo llegar desde Plaza de España y alrededores</h2>
<ul class="como">
<li><b>Desde Plaza de España:</b> por la calle Princesa hasta la calle Ventura Rodríguez, unos 3–4 minutos andando.</li>
<li><b>Metro Ventura Rodríguez (L3):</b> la parada más cercana, a un par de minutos.</li>
<li><b>Metro Plaza de España (L2, L3 y L10):</b> unos 5 minutos andando.</li>
<li><b>Desde Gran Vía o Callao:</b> línea 3 hasta Ventura Rodríguez (dos paradas desde Callao) o unos 15 minutos andando.</li>
<li><b>Desde Argüelles:</b> línea 3, una parada hasta Ventura Rodríguez, o unos 10–12 minutos andando por la calle Princesa.</li>
<li><b>Desde Moncloa:</b> línea 3, dos paradas hasta Ventura Rodríguez.</li>
<li><b>Templo de Debod:</b> unos 5 minutos andando.</li>
<li><b>Plaza de los Cubos y cines Renoir Princesa:</b> la entrada está en la propia plaza. Mira el <a href="/sushi-cines-princesa/">plan cine y sushi</a>.</li>
</ul>
<h2 class="h2s">Grupos, comidas de empresa y cenas de Navidad</h2>
<p>Preparamos mesas para cumpleaños, cenas de amigos, comidas de empresa y cenas de Navidad. Cuéntanos cuántos sois en <a href="/grupos-y-cumpleanos/">grupos y cumpleaños</a>.</p>
<h2 class="h2s">Sushi para llevar</h2>
<p>Pide desde la <a href="/carta/">carta online</a>, elige la hora y recoge tu pedido en el restaurante con un 20 % de descuento.</p></div>
<div><h2 class="h2s">Preguntas frecuentes</h2>@@FAQ@@</div></div></div></main>
<style>.como{margin:6px 0 14px;padding-left:20px;line-height:1.55}.como li{margin:6px 0}</style>'''


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def build_page(tpl):
    t = tpl
    t = re.sub(r'<title>.*?</title>', '<title>' + esc(TITLE) + '</title>', t, count=1, flags=re.S)
    t = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(DESC) + '">', t, count=1)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + URL + '">', t, count=1)
    t = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="' + URL + '">', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(TITLE) + '">', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(DESC) + '">', t, count=1)
    # hreflang/alternates que apunten a la página de los cines: fuera
    t = re.sub(r'<link rel="alternate"[^>]*sushi-cines-princesa[^>]*>', '', t)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://langsushi.es/"},
        {"@type": "ListItem", "position": 2, "name": "Sushi en Plaza de España", "item": URL}]}

    def ld(m):
        body = m.group(1)
        if '"FAQPage"' in body:
            return '<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + '</script>'
        if '"BreadcrumbList"' in body:
            return '<script type="application/ld+json">' + json.dumps(bc_ld, ensure_ascii=False) + '</script>'
        return m.group(0)
    t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, t, flags=re.S)
    faq_html = ''.join('<details class="faq"><summary>' + esc(q) + '</summary><p>' + esc(a) + '</p></details>' for q, a in FAQ)
    main = MAIN.replace('@@FAQ@@', faq_html)
    i, j = t.find('<main'), t.find('</main>')
    if i < 0 or j < 0:
        raise ValueError('plantilla sin <main>')
    return t[:i] + main + t[j + len('</main>'):]


FOOT_OLD = '<p><a href="/sushi-cines-princesa/">Sushi en Plaza de los Cubos</a></p>'
FOOT_NEW = FOOT_OLD + '<p><a href="/sushi-plaza-de-espana/">Sushi en Plaza de España</a></p>'
FOOT2_OLD = '<a href="/sushi-cines-princesa/">Sushi en Plaza de los Cubos</a> · '
FOOT2_NEW = FOOT2_OLD + '<a href="/sushi-plaza-de-espana/">Sushi en Plaza de España</a> · '
HOME_OLD = 'en el centro de Madrid, a pocos pasos de Plaza de España.'
HOME_NEW = 'en el centro de Madrid, a pocos pasos de Plaza de España (<a href="/sushi-plaza-de-espana/">cómo llegar y precios</a>).'


def main(args):
    root = args[0] if args else 'site'
    tpl_p = os.path.join(root, 'sushi-cines-princesa', 'index.html')
    out_p = os.path.join(root, SLUG, 'index.html')
    if not os.path.isfile(tpl_p):
        print('patch_plazaespana: no está la plantilla, no se crea la página')
        return
    if not os.path.isfile(out_p):
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        open(out_p, 'w', encoding='utf-8').write(build_page(open(tpl_p, encoding='utf-8').read()))
        print('patch_plazaespana: página creada')
    n = 0
    for r, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.html') or '/admin' in r.replace('\\', '/'):
                continue
            p = os.path.join(r, f)
            t = open(p, encoding='utf-8').read(); o = t
            if FOOT_OLD in o and '/sushi-plaza-de-espana/">Sushi en Plaza de España' not in o:
                o = o.replace(FOOT_OLD, FOOT_NEW, 1)
            if FOOT2_OLD in o and '/sushi-plaza-de-espana/">Sushi en Plaza de España' not in o:
                o = o.replace(FOOT2_OLD, FOOT2_NEW, 1)
            if os.path.normpath(p) == os.path.normpath(os.path.join(root, 'index.html')) and 'cómo llegar y precios</a>' not in o:
                o = o.replace(HOME_OLD, HOME_NEW, 1)
            if o != t:
                open(p, 'w', encoding='utf-8').write(o); n += 1
    sm = os.path.join(root, 'sitemap.xml')
    if os.path.isfile(sm):
        t = open(sm, encoding='utf-8').read()
        if URL not in t:
            entry = '<url><loc>' + URL + '</loc><lastmod>2026-11-08</lastmod><priority>0.8</priority></url>'
            t = t.replace('<url><loc>https://langsushi.es/sushi-cines-princesa/', entry + '<url><loc>https://langsushi.es/sushi-cines-princesa/', 1) if 'sushi-cines-princesa/' in t else t.replace('</urlset>', entry + '</urlset>', 1)
            open(sm, 'w', encoding='utf-8').write(t)
    ll = os.path.join(root, 'llms.txt')
    if os.path.isfile(ll):
        t = open(ll, encoding='utf-8').read()
        if SLUG not in t:
            line = '- [Sushi en Plaza de España: precios y cómo llegar](' + URL + ')\n'
            k = t.find('- [Sushi antes o después del cine')
            t = t[:k] + line + t[k:] if k >= 0 else t + line
            open(ll, 'w', encoding='utf-8').write(t)
    print('patch_plazaespana: páginas enlazadas', n)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception as e:
        print('patch_plazaespana: ERROR (la web se publica igual):', e)

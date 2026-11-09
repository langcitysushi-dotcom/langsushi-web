# Idiomas y textos propios (09/11/2026):
#  - /en/ ampliada (precios, cómo llegar, reservas, grupos, preguntas frecuentes con schema).
#  - /zh/ nueva en chino simplificado, creada a partir de /en/ (misma cabecera y estilos).
#  - hreflang zh-Hans en portada, /en/ y sitemap; enlace "中文" en el pie.
#  - Texto propio en /reservas/ y /contacto/ para que no sean casi iguales a la portada.
# No hace nada si ya está aplicado. Nunca rompe la publicación: si algo falla, lo avisa y sigue.
import json, os, re, sys

BASE = 'https://langsushi.es/'
MAPS = 'https://maps.google.com/?cid=9612486309576316227'


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, t):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)


def faq_html(faq):
    return ''.join('<details class="faq"><summary>' + esc(q) + '</summary><p>' + esc(a) + '</p></details>' for q, a in faq)


def faq_ld(faq):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + '</script>'


def set_head(t, title, desc, url):
    t = re.sub(r'<title>.*?</title>', '<title>' + esc(title) + '</title>', t, count=1, flags=re.S)
    t = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(desc) + '">', t, count=1)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + url + '">', t, count=1)
    t = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="' + url + '">', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(title) + '">', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(desc) + '">', t, count=1)
    return t


def swap_main(t, main):
    i, j = t.find('<main'), t.find('</main>')
    if i < 0 or j < 0:
        raise ValueError('sin <main>')
    return t[:i] + main + t[j + len('</main>'):]


def add_faq_ld(t, faq):
    t = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', '', t, flags=re.S)
    k = t.find('</head>')
    return t[:k] + faq_ld(faq) + '\n' + t[k:] if k >= 0 else t


ALT_EN = '<link rel="alternate" hreflang="en" href="https://langsushi.es/en/">'
ALT_ZH = '<link rel="alternate" hreflang="zh-Hans" href="https://langsushi.es/zh/">'

# ---------------------------------------------------------------- English
EN_TITLE = 'Sushi near Plaza de España, Madrid · All-you-can-eat · Lang City'
EN_DESC = ('Japanese and fusion sushi restaurant a 3–4 minute walk from Plaza de España, Madrid. '
           'All-you-can-eat sushi from €17.95, set lunch menu €15.95, 139 dishes with photos and prices. Book online.')
EN_FAQ = [
    ('Where is Lang City?', 'Calle de Ventura Rodríguez 5, 28008 Madrid, a 3–4 minute walk from Plaza de España. The entrance is on Calle de Santa María Micaela 6, in Plaza de los Cubos.'),
    ('How much is the all-you-can-eat sushi buffet?', '€17.95 for lunch Tuesday to Friday, €23.95 for dinner Tuesday to Thursday and €27.95 on Friday evening, weekends, public holidays and the evening before them. Children 100–130 cm €11.95; under-3s free. Drinks and desserts are not included.'),
    ('Are you open on Mondays?', 'No. We are open Tuesday to Sunday, 12:00–17:00 and 19:30–24:00, and closed on Mondays.'),
    ('Can I book a table online?', 'Yes, at langsushi.es/reservas. The page is in Spanish: choose the number of people (personas), the day (día) and the time, and you will receive the confirmation by email.'),
    ('Do you have vegetarian options and allergen information?', 'Yes. On the online menu you can filter vegetarian dishes and see the allergens of every dish.'),
    ('Can I order takeaway?', 'Yes. Order from the online menu and pick it up at the restaurant with 20% off.'),
]
EN_MAIN = '''<main><section class="hero"><div class="wrap"><div><div class="eyebrow">Sushi · All-you-can-eat · Plaza de España</div><div class="hlogo"><img src="/img/logo.webp" alt="Lang City Sushi Fusión" width="1000" height="188"></div>
<h1 class="tag">Sushi &amp; Japanese restaurant near Plaza de España</h1>
<p>Lang City is a Japanese and fusion sushi restaurant in central Madrid, a 3–4 minute walk from Plaza de España, at <b>Calle de Ventura Rodríguez 5</b> (entrance on Calle de Santa María Micaela 6, in Plaza de los Cubos). All-you-can-eat sushi from €17.95, a set lunch menu for €15.95 and 139 dishes à la carte, all with photos and prices.</p>
<div class="ctas"><a class="btn gold" href="/carta/">See the menu</a><a class="btn ghost" href="/reservas/">Book a table</a></div></div>
<div class="collage" aria-hidden="true"><img src="/img/9A.webp" alt="" width="900" height="675"><img src="/img/t/22B.webp" alt="" width="480" height="360"><img src="/img/t/C5.webp" alt="" width="480" height="360"></div></div></section>
<div class="band"><div class="wrap"><div><small>Opening hours</small><span>Tuesday to Sunday · 12:00–17:00 and 19:30–24:00 · closed on Mondays</span></div><div><small>Address</small><span>Calle de Ventura Rodríguez, 5 · 28008 Madrid</span></div><div><small>Phone</small><span><a class="tel" href="tel:+34919414881">+34 919 41 48 81</a></span></div></div></div>
<div class="sec"><div class="wrap seo-grid"><div><h2 class="h2s">All-you-can-eat sushi near Plaza de España</h2>
<p>Order as much as you like from the tablet at your table for 90 minutes: nigiri, maki and uramaki rolls, special rolls, salmon and tuna sashimi, carpaccio, dim sum such as xiao long bao and shao mai, tempura, wok dishes, fried rice and noodles, grill and desserts, all made to order.</p>
<table class="bftab"><caption>Prices per person, VAT included</caption><tbody><tr><th scope="row">Buffet · lunch, Tuesday to Friday (not public holidays or the day before)</th><td>€17.95</td></tr><tr><th scope="row">Buffet · dinner, Tuesday to Thursday (not public holidays or the day before)</th><td>€23.95</td></tr><tr><th scope="row">Buffet · Friday dinner, Saturday, Sunday and public holidays</th><td>€27.95</td></tr><tr><th scope="row">Buffet · children 100–130 cm</th><td>€11.95</td></tr><tr><th scope="row">Buffet · under 3</th><td>Free</td></tr><tr><th scope="row">Set lunch menu (menú del día), Tuesday to Sunday, 4 dishes</th><td>€15.95</td></tr></tbody></table>
<p>Drinks and desserts are not included in the buffet. You can also order à la carte: the <a href="/carta/">online menu</a> shows a photo, the price and the allergens of every dish, and lets you filter vegetarian dishes.</p>
<h2 class="h2s">How to book</h2>
<p>Book on our <a href="/reservas/">booking page</a> (in Spanish): choose the number of people (<i>personas</i>), the day (<i>día</i>) and the time (<i>hora</i>), and the confirmation arrives by email. For takeaway, order from the online menu and pick it up at the restaurant with 20% off. Birthdays, groups, company lunches and Christmas dinners are welcome: see <a href="/grupos-y-cumpleanos/">groups</a>.</p>
<h2 class="h2s">Getting here</h2>
<ul class="como">
<li><b>From Plaza de España:</b> walk up Calle Princesa to Calle de Ventura Rodríguez, about 3–4 minutes.</li>
<li><b>Metro Ventura Rodríguez (line 3):</b> the closest station, a couple of minutes away.</li>
<li><b>Metro Plaza de España (lines 2, 3 and 10):</b> about 5 minutes on foot.</li>
<li><b>From Gran Vía or Callao:</b> line 3 to Ventura Rodríguez, two stops from Callao.</li>
<li><b>From Argüelles or Moncloa:</b> line 3, one or two stops to Ventura Rodríguez.</li>
<li><b>Temple of Debod:</b> about 5 minutes on foot.</li>
<li><b>Renoir Princesa cinemas:</b> right next to us, in Plaza de los Cubos.</li>
</ul>
<p><a class="btn gold" target="_blank" rel="noopener" href="''' + MAPS + '''">Directions on Google Maps</a></p></div>
<div><h2 class="h2s">Frequently asked questions</h2>''' + faq_html(EN_FAQ) + '''</div></div></div></main>
<style>.como{margin:6px 0 14px;padding-left:20px;line-height:1.55}.como li{margin:6px 0}.bftab td{white-space:nowrap}</style>'''

# ---------------------------------------------------------------- 中文
ZH_TITLE = 'Lang City · 马德里西班牙广场日料寿司自助餐'
ZH_DESC = ('马德里市中心日料寿司餐厅，距西班牙广场（Plaza de España）步行约3–4分钟。日料自助餐17,95 €起，每日套餐15,95 €，'
           '139道菜配照片和价格，可网上订座和自取。地址：C. de Ventura Rodríguez 5。')
ZH_FAQ = [
    ('餐厅在哪里？', '地址是 C. de Ventura Rodríguez 5, 28008 Madrid，距西班牙广场（Plaza de España）步行约3–4分钟。入口在 Plaza de los Cubos 广场，C. de Santa María Micaela 6。'),
    ('日料自助餐多少钱？', '周二至周五午餐17,95 €；周二至周四晚餐23,95 €；周五晚餐、周末、节假日及节日前夕27,95 €。儿童（身高100–130厘米）11,95 €，3岁以下免费。饮料和甜品另计。'),
    ('周一营业吗？', '周一休息。营业时间为周二至周日 12:00–17:00 和 19:30–24:00。'),
    ('可以网上订座吗？', '可以，在 langsushi.es/reservas 订座。页面是西班牙语：选择人数（personas）、日期（día）和时间，确认信息会发到您的邮箱。也可以打电话 919 41 48 81。'),
    ('有素食和过敏原信息吗？', '有。网上菜单可以筛选素食菜品，每道菜都标有过敏原。'),
    ('可以外带吗？', '可以。在网上菜单点餐，到店自取享八折优惠。'),
    ('原来 Castellana 的店还开吗？', '原来在 Paseo de la Castellana 的店已经关闭，现在只在 C. de Ventura Rodríguez 5 营业。'),
]
ZH_MAIN = '''<main><section class="hero"><div class="wrap"><div><div class="eyebrow">寿司 · 日料自助 · 西班牙广场</div><div class="hlogo"><img src="/img/logo.webp" alt="Lang City Sushi Fusión" width="1000" height="188"></div>
<h1 class="tag">马德里西班牙广场日料寿司自助餐</h1>
<p>Lang City 是马德里市中心的日式料理和寿司融合餐厅，地址 <b>C. de Ventura Rodríguez 5</b>（入口在 Plaza de los Cubos 广场，C. de Santa María Micaela 6），距西班牙广场（Plaza de España）步行约3–4分钟。日料自助餐17,95 €起，每日套餐15,95 €，菜单共139道菜，每道菜都有照片和价格。</p>
<div class="ctas"><a class="btn gold" href="/carta/">查看菜单</a><a class="btn ghost" href="/reservas/">网上订座</a></div></div>
<div class="collage" aria-hidden="true"><img src="/img/9A.webp" alt="" width="900" height="675"><img src="/img/t/22B.webp" alt="" width="480" height="360"><img src="/img/t/C5.webp" alt="" width="480" height="360"></div></div></section>
<div class="band"><div class="wrap"><div><small>营业时间</small><span>周二至周日 12:00–17:00、19:30–24:00 · 周一休息</span></div><div><small>地址</small><span>C. de Ventura Rodríguez, 5 · 28008 Madrid</span></div><div><small>电话</small><span><a class="tel" href="tel:+34919414881">919 41 48 81</a></span></div></div></div>
<div class="sec"><div class="wrap seo-grid"><div><h2 class="h2s">西班牙广场附近的日料自助餐</h2>
<p>用餐时间90分钟，用桌上的平板电脑点餐，想吃多少点多少：握寿司、卷寿司、特色卷、三文鱼和金枪鱼刺身、薄切生鱼片（carpaccio）、小笼包和烧卖等点心、天妇罗、炒锅菜、炒饭炒面、铁板和甜品，全部现点现做。</p>
<table class="bftab"><caption>每人价格，含税</caption><tbody><tr><th scope="row">自助餐 · 周二至周五午餐（节假日及节日前夕除外）</th><td>17,95 €</td></tr><tr><th scope="row">自助餐 · 周二至周四晚餐（节假日及节日前夕除外）</th><td>23,95 €</td></tr><tr><th scope="row">自助餐 · 周五晚餐、周六、周日及节假日</th><td>27,95 €</td></tr><tr><th scope="row">自助餐 · 儿童（身高100–130厘米）</th><td>11,95 €</td></tr><tr><th scope="row">自助餐 · 3岁以下</th><td>免费</td></tr><tr><th scope="row">每日套餐（menú del día），周二至周日，四道菜任选</th><td>15,95 €</td></tr></tbody></table>
<p>自助餐不含饮料和甜品。也可以单点：<a href="/carta/">网上菜单</a>每道菜都有照片、价格和过敏原，还可以筛选素食菜品。</p>
<h2 class="h2s">订座和外带</h2>
<p>在<a href="/reservas/">订座页面</a>（西班牙语）选择人数（<i>personas</i>）、日期（<i>día</i>）和时间（<i>hora</i>），确认信息会发到您的邮箱。网上点餐、到店自取享八折优惠。生日、朋友聚会、公司聚餐和圣诞晚宴都可以预订，详情请看<a href="/grupos-y-cumpleanos/">团体聚餐</a>（西班牙语）或打电话 919 41 48 81。</p>
<h2 class="h2s">交通</h2>
<ul class="como">
<li><b>从西班牙广场：</b>沿 Calle Princesa 走到 Calle de Ventura Rodríguez，步行约3–4分钟。</li>
<li><b>地铁 Ventura Rodríguez（3号线）：</b>最近的地铁站，步行约2分钟。</li>
<li><b>地铁 Plaza de España（2、3、10号线）：</b>步行约5分钟。</li>
<li><b>从 Gran Vía 或 Callao：</b>乘3号线到 Ventura Rodríguez，Callao 出发两站。</li>
<li><b>从 Argüelles 或 Moncloa：</b>乘3号线一至两站到 Ventura Rodríguez。</li>
<li><b>德波神庙（Templo de Debod）：</b>步行约5分钟。</li>
<li><b>Renoir Princesa 电影院：</b>就在旁边的 Plaza de los Cubos 广场。</li>
</ul>
<p>原来在 Paseo de la Castellana 的店已经关闭，现在只在 C. de Ventura Rodríguez 5 营业，欢迎老朋友来新店！</p>
<p><a class="btn gold" target="_blank" rel="noopener" href="''' + MAPS + '''">谷歌地图导航</a></p></div>
<div><h2 class="h2s">常见问题</h2>''' + faq_html(ZH_FAQ) + '''</div></div></div></main>
<style>.como{margin:6px 0 14px;padding-left:20px;line-height:1.55}.como li{margin:6px 0}.bftab td{white-space:nowrap}</style>'''

ZH_HEADER_NAV = '<nav class="nav"><a href="/carta/">菜单</a><a href="/reservas/">订座</a><a href="/">Español</a><a href="/en/">English</a></nav>'
ZH_FOOTER = ('<footer><div class="wrap"><div><p>Lang City · XLK MADRID, S.L.</p></div><div><h4>营业时间</h4><p>周二至周日 12:00–17:00 · 19:30–24:00 · 周一休息</p></div>'
             '<div><h4>联系方式</h4><p>C. de Ventura Rodríguez, 5, 28008 Madrid</p><p><a href="tel:+34919414881">919 41 48 81</a></p></div>'
             '<div><h4>网站</h4><p><a href="/carta/">菜单</a></p><p><a href="/reservas/">订座</a></p><p><a href="/aviso-legal.html">Aviso legal</a></p></div></div></footer>')

RES_ANCHOR = re.compile(r'(<h1>Reserva tu mesa</h1><p>[^<]*</p>)')
RES_ADD = ('<p>Lang City está en C. de Ventura Rodríguez 5, junto a Plaza de España (entrada por C. de Santa María Micaela 6, en Plaza de los Cubos). '
           'Reserva para comer o cenar de martes a domingo: buffet libre desde 17,95 €, menú del día por 15,95 € o carta. '
           'Para cumpleaños, comidas de empresa y cenas de Navidad, mira <a href="/grupos-y-cumpleanos/">grupos y cumpleaños</a>.</p>')
CON_ANCHOR = '(los lunes descansamos).</p>'
CON_ADD = ('<p>La entrada está en C. de Santa María Micaela 6, en Plaza de los Cubos. Metro Ventura Rodríguez (línea 3) o Plaza de España (líneas 2, 3 y 10). '
           '<a href="/sushi-plaza-de-espana/">Cómo llegar desde Plaza de España, Gran Vía, Argüelles o Moncloa</a>.</p>')


def do_en(root):
    p = os.path.join(root, 'en', 'index.html')
    if not os.path.isfile(p):
        return None
    t = rd(p)
    if 'All-you-can-eat sushi near Plaza de España</h2>' not in t:
        t = set_head(t, EN_TITLE, EN_DESC, BASE + 'en/')
        t = swap_main(t, EN_MAIN)
        t = add_faq_ld(t, EN_FAQ)
    if '<a href="/zh/">中文</a>' not in t:
        t = t.replace('<a href="/">Español</a></nav>', '<a href="/">Español</a><a href="/zh/">中文</a></nav>', 1)
        t = t.replace('<p><a href="/aviso-legal.html">Legal notice</a></p>', '<p><a href="/zh/">中文</a></p><p><a href="/aviso-legal.html">Legal notice</a></p>', 1)
    wr(p, t)
    return t


def do_zh(root, en_html):
    p = os.path.join(root, 'zh', 'index.html')
    if os.path.isfile(p) or not en_html:
        return
    t = en_html.replace('<html lang="en">', '<html lang="zh-Hans">', 1)
    t = set_head(t, ZH_TITLE, ZH_DESC, BASE + 'zh/')
    t = t.replace('<meta property="og:locale" content="en_GB">', '<meta property="og:locale" content="zh_CN">')
    t = t.replace('"url": "https://langsushi.es/en/"', '"url": "https://langsushi.es/zh/"')
    t = t.replace('"description": "Japanese and fusion sushi restaurant near Plaza de España, Madrid."', '"description": "马德里西班牙广场附近的日料寿司融合餐厅。"')
    t = re.sub(r'<nav class="nav">.*?</nav>', ZH_HEADER_NAV, t, count=1, flags=re.S)
    t = t.replace('<a class="logo" href="/en/">', '<a class="logo" href="/zh/">', 1)
    t = swap_main(t, ZH_MAIN)
    t = re.sub(r'<footer>.*?</footer>', ZH_FOOTER, t, count=1, flags=re.S)
    t = add_faq_ld(t, ZH_FAQ)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    wr(p, t)


def link_all(root):
    n = 0
    for r, _, fs in os.walk(root):
        if '/admin' in r.replace('\\', '/'):
            continue
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(r, f)
            t = rd(p); o = t
            if ALT_EN in o and ALT_ZH not in o:
                o = o.replace(ALT_EN, ALT_EN + ALT_ZH)
            rel = os.path.relpath(p, root).replace('\\', '/')
            if rel != 'zh/index.html' and '<a href="/en/">English</a>' in o and '<a href="/zh/">中文</a>' not in o:
                o = o.replace('<a href="/en/">English</a>', '<a href="/en/">English</a> · <a href="/zh/">中文</a>', 1)
            rel = os.path.relpath(p, root).replace('\\', '/')
            if rel == 'reservas/index.html' and 'Reserva para comer o cenar de martes a domingo' not in o:
                o = RES_ANCHOR.sub(lambda m: m.group(1) + RES_ADD, o, count=1)
            if rel == 'contacto/index.html' and 'Cómo llegar desde Plaza de España, Gran Vía' not in o:
                o = o.replace(CON_ANCHOR, CON_ANCHOR + CON_ADD, 1)
            if o != t:
                wr(p, o); n += 1
    return n


def do_sitemap(root):
    sm = os.path.join(root, 'sitemap.xml')
    if not os.path.isfile(sm):
        return
    t = rd(sm)
    if BASE + 'zh/</loc>' in t:
        return
    xen = '<xhtml:link rel="alternate" hreflang="en" href="https://langsushi.es/en/"/>'
    xzh = '<xhtml:link rel="alternate" hreflang="zh-Hans" href="https://langsushi.es/zh/"/>'
    t = t.replace(xen, xen + xzh)
    entry = ('<url><loc>' + BASE + 'zh/</loc><lastmod>2026-11-09</lastmod><priority>0.7</priority>'
             '<xhtml:link rel="alternate" hreflang="es" href="https://langsushi.es/"/>' + xen + xzh + '</url>')
    t = t.replace('</urlset>', entry + '</urlset>', 1)
    t = t.replace('<loc>https://langsushi.es/en/</loc><lastmod>2026-11-05</lastmod>', '<loc>https://langsushi.es/en/</loc><lastmod>2026-11-09</lastmod>', 1)
    wr(sm, t)
    ll = os.path.join(root, 'llms.txt')
    if os.path.isfile(ll):
        l = rd(ll)
        if '/zh/' not in l:
            l = l.replace('- [English](https://langsushi.es/en/)\n', '- [English](https://langsushi.es/en/)\n- [中文](https://langsushi.es/zh/)\n', 1)
            wr(ll, l)


def main(args):
    root = args[0] if args else 'site'
    en = do_en(root)
    do_zh(root, en)
    n = link_all(root)
    do_sitemap(root)
    print('patch_idiomas: hecho; páginas tocadas', n)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception as e:
        print('patch_idiomas: ERROR (la web se publica igual):', e)

# Pedido para llevar mas visible (27/11/2026).
# 1) Portada ES/EN/ZH: el boton principal (dorado) pasa a ser "Pedir para llevar −40%".
# 2) El bloque −40% de la portada enlaza a la carta.
# 3) Titulo y descripcion de la portada y de la carta usan "para llevar" (lo que busca la gente).
# 4) El texto de la portada enlaza a la pagina /sushi-para-llevar/.
# Va despues de patch_..._recoger40.py y patch_..._pagos.py. Nunca rompe la publicacion.
import os, sys

R = [
    # Botones del hero
    ('<div class="ctas"><a class="btn gold" href="#menus">Ver menús y precios</a><a class="btn ghost" href="/reservas/">Reservar mesa</a><a class="btn ghost" href="/carta/">Ver la carta</a></div>',
     '<div class="ctas"><a class="btn gold" href="/carta/">Pedir para llevar −40%</a><a class="btn ghost" href="/reservas/">Reservar mesa</a><a class="btn ghost" href="#menus">Ver menús y precios</a></div>'),
    ('<div class="ctas"><a class="btn gold" href="/carta/">See the menu</a><a class="btn ghost" href="/reservas/">Book a table</a></div>',
     '<div class="ctas"><a class="btn gold" href="/carta/">Order takeaway −40%</a><a class="btn ghost" href="/reservas/">Book a table</a><a class="btn ghost" href="/carta/">See the menu</a></div>'),
    ('<div class="ctas"><a class="btn gold" href="/carta/">查看菜单</a><a class="btn ghost" href="/reservas/">网上订座</a></div>',
     '<div class="ctas"><a class="btn gold" href="/carta/">外带自取 · 六折</a><a class="btn ghost" href="/reservas/">网上订座</a><a class="btn ghost" href="/carta/">查看菜单</a></div>'),
    # Bloque −40% clicable
    ('<div class="promo"><b>−40%</b><span>en tu pedido para recoger en el restaurante, haciéndolo desde esta web.</span></div>',
     '<a class="promo" href="/carta/" style="text-decoration:none;color:inherit"><b>−40%</b><span>en tu pedido para llevar: pídelo en esta web y recógelo en el restaurante.</span></a>'),
    # Titulo y descripcion
    ('Lang City · Sushi y buffet libre junto a Plaza de España',
     'Lang City · Sushi, buffet libre y para llevar junto a Plaza de España'),
    ('carta con fotos y precios y reserva online.',
     'carta con fotos y precios, sushi para llevar con 40 % de descuento y reserva online.'),
    ('Pide para recoger con 40 % de descuento.',
     'Pide sushi para llevar con 40 % de descuento.'),
    ('haz tu pedido para recoger o reserva mesa online',
     'haz tu pedido para llevar o reserva mesa online'),
    # Enlace a la pagina de sushi para llevar
    ('o pedir para recoger con un 40 % de descuento.</p>',
     'o <a href="/sushi-para-llevar/">pedir sushi para llevar</a> con un 40 % de descuento.</p>'),
]


def main(args):
    done, usados = 0, set()
    for a in args:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            if '/admin/' in p.replace('\\', '/'):
                continue
            try:
                t = open(p, encoding='utf-8').read()
            except Exception:
                continue
            n = t
            for i, (x, y) in enumerate(R):
                if x in n:
                    n = n.replace(x, y)
                    usados.add(i)
            if n != t:
                with open(p, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(n)
                done += 1
    print('patch_llevar: archivos cambiados', done)
    for i, (x, _) in enumerate(R):
        if i not in usados:
            print('  no encontrado:', x[:90])


if __name__ == '__main__':
    try:
        main(sys.argv[1:] or ['site'])
    except Exception as e:
        print('patch_llevar: error (se ignora)', e)

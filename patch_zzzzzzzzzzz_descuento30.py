# Descuento de los pedidos para recoger hechos desde la web: 30 % (antes 20 %). Desde el 17/11/2026.
# Cambia el calculo del carrito y todos los textos (ES/EN/ZH, schema, llms.txt). Va el ultimo. Nunca rompe la publicacion.
import os, re, sys

R = [
    ('const PICKUP_DISCOUNT = 0.20;', 'const PICKUP_DISCOUNT = 0.30;'),
    ('const PICKUP_DISCOUNT=0.20;', 'const PICKUP_DISCOUNT=0.30;'),
    ('const PICKUP_DISCOUNT = 0.2;', 'const PICKUP_DISCOUNT = 0.30;'),
    ('Recoger (−20%)', 'Recoger (−30%)'),
    ('Descuento recogida 20%', 'Descuento recogida 30%'),
    ('<b>−20%</b>', '<b>−30%</b>'),
    ('20 % de descuento', '30 % de descuento'),
    ('20% de descuento', '30 % de descuento'),
    ('with 20% off', 'with 30% off'),
    ('20% off', '30% off'),
    ('八折优惠', '七折优惠（立减30%）'),
]
CHECK = re.compile(r'20 ?% de descuento|−20%|recogida 20|PICKUP_DISCOUNT ?= ?0\.2|20% off|八折')


def main(args):
    done, left = 0, []
    for a in args:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt', '.js', '.json'))]
        for p in files:
            if os.path.basename(p) == 'admin.html' or '/admin/' in p:
                continue
            try:
                with open(p, encoding='utf-8') as f:
                    t = f.read()
            except Exception:
                continue
            n = t
            for x, y in R:
                n = n.replace(x, y)
            if n != t:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(n)
                done += 1
            for m in CHECK.finditer(n):
                left.append('%s: ...%s...' % (p, n[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ')))
    print('patch_descuento30: archivos cambiados', done)
    for l in left[:20]:
        print('  queda:', l)


if __name__ == '__main__':
    try:
        main(sys.argv[1:] or ['site'])
    except Exception as e:
        print('patch_descuento30: error (se ignora)', e)

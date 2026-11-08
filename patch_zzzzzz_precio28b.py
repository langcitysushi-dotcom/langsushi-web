# Precio 28B (08/11/2026): el Roll Tartar de Salmón con Cebolla cuesta 16,95 €, no 6,95 €.
# Corrige la carta (datos del pedido, tarjeta visible y datos para Google). No hace nada si ya está corregido.
import os, re, sys

R = [
    (re.compile(r'(\{"id":"28B"[^}]*?"p":)6\.95\b'), r'\g<1>16.95'),
    (re.compile(r'("name": "Roll Tartar de Salm(?:ó|o)n con Cebolla", "offers": \{"@type": "Offer", "price": ")6\.95"'), r'\g<1>16.95"'),
    (re.compile(r'(Roll Tartar de Salm(?:ó|o)n con Cebolla</h3>(?:(?!</article>).){0,400}?<span class="price">)6,95(\s|&nbsp;)?€', re.S), r'\g<1>16,95\2€'),
]

def patch_text(t):
    for rx, rep in R:
        t = rx.sub(rep, t)
    return t

def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            t = open(p, encoding='utf-8').read(); o = patch_text(t)
            if o != t:
                open(p, 'w', encoding='utf-8').write(o); n += 1
    print('patch_precio28b: archivos cambiados', n)

if __name__ == '__main__':
    main(sys.argv[1:])

# Bebida gratis de apertura: termina el domingo 15/11/2026 (antes 30/11). Los avisos se ocultan solos desde el 16/11.
import os, sys
R = [
    ('data-hasta="2026-11-30"', 'data-hasta="2026-11-15"'),
    ('<strong>Noviembre de apertura:</strong> tu primera bebida gratis con el buffet o el menú del día.',
     '<strong>Hasta el domingo 15 de noviembre:</strong> tu primera bebida gratis con el buffet o el menú del día, por nuestra apertura.'),
    ('<div class="nov-b">Noviembre</div>', '<div class="nov-b">Hasta el 15</div>'),
    ('Durante todo noviembre, con tu buffet', 'Hasta el domingo 15 de noviembre, con tu buffet'),
    ('Válido hasta el 30 de noviembre.', 'Válido hasta el domingo 15 de noviembre.'),
]
def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt'))]
        for p in files:
            t = open(p, encoding='utf-8').read(); o = t
            for x, y in R: t = t.replace(x, y)
            if t != o: open(p, 'w', encoding='utf-8').write(t); n += 1
    print('patch_nov15: archivos cambiados', n)
if __name__ == '__main__': main(sys.argv[1:])

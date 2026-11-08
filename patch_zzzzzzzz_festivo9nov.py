# Lunes 9/11/2026 (festivo de La Almudena): abrimos con horario normal y tarifa de festivo.
# Aviso en portada (se oculta solo desde el 10/11 con data-hasta) y "Abierto ahora" sin el cierre de los lunes ese día.
# No hace nada si ya está aplicado.
import os, sys
AVISO = ('<div class="promo" data-hasta="2026-11-09"><b>Lunes 9</b><span><strong>Abrimos el lunes 9 de noviembre (festivo de La Almudena):</strong> '
         '12:00–17:00 y 19:30–24:00, con tarifa de festivo.</span></div>\n        ')
R = [
    ('<div class="promo promo-nov" data-hasta="2026-11-15">', AVISO + '<div class="promo promo-nov" data-hasta="2026-11-15">'),
    ('weekday:"short"})==="Mon"){el.innerHTML="<i>Cerrado</i> · los lunes descansamos',
     'weekday:"short"})==="Mon"&&new Date().toLocaleString("sv-SE",{timeZone:"Europe/Madrid"}).slice(0,10)!=="2026-11-09"){el.innerHTML="<i>Cerrado</i> · los lunes descansamos'),
]
MARKS = ['data-hasta="2026-11-09"', '!=="2026-11-09"){el.innerHTML']

def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            if os.path.basename(p) == 'admin.html' or '/admin/' in p:
                continue
            t = open(p, encoding='utf-8').read(); o = t
            for (x, y), m in zip(R, MARKS):
                if m not in t:
                    t = t.replace(x, y)
            if t != o:
                open(p, 'w', encoding='utf-8').write(t); n += 1
    print('patch_festivo9nov: archivos cambiados', n)

if __name__ == '__main__':
    main(sys.argv[1:])

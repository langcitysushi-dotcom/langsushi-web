# Quita del HTML los avisos y promociones caducados (elementos <div ... data-hasta="AAAA-MM-DD">).
# En el navegador ya se ocultaban por JavaScript, pero el texto seguía en el código y Google lo podía mostrar.
# Se ejecuta en cada publicación, así que cualquier aviso nuevo con data-hasta desaparece solo al caducar.
import os, re, sys, datetime
try:
    from zoneinfo import ZoneInfo
    HOY = datetime.datetime.now(ZoneInfo('Europe/Madrid')).date().isoformat()
except Exception:
    HOY = datetime.date.today().isoformat()

ABRE = re.compile(r'<div\b[^>]*\bdata-hasta="(\d{4}-\d{2}-\d{2})"[^>]*>')
ETIQ = re.compile(r'<(/?)div\b[^>]*>')

def quitar(t):
    n = 0
    while True:
        m = next((m for m in ABRE.finditer(t) if m.group(1) < HOY), None)
        if not m:
            return t, n
        prof, fin = 0, None
        for e in ETIQ.finditer(t, m.start()):
            prof += -1 if e.group(1) else 1
            if prof == 0:
                fin = e.end(); break
        if fin is None:
            return t, n
        ini = m.start()
        while ini > 0 and t[ini - 1] in ' \t': ini -= 1
        if ini > 0 and t[ini - 1] == '\n': ini -= 1
        t = t[:ini] + t[fin:]; n += 1

def main(args):
    total = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            t = open(p, encoding='utf-8').read()
            t2, n = quitar(t)
            if n:
                open(p, 'w', encoding='utf-8').write(t2); total += n
    print('patch_caducados: avisos caducados quitados', total, '(hoy', HOY + ')')

if __name__ == '__main__': main(sys.argv[1:])

# Desde el 16/11/2026 el restaurante abre TODOS los dias (tambien los lunes).
# Deshace "lunes cerrado" (patch_zz_lunes.py y textos de otros parches): textos ES/EN/ZH,
# precios por dias (lunes a viernes / lunes a jueves), schema con Monday, reservas y "abierto ahora".
# Va el ultimo (orden alfabetico). No hace nada si ya esta aplicado. Nunca rompe la publicacion.
import os, re, sys

R = [
    # --- espanol: frases completas primero ---
    ('Martes a domingo · 12:00–17:00 y 19:30–24:00 · lunes cerrado', 'Todos los días · 12:00–17:00 y 19:30–24:00'),
    ('<dt>Días</dt><dd>Martes a domingo</dd><dt>Lunes</dt><dd>Cerrado (descanso)</dd>', '<dt>Días</dt><dd>Todos los días, de lunes a domingo</dd>'),
    ('<dt>Horario</dt><dd>Martes a domingo · lunes cerrado<br>', '<dt>Horario</dt><dd>Todos los días, de lunes a domingo<br>'),
    ('<h4>Horario</h4><p>Martes a domingo · lunes cerrado</p>', '<h4>Horario</h4><p>Todos los días, de lunes a domingo</p>'),
    ('Abrimos de martes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. Los lunes cerramos por descanso.',
     'Abrimos todos los días, de lunes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. No cerramos ningún día de la semana.'),
    ('De martes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. Los lunes cerramos por descanso.',
     'Todos los días, de lunes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. No cerramos ningún día de la semana.'),
    ('Martes a domingo 12:00–17:00 · 19:30–24:00 · lunes cerrado', 'Todos los días 12:00–17:00 · 19:30–24:00'),
    ('Martes a domingo 12:00–17:00 y 19:30–24:00 (lunes cerrado)', 'Todos los días 12:00–17:00 y 19:30–24:00'),
    ('De martes a domingo, de 19:30 a 24:00', 'Todos los días, de 19:30 a 24:00'),
    ('Abrimos de martes a domingo hasta las 24:00 (los lunes cerramos).', 'Abrimos todos los días hasta las 24:00.'),
    ('Abrimos de martes a domingo a mediodía y por la noche (los lunes descansamos).', 'Abrimos todos los días a mediodía y por la noche.'),
    ('Horario: de martes a domingo 12:00–17:00 y 19:30–24:00; lunes cerrado', 'Horario: todos los días (de lunes a domingo) 12:00–17:00 y 19:30–24:00'),
    ('todos los días que abrimos (de martes a domingo)', 'todos los días (de lunes a domingo)'),
    ('Reserva para comer o cenar de martes a domingo', 'Reserva para comer o cenar cualquier día de la semana'),
    ('Los lunes el restaurante está cerrado por descanso. Elige otro día.', 'Elige otro día.'),
    # precios por dias
    ('de martes a viernes', 'de lunes a viernes'),
    ('de martes a jueves', 'de lunes a jueves'),
    ('Martes a viernes, no festivos', 'Lunes a viernes, no festivos'),
    ('Martes a jueves, no festivos', 'Lunes a jueves, no festivos'),
    ('Noches M–J', 'Noches L–J'),
    # restos genericos
    (' · lunes cerrado', ''),
    (' (lunes cerrado)', ''),
    ('; lunes cerrado', ''),
    ('de martes a domingo', 'de lunes a domingo'),
    ('Martes a domingo', 'Lunes a domingo'),
    # --- ingles ---
    ('Tuesday to Sunday · 12:00–17:00 and 19:30–24:00 · closed on Mondays', 'Every day · 12:00–17:00 and 19:30–24:00 (Monday to Sunday)'),
    ('Tue–Sun 12:00–17:00 · 19:30–24:00 · closed Mon', 'Every day 12:00–17:00 · 19:30–24:00'),
    ('No. We are open Tuesday to Sunday, 12:00–17:00 and 19:30–24:00, and closed on Mondays.',
     'Yes. We are open every day, Monday to Sunday, 12:00–17:00 and 19:30–24:00.'),
    ('weekday lunch (Tue–Fri)', 'weekday lunch (Mon–Fri)'),
    ('Tuesday to Friday', 'Monday to Friday'),
    ('Tuesday to Thursday', 'Monday to Thursday'),
    ('Tuesday to Sunday', 'Monday to Sunday'),
    (', and closed on Mondays', ''),
    (' · closed on Mondays', ''),
    (' · closed Mon', ''),
    # --- chino ---
    ('周一休息。营业时间为周二至周日 12:00–17:00 和 19:30–24:00。', '营业。我们每天营业（周一至周日），12:00–17:00 和 19:30–24:00。'),
    ('周二至周日 12:00–17:00、19:30–24:00 · 周一休息', '每天营业（周一至周日）12:00–17:00、19:30–24:00'),
    ('周二至周日 12:00–17:00 · 19:30–24:00 · 周一休息', '每天 12:00–17:00 · 19:30–24:00'),
    ('周二至周五', '周一至周五'),
    ('周二至周四', '周一至周四'),
    ('周二至周日', '周一至周日'),
    (' · 周一休息', ''),
    ('，周一休息', ''),
    ('（周一休息）', ''),
    # --- schema.org ---
    ('"dayOfWeek": ["Tuesday", "Wednesday"', '"dayOfWeek": ["Monday", "Tuesday", "Wednesday"'),
    ('"dayOfWeek":["Tuesday","Wednesday"', '"dayOfWeek":["Monday","Tuesday","Wednesday"'),
    # --- reservas (formulario antiguo) ---
    ('if((dateStr?new Date(dateStr+"T00:00"):new Date()).getDay()===1)return [];', ''),
    ('if(x.getDay()===1)continue;', ''),
]
RX = [
    # bloque "lunes cerrado" en loadAvail
    (re.compile(r'if\(RS\.fecha&&new Date\(RS\.fecha\+"T00:00"\)\.getDay\(\)===1\)\{.*?`;return\}', re.S), ''),
    # "abierto ahora": cerrado los lunes
    (re.compile(r'if\(new Date\(\)\.toLocaleString\("en-GB",\{timeZone:"Europe/Madrid",weekday:"short"\}\)==="Mon".{0,200}?\)\{el\.innerHTML="<i>Cerrado</i> · los lunes descansamos[^"]*";return\}'), ''),
]
CHECK = re.compile(r'lunes cerrado|lunes descans|lunes cerramos|Cerrado \(descanso\)|closed on Monday|closed Mon|周一休息|getDay\(\)===1')


def patch_text(t):
    for a, b in R:
        t = t.replace(a, b)
    for rx, b in RX:
        t = rx.sub(b, t)
    return t


def main(args):
    done, left = 0, []
    for a in args:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt', '.js', '.xml'))]
        for p in files:
            if os.path.basename(p) == 'admin.html' or '/admin/' in p:
                continue
            try:
                with open(p, encoding='utf-8') as f:
                    t = f.read()
            except Exception:
                continue
            n = patch_text(t)
            if n != t:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(n)
                done += 1
            for m in CHECK.finditer(n):
                left.append('%s: ...%s...' % (p, n[max(0, m.start() - 60):m.end() + 60].replace('\n', ' ')))
    print('patch_lunesabierto: archivos cambiados', done)
    for l in left[:30]:
        print('  queda:', l)


if __name__ == '__main__':
    try:
        main(sys.argv[1:] or ['site'])
    except Exception as e:
        print('patch_lunesabierto: error (se ignora)', e)

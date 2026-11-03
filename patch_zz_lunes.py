# Lunes cerrado (descanso semanal): textos, schema, reservas y "abierto ahora".
# Uso: python3 patch_zz_lunes.py <carpeta_o_archivo> [...]. No hace nada si ya está aplicado.
import os, sys

R = [
    # horarios
    ('Lunes a domingo · 12:00–17:00 y 19:30–24:00', 'Martes a domingo · 12:00–17:00 y 19:30–24:00 · lunes cerrado'),
    ('<dt>Días</dt><dd>Lunes a domingo</dd>', '<dt>Días</dt><dd>Martes a domingo</dd><dt>Lunes</dt><dd>Cerrado (descanso)</dd>'),
    ('<dt>Horario</dt><dd>Lunes a domingo<br>', '<dt>Horario</dt><dd>Martes a domingo · lunes cerrado<br>'),
    ('<h4>Horario</h4><p>Lunes a domingo</p>', '<h4>Horario</h4><p>Martes a domingo · lunes cerrado</p>'),
    ('Abrimos de lunes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00.', 'Abrimos de martes a domingo, de 12:00 a 17:00 y de 19:30 a 24:00. Los lunes cerramos por descanso.'),
    ('Todos los días 12:00–17:00 · 19:30–24:00', 'Martes a domingo 12:00–17:00 · 19:30–24:00 · lunes cerrado'),
    ('Todos los días 12:00–17:00 y 19:30–24:00', 'Martes a domingo 12:00–17:00 y 19:30–24:00 (lunes cerrado)'),
    ('Todos los días de 19:30 a 24:00', 'De martes a domingo, de 19:30 a 24:00'),
    ('Abrimos todos los días hasta las 24:00.', 'Abrimos de martes a domingo hasta las 24:00 (los lunes cerramos).'),
    ('Abrimos todos los días a mediodía y por la noche.', 'Abrimos de martes a domingo a mediodía y por la noche (los lunes descansamos).'),
    ('Horario: todos los días 12:00–17:00 y 19:30–24:00', 'Horario: de martes a domingo 12:00–17:00 y 19:30–24:00; lunes cerrado'),
    # precios por días
    ('de lunes a viernes', 'de martes a viernes'),
    ('de lunes a jueves', 'de martes a jueves'),
    ('Lunes a viernes, no festivos', 'Martes a viernes, no festivos'),
    ('Lunes a jueves, no festivos', 'Martes a jueves, no festivos'),
    ('Noches L–J', 'Noches M–J'),
    # inglés
    ('Every day · 12:00–17:00 and 19:30–24:00', 'Tuesday to Sunday · 12:00–17:00 and 19:30–24:00 · closed on Mondays'),
    ('Every day 12:00–17:00 · 19:30–24:00', 'Tue–Sun 12:00–17:00 · 19:30–24:00 · closed Mon'),
    ('weekday lunch (Mon–Fri)', 'weekday lunch (Tue–Fri)'),
    ('dinner Monday to Thursday', 'dinner Tuesday to Thursday'),
    # schema.org
    ('"dayOfWeek": ["Monday", "Tuesday"', '"dayOfWeek": ["Tuesday"'),
    ('"dayOfWeek":["Monday","Tuesday"', '"dayOfWeek":["Tuesday"'),
    # reservas: sin horas los lunes, primer día abierto, chips sin lunes
    ('function slots(dateStr){', 'function slots(dateStr){if((dateStr?new Date(dateStr+"T00:00"):new Date()).getDay()===1)return [];'),
    ('function firstDay(){const t=new Date();const s=ymd(t);if(slots(s).length)return s;t.setDate(t.getDate()+1);return ymd(t)}',
     'function firstDay(){const t=new Date();for(let i=0;i<7;i++){const s=ymd(t);if(slots(s).length)return s;t.setDate(t.getDate()+1)}return ymd(t)}'),
    ('for(let i=0;i<14;i++){const x=new Date(d);x.setDate(d.getDate()+i);const f=ymd(x);',
     'for(let i=0,n=0;n<14&&i<20;i++){const x=new Date(d);x.setDate(d.getDate()+i);if(x.getDay()===1)continue;n++;const f=ymd(x);'),
    ('async function loadAvail(){', 'async function loadAvail(){if(RS.fecha&&new Date(RS.fecha+"T00:00").getDay()===1){RS.hora=null;$("#resForm").hidden=true;$("#slots").innerHTML=`<p class="closed">Los lunes el restaurante está cerrado por descanso. Elige otro día.</p>`;return}'),
    # "abierto ahora"
    ('function abiertoAhora(){const el=document.getElementById("abierto");if(!el)return;',
     'function abiertoAhora(){const el=document.getElementById("abierto");if(!el)return;if(new Date().toLocaleString("en-GB",{timeZone:"Europe/Madrid",weekday:"short"})==="Mon"){el.innerHTML="<i>Cerrado</i> · los lunes descansamos; abrimos el martes a las 12:00";return}'),
]
MARK = 'lunes cerrado'

def patch_text(t):
    for a, b in R:
        if b in t:
            continue
        t = t.replace(a, b)
    return t

def patch_file(p):
    with open(p, encoding='utf-8') as f:
        t = f.read()
    n = patch_text(t)
    if n != t:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(n)
        return True
    return False

def main(args):
    done = 0
    for a in args:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt'))]
        for p in files:
            if os.path.basename(p) == 'admin.html' or '/admin/' in p:
                continue
            done += patch_file(p)
    print('patch_lunes: archivos cambiados', done)

if __name__ == '__main__':
    main(sys.argv[1:] or ['site'])

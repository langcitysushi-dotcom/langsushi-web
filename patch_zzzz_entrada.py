# En Plaza de los Cubos, entrada por C. de Santa María Micaela, 6 (confirmado por el dueño 05/11/2026). Va después de patch_zzz_cubos.
# La dirección oficial sigue siendo C. de Ventura Rodríguez 5 (datos estructurados sin cambios).
import os, sys
R = [
    ('a un paso de Plaza de los Cubos: 1–2 minutos andando',
     'en Plaza de los Cubos (entrada por C. de Santa María Micaela, 6): 1–2 minutos andando'),
    ('a un minuto de Plaza de los Cubos y de los cines Renoir Princesa',
     'en Plaza de los Cubos, junto a los cines Renoir Princesa'),
    ('<b>C. de Ventura Rodríguez 5</b>, a un minuto andando de Plaza de los Cubos.',
     '<b>C. de Ventura Rodríguez 5</b>, en la propia Plaza de los Cubos (entrada por la calle de Santa María Micaela, 6).'),
    ('Uno o dos minutos. Estamos en C. de Ventura Rodríguez 5, a un paso de Plaza de los Cubos y muy cerca de Plaza de España.',
     'Uno o dos minutos: estamos en la misma Plaza de los Cubos, con entrada por la calle de Santa María Micaela, 6 (C. de Ventura Rodríguez 5), muy cerca de Plaza de España.'),
    ('a un paso de Plaza de los Cubos y de Plaza de España',
     'en Plaza de los Cubos, junto a Plaza de España'),
    ('<span>C. de Ventura Rodríguez, 5 · Plaza de los Cubos · 28008 Madrid</span>',
     '<span>C. de Ventura Rodríguez, 5 · Plaza de los Cubos (entrada por C. de Santa María Micaela, 6) · 28008 Madrid</span>'),
    ('<h4>Contacto</h4><p>C. de Ventura Rodríguez, 5, 28008 Madrid</p>',
     '<h4>Contacto</h4><p>C. de Ventura Rodríguez, 5, 28008 Madrid<br>Plaza de los Cubos · entrada por C. de Santa María Micaela, 6</p>'),
    ('<h2 class="h2s">Cómo llegar</h2><p>C. de Ventura Rodríguez, 5, 28008 Madrid.',
     '<h2 class="h2s">Cómo llegar</h2><p>C. de Ventura Rodríguez, 5, 28008 Madrid: estamos en Plaza de los Cubos, con entrada por la calle de Santa María Micaela, 6.'),
    ('Restaurante japonés y sushi fusión en C. de Ventura Rodríguez 5, junto a Plaza de España (Madrid).',
     'Restaurante japonés y sushi fusión en Plaza de los Cubos (C. de Ventura Rodríguez 5), junto a Plaza de España.'),
    ('<h4>Contact</h4><p>Calle de Ventura Rodríguez, 5, 28008 Madrid</p>',
     '<h4>Contact</h4><p>Calle de Ventura Rodríguez, 5, 28008 Madrid<br>Plaza de los Cubos · entrance on C. de Santa María Micaela, 6</p>'),
]
def patch_text(t):
    for a, b in R:
        if b in t:
            continue
        t = t.replace(a, b)
    return t
def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt'))]
        for p in files:
            if '/admin/' in p:
                continue
            t = open(p, encoding='utf-8').read(); o = patch_text(t)
            if o != t: open(p, 'w', encoding='utf-8').write(o); n += 1
    print('patch_entrada: archivos cambiados', n)
if __name__ == '__main__': main(sys.argv[1:])

# Plaza de los Cubos: el restaurante está a ~70 m de la plaza y a ~90 m de los cines Renoir Princesa
# (medido en Google Maps el 05/11/2026). Corrige "5 minutos" y añade la plaza en portada y en la página de cines.
import os, sys
R = [
    ('Sushi junto a los cines de Princesa, Madrid · Lang City', 'Sushi en Plaza de los Cubos y cines Princesa · Lang City'),
    ('a unos 5 minutos andando de los cines de Princesa y Plaza de los Cubos', 'a un minuto de Plaza de los Cubos y de los cines Renoir Princesa'),
    ('Sushi antes o después del cine, a 5 minutos de Princesa', 'Sushi en Plaza de los Cubos, antes o después del cine'),
    ('<b>C. de Ventura Rodríguez 5</b>, a unos cinco minutos andando.', '<b>C. de Ventura Rodríguez 5</b>, a un minuto andando de Plaza de los Cubos.'),
    ('Unos 5 minutos desde los cines de Princesa', '1–2 minutos desde los cines Renoir Princesa'),
    ('a unos cinco minutos andando de los cines de Princesa y Martín de los Heros.', 'a un paso de Plaza de los Cubos: 1–2 minutos andando de los cines Renoir Princesa y unos 5 de los de Martín de los Heros.'),
    ('Unos cinco minutos. Estamos en C. de Ventura Rodríguez 5, muy cerca de la calle Princesa y de Plaza de España.', 'Uno o dos minutos. Estamos en C. de Ventura Rodríguez 5, a un paso de Plaza de los Cubos y muy cerca de Plaza de España.'),
    ('preparados al momento en C. de Ventura Rodríguez, 5, Madrid.', 'preparados al momento en C. de Ventura Rodríguez, 5, a un paso de Plaza de los Cubos y de Plaza de España.'),
    ('<span>C. de Ventura Rodríguez, 5 · 28008 Madrid</span>', '<span>C. de Ventura Rodríguez, 5 · Plaza de los Cubos · 28008 Madrid</span>'),
    ('>Antes o después del cine</a>', '>Sushi en Plaza de los Cubos</a>'),
    ('<a href="/sushi-cines-princesa/">Sushi y cine en Princesa</a>', '<a href="/sushi-cines-princesa/">Sushi en Plaza de los Cubos</a>'),
]
def patch_text(t):
    for a, b in R:
        t = t.replace(a, b)
    return t
def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt'))]
        for p in files:
            t = open(p, encoding='utf-8').read(); o = patch_text(t)
            if o != t: open(p, 'w', encoding='utf-8').write(o); n += 1
    print('patch_cubos: archivos cambiados', n)
if __name__ == '__main__': main(sys.argv[1:])

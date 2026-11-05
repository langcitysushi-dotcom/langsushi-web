# Enlaces de Google Maps → ficha buena de Lang City (CID 9612486309576316227), no la duplicada.
import os, sys
NEW = 'https://maps.google.com/?cid=9612486309576316227'
R = [
    ('https://www.google.com/maps/search/?api=1&amp;query=LANG%20CITY%20BAR%20%26%20RESTAURANT%2C%20Calle%20de%20Ventura%20Rodr%C3%ADguez%205%2C%2028008%20Madrid', NEW),
    ('https://www.google.com/maps/search/?api=1&query=LANG%20CITY%20BAR%20%26%20RESTAURANT%2C%20Calle%20de%20Ventura%20Rodr%C3%ADguez%205%2C%2028008%20Madrid', NEW),
    ('https://www.google.com/maps/search/?api=1&query=Lang%20City%20Bar%20%26%20Restaurant&query_place_id=ChIJZ2GOtLwpQg0RLNxM4PffHLg', NEW),
]
def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith(('.html', '.txt', '.py'))]
        for p in files:
            t = open(p, encoding='utf-8').read(); o = t
            for x, y in R: t = t.replace(x, y)
            if t != o: open(p, 'w', encoding='utf-8').write(t); n += 1
    print('patch_maps: archivos cambiados', n)
if __name__ == '__main__': main(sys.argv[1:])

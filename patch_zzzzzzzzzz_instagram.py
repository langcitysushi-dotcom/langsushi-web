# Genera las imagenes JPEG para Instagram en site/instagram/ (Instagram exige JPEG con URL publica).
# Usa las fotos de la carta (site/img/*.webp) y el logo. Nunca rompe la publicacion.
import os, sys, subprocess, urllib.request

POSTS = [
    ('p1_mudanza.jpg', '27B.webp', 'NUEVA DIRECCIÓN', 'Nos hemos mudado',
     ['C. de Ventura Rodríguez, 5', 'Entrada por Plaza de los Cubos'], ['Junto a Plaza de España · langsushi.es']),
    ('p2_lunes.jpg', 'C5.webp', 'DESDE EL 16 DE NOVIEMBRE', 'Abrimos todos los días',
     ['También los lunes', '12:00–17:00 · 19:30–24:00'], ['C. de Ventura Rodríguez, 5 · Plaza de los Cubos']),
    ('p3_buffet.jpg', '12A.webp', 'SUSHI · SASHIMI · DIM SUM', 'Buffet libre japonés',
     ['Desde 17,95 € a mediodía', 'Sushi, dim sum, wok y plancha al momento'], ['Pide desde la tablet de tu mesa']),
]
CAROUSEL = ['9A', '7', '3A', '41', 'C2']
FONTS = {
    'bold': 'https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.8/files/inter-latin-700-normal.woff',
    'semi': 'https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.8/files/inter-latin-600-normal.woff',
    'med': 'https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.8/files/inter-latin-500-normal.woff',
    'reg': 'https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.8/files/inter-latin-400-normal.woff',
}
FALLBACK = {'bold': 'DejaVuSans-Bold.ttf', 'semi': 'DejaVuSans-Bold.ttf', 'med': 'DejaVuSans.ttf', 'reg': 'DejaVuSans.ttf'}


def main(site):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        tgt = os.path.join(os.path.dirname(os.path.abspath(site)), '_pylib')
        for extra in (['--break-system-packages'], []):
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--target', tgt] + extra + ['pillow'], check=False)
            if os.path.isdir(os.path.join(tgt, 'PIL')):
                break
        sys.path.insert(0, tgt)
        import importlib; importlib.invalidate_caches()
        from PIL import Image, ImageDraw, ImageFont
    out = os.path.join(site, 'instagram')
    os.makedirs(out, exist_ok=True)
    fdir = os.path.join(out, '_f')
    os.makedirs(fdir, exist_ok=True)
    fpath = {}
    for k, u in FONTS.items():
        p = os.path.join(fdir, k + '.woff')
        try:
            urllib.request.urlretrieve(u, p)
            ft = ImageFont.truetype(p, 40)
            if ft.getmask('a').tobytes() == ft.getmask('b').tobytes():
                raise ValueError('fuente sin letras')
            fpath[k] = p
        except Exception:
            fpath[k] = FALLBACK[k]

    def F(k, s):
        try:
            return ImageFont.truetype(fpath[k], s)
        except Exception:
            return ImageFont.load_default()

    img = os.path.join(site, 'img')
    W, H = 1080, 1350
    BG = (250, 247, 242); INK = (28, 26, 24); RED = (190, 30, 45); GREY = (110, 104, 98)
    logo = Image.open(os.path.join(img, 'logo.webp')).convert('RGBA')

    def center(d, y, t, f, c):
        d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=c)

    for name, photo, tag, head, sub, small in POSTS:
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        lg = logo.copy(); lg.thumbnail((420, 95)); im.paste(lg, ((W - lg.width) // 2, 40), lg)
        p = Image.open(os.path.join(img, photo)).convert('RGB')
        p = p.resize((W, int(p.height * W / p.width)), Image.LANCZOS)
        if p.height > 740:
            c = (p.height - 740) // 2; p = p.crop((0, c, W, c + 740))
        im.paste(p, (0, 165)); y = 165 + p.height + 50
        f = F('semi', 30); tw = d.textlength(tag, font=f)
        d.rounded_rectangle(((W - tw) / 2 - 22, y, (W + tw) / 2 + 22, y + 54), 27, fill=RED)
        d.text(((W - tw) / 2, y + 9), tag, font=f, fill='white'); y += 78
        center(d, y, head, F('bold', 78), INK); y += 100
        for l in sub:
            center(d, y, l, F('med', 38), INK); y += 52
        y += 8
        for l in small:
            center(d, y, l, F('reg', 30), GREY); y += 42
        im.save(os.path.join(out, name), 'JPEG', quality=90)
    for n in CAROUSEL:
        p = Image.open(os.path.join(img, n + '.webp')).convert('RGB')
        p2 = p.resize((int(p.width * H / p.height), H), Image.LANCZOS); x = (p2.width - W) // 2
        p2.crop((x, 0, x + W, H)).save(os.path.join(out, 'c_' + n + '.jpg'), 'JPEG', quality=90)
    import shutil; shutil.rmtree(fdir, ignore_errors=True)
    print('patch_instagram: imagenes', sorted(f for f in os.listdir(out) if f.endswith('.jpg')))


if __name__ == '__main__':
    try:
        main((sys.argv[1:] or ['site'])[0])
    except Exception as e:
        print('patch_instagram: error (se ignora)', e)

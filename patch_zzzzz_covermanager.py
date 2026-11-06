# Reservas por CoverManager (06/11/2026): el módulo de CoverManager sustituye al formulario propio en la vista
# de reservas. El formulario antiguo se queda oculto (no se borra) para que el resto del JavaScript siga funcionando.
# Va el último. No hace nada si ya está aplicado.
import os, sys

MARK = 'id="cm-reservas"'
CM = ('<div class="formcard" id="cm-reservas" style="padding:0;overflow:hidden;background:#fff">'
      '<script src="https://www.covermanager.com/js/iframeResizer/iframeResizer.min.js"></script>'
      '<iframe id="restaurante-lang-city" title="Reservas Lang City" loading="lazy" '
      'src="https://www.covermanager.com/reservation/module_restaurant/restaurante-lang-city/spanish" '
      'allow="payment" frameborder="0" height="620" width="100%" style="display:block;border:0;min-height:550px" '
      'onload="if(window.iFrameResize){iFrameResize({checkOrigin:false},this)}"></iframe>'
      '<p class="note" style="margin:0;padding:10px 14px;font-size:13px">¿No se carga? Reserva en '
      '<a href="https://www.covermanager.com/reservation/module_restaurant/restaurante-lang-city/spanish" target="_blank" rel="noopener" style="color:inherit">CoverManager</a> '
      'o llámanos al <a href="tel:+34919414881" style="color:inherit">919 41 48 81</a>.</p></div>'
      '<style>#rBook,#rDemo,#rAviso,#resDone{display:none!important}</style>\n        ')

R = [
    ('<div class="formcard rbook" id="rBook">', CM + '<div class="formcard rbook" id="rBook">'),
    ('Elige cuántos sois, el día y una hora libre. La confirmación es al momento.',
     'Elige cuántos sois, el día y la hora. Recibirás la confirmación por email.'),
    ('Para verla o cancelarla usa el enlace de tu email de confirmación, o abre «Mis pedidos y reservas» abajo en la web si la hiciste desde este móvil.',
     'Para verla, cambiarla o cancelarla usa el enlace del email de confirmación de CoverManager, o llámanos al 919 41 48 81.'),
]

def patch_text(t):
    if MARK in t:
        return t
    for a, b in R:
        t = t.replace(a, b, 1) if a == R[0][0] else t.replace(a, b)
    return t

def main(args):
    n = 0
    for a in args or ['site']:
        files = [a] if os.path.isfile(a) else [os.path.join(r, f) for r, _, fs in os.walk(a) for f in fs if f.endswith('.html')]
        for p in files:
            if '/admin/' in p:
                continue
            t = open(p, encoding='utf-8').read(); o = patch_text(t)
            if o != t:
                open(p, 'w', encoding='utf-8').write(o); n += 1
    print('patch_covermanager: archivos cambiados', n)

if __name__ == '__main__':
    main(sys.argv[1:])

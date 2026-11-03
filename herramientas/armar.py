import json, os, html, sys
# Genera las páginas de sitio/ a partir de paginas.py.  Uso: python3 herramientas/armar.py
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, '..', 'sitio')
DOMINIO = 'https://cuentasclaro.com'
URLS = []
SITE = 'Cuentas Claras'

def page(path, title, desc, body, faq=None, script='', home=False, nombre=''):
    depth = 0 if path == '' else path.count('/') + 1
    up = '../' * depth
    faq_html, ld = '', ''
    if faq:
        faq_html = '<h2>Preguntas frecuentes</h2>' + ''.join(
            f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
        ld = '<script type="application/ld+json">' + json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]
        }, ensure_ascii=False) + '</script>'
    crumb = '' if home else f'<div class="crumb"><a href="{up}">Inicio</a> › {html.escape(nombre)}</div>'
    full_title = title if home else f'{title} | {SITE}'
    url = DOMINIO + '/' + (path + '/' if path else '')
    URLS.append(url)
    doc = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_AR">
<meta name="theme-color" content="#0f7b5f">
<link rel="icon" href="{up}icono.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}estilo.css">
{ld}
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="{up}">Cuentas<span>Claras</span></a>
<nav><a href="{up}#calculadoras">Calculadoras</a></nav>
</div></header>
<main><div class="wrap">
{crumb}
{body}
<div class="ad"></div>
{faq_html}
</div></main>
<footer class="bottom"><div class="wrap">
<p><a href="{up}">Inicio</a><a href="{up}acerca/">Acerca de</a><a href="{up}privacidad/">Privacidad</a></p>
<p>© <span data-anio></span> {SITE}. Los resultados son estimaciones orientativas y no reemplazan el asesoramiento de un contador o abogado.</p>
</div></footer>
<script src="{up}comun.js"></script>
{('<script>' + script + '</script>') if script else ''}
</body>
</html>
'''
    out = os.path.join(BASE, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)

exec(open(os.path.join(AQUI, 'paginas.py')).read())

# sitemap.xml y robots.txt
open(os.path.join(BASE, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in URLS) + '</urlset>\n')
open(os.path.join(BASE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n')
print(len(URLS), 'páginas generadas')

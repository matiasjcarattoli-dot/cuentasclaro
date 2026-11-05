import json, os, html, urllib.parse
# Genera las páginas de sitio/ a partir de paginas.py.  Uso: python3 herramientas/armar.py
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, '..', 'sitio')
DOMINIO = 'https://cuentasclaro.com'
SITE = 'Cuentas Claras'
ADSENSE = 'ca-pub-1125850479848811'
URLS = []

# ---------- Catálogo: de acá salen la portada, el menú y las relacionadas ----------
CATEGORIAS = [
    ('trabajo', 'Trabajo, sueldo e impuestos', 'Lo que cobrás, lo que te deben, monotributo y fechas.'),
    ('ahorro', 'Ahorro, inversión y préstamos', 'Hacé rendir tu plata y sabé cuánto te cuesta financiarte.'),
    ('compras', 'Compras, precios e inflación', 'Cuotas, IVA, porcentajes, alquiler y dólar.'),
    ('utiles', 'Herramientas para el día a día', 'Viajes, gastos compartidos, horas y cuentas rápidas.'),
]
CALCS = [
    # slug, nombre corto, descripción de la tarjeta, ícono, categoría
    ('sueldo-neto', 'Sueldo neto', 'Cuánto cobrás en mano a partir del bruto.', 'billete', 'trabajo'),
    ('aguinaldo', 'Aguinaldo (SAC)', 'Completo o proporcional, con fechas de pago.', 'regalo', 'trabajo'),
    ('vacaciones', 'Vacaciones', 'Días que te corresponden y cuánto te pagan.', 'sol', 'trabajo'),
    ('indemnizacion', 'Indemnización por despido', 'Tu liquidación final, rubro por rubro.', 'documento', 'trabajo'),
    ('horas-extra', 'Horas extra', 'Al 50 % y al 100 %, con el valor de tu hora.', 'reloj', 'trabajo'),
    ('monotributo', 'Monotributo', 'En qué categoría estás y cuánto pagás por mes.', 'recibo', 'trabajo'),
    ('empleada-domestica', 'Sueldo de empleada doméstica', 'Sueldo por hora o por mes según la categoría.', 'casa', 'trabajo'),
    ('dias-habiles', 'Días hábiles', 'Días hábiles entre dos fechas, con los feriados.', 'calendario', 'trabajo'),
    ('jubilacion', 'Jubilación, bono y aguinaldo', 'Haber, bono de ANSES y medio aguinaldo de jubilados.', 'regalo', 'trabajo'),
    ('sueldo-por-hora', 'Sueldo por hora', 'Cuánto ganás por hora, por día y por semana.', 'reloj', 'trabajo'),
    ('sueldo-bruto', 'Sueldo bruto desde el neto', 'Cuánto tiene que ser el bruto para cobrar X en mano.', 'billete', 'trabajo'),
    ('precio-de-venta', 'Precio de venta', 'Para emprendedores: costo, ganancia, comisiones e IVA.', 'etiqueta', 'trabajo'),
    ('plazo-fijo', 'Plazo fijo', 'Intereses, TEA y si le gana a la inflación.', 'banco', 'ahorro'),
    ('plazo-fijo-uva', 'Plazo fijo UVA', 'Cuánto rinde ajustado por inflación y si conviene.', 'banco', 'ahorro'),
    ('cuenta-remunerada', 'Cuenta remunerada', 'Cuánto te rinde la plata en una billetera virtual.', 'billete', 'ahorro'),
    ('credito-hipotecario-uva', 'Crédito hipotecario UVA', 'Cuota inicial, ingreso necesario y cómo sube.', 'casa', 'ahorro'),
    ('interes-compuesto', 'Interés compuesto y ahorro', 'Cuánto juntás ahorrando todos los meses.', 'grafico', 'ahorro'),
    ('prestamo', 'Préstamo personal', 'Cuota mensual, intereses y cuadro de pagos.', 'mano', 'ahorro'),
    ('ahorro-objetivo', 'Meta de ahorro', 'Cuánto ahorrar por mes para llegar a tu objetivo.', 'objetivo', 'ahorro'),
    ('tasas', 'Conversor de tasas', 'Pasá de TNA a TEA y a tasa mensual (TEM).', 'grafico', 'ahorro'),
    ('cuotas', '¿Cuotas o contado?', 'Qué conviene según la inflación.', 'tarjeta', 'compras'),
    ('inflacion', 'Inflación acumulada', 'Cuánto subieron los precios y cuánto vale hoy tu plata.', 'termometro', 'compras'),
    ('alquiler', 'Aumento de alquiler', 'Cuánto vas a pagar con la próxima actualización.', 'casa', 'compras'),
    ('iva', 'IVA', 'Agregá o sacá el IVA de un precio (21 %, 10,5 %, 27 %).', 'recibo', 'compras'),
    ('porcentajes', 'Porcentajes', 'Descuentos, aumentos y variaciones al instante.', 'porcentaje', 'compras'),
    ('dolar', 'Dólar hoy', 'Cotizaciones y conversor pesos ⇄ dólares.', 'dolar', 'compras'),
    ('costo-viaje', 'Costo de un viaje en auto', 'Nafta y peajes, y cuánto pone cada uno.', 'auto', 'utiles'),
    ('dividir-gastos', 'Dividir gastos', 'Quién le debe a quién después de una salida o viaje.', 'personas', 'utiles'),
    ('horas-trabajadas', 'Horas trabajadas', 'Sumá tus horarios de entrada y salida.', 'reloj', 'utiles'),
    ('edad', 'Calcular edad', 'Años, meses y días exactos, y tu próximo cumpleaños.', 'regalo', 'utiles'),
    ('dias-entre-fechas', 'Días entre fechas', 'Días corridos entre dos fechas o sumar días.', 'calendario', 'utiles'),
    ('consumo-electrico', 'Consumo eléctrico', 'Cuánto gasta de luz cada electrodoméstico.', 'rayo', 'utiles'),
    ('regla-de-tres', 'Regla de tres', 'Simple directa e inversa, al instante.', 'cambio', 'utiles'),
]
NOMBRES = {c[0]: c[1] for c in CALCS}
GUIAS = [
    # slug (dentro de guias/), título corto, descripción, calculadoras relacionadas
    ('feriados-2026', 'Feriados 2026 en Argentina', 'Calendario completo, fines de semana largos y los que quedan en el año.', ['dias-habiles', 'vacaciones', 'horas-extra']),
    ('aguinaldo-diciembre-2026', 'Aguinaldo de diciembre 2026', 'Cuándo se cobra, cómo se calcula y ejemplos con números.', ['aguinaldo', 'sueldo-neto', 'vacaciones']),
    ('como-calcular-indemnizacion', 'Cómo calcular la indemnización por despido', 'Qué te corresponde rubro por rubro si te despiden sin causa.', ['indemnizacion', 'vacaciones', 'aguinaldo']),
    ('cuotas-o-contado', '¿Conviene pagar en cuotas o de contado?', 'Cómo decidir con inflación, cuotas sin interés y descuentos.', ['cuotas', 'inflacion', 'prestamo']),
    ('sueldo-bruto-y-neto', 'Sueldo bruto y neto: diferencias', 'Qué te descuentan del sueldo y cómo leer tu recibo.', ['sueldo-neto', 'sueldo-bruto', 'aguinaldo']),
    ('tna-tea-cft', 'TNA, TEA, TEM y CFT explicados', 'Qué significa cada tasa y cómo compararlas.', ['tasas', 'plazo-fijo', 'prestamo']),
    ('vacaciones-cuantos-dias', 'Vacaciones: cuántos días te corresponden', 'Días por antigüedad, cuándo se toman y cómo se pagan.', ['vacaciones', 'dias-habiles', 'aguinaldo']),
    ('que-hacer-si-me-despiden', 'Qué hacer si te despiden', 'Los pasos para cobrar todo lo que te corresponde.', ['indemnizacion', 'vacaciones', 'dias-habiles']),
    ('licencias-por-ley', 'Licencias laborales por ley', 'Días por matrimonio, nacimiento, examen, enfermedad y más.', ['vacaciones', 'dias-habiles', 'sueldo-neto']),
    ('como-pedir-un-aumento', 'Cómo pedir un aumento de sueldo', 'Cuándo, cuánto y cómo pedirlo, con números.', ['inflacion', 'sueldo-bruto', 'sueldo-neto']),
    ('credito-hipotecario-uva', 'Cómo funciona el crédito hipotecario UVA', 'Qué es, cómo sube la cuota y qué riesgos tiene.', ['credito-hipotecario-uva', 'inflacion', 'ahorro-objetivo']),
    ('donde-tener-los-ahorros', 'Dónde tener tus ahorros en pesos', 'Cuenta remunerada, plazo fijo, UVA y fondos: diferencias.', ['cuenta-remunerada', 'plazo-fijo', 'plazo-fijo-uva']),
    ('resumen-tarjeta-de-credito', 'Cómo leer el resumen de la tarjeta', 'Pago mínimo, intereses, cierre y vencimiento explicados.', ['cuotas', 'prestamo', 'tasas']),
    ('recategorizacion-monotributo', 'Recategorización del monotributo', 'Cuándo y cómo recategorizarte, paso a paso.', ['monotributo', 'precio-de-venta', 'iva']),
]

# Íconos de línea propios (24×24, trazo), así se ven igual en todos los dispositivos.
P = {
    'billete': '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9.5v5M18 9.5v5"/>',
    'regalo': '<rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5V20h14v-7.5M12 8.5V20M12 8.5c-1.5-3-5.5-3.5-5.5-1S10 8.5 12 8.5zm0 0c1.5-3 5.5-3.5 5.5-1S14 8.5 12 8.5z"/>',
    'sol': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>',
    'documento': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    'reloj': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'banco': '<path d="M3 9.5 12 4l9 5.5M4.5 10v8M9.5 10v8M14.5 10v8M19.5 10v8M3 20.5h18"/>',
    'grafico': '<path d="M3.5 20.5h17M5 16l4.5-5 3.5 3 6-7"/><path d="M15 7h4v4"/>',
    'mano': '<path d="M3 15.5h3l3.5 2.5h5a1.5 1.5 0 0 0 0-3H11"/><path d="M6 15.5V20H3M14.5 15l4-2.5a1.5 1.5 0 0 1 2 2.2L15 19.5H9.5"/><circle cx="14" cy="7" r="3"/>',
    'tarjeta': '<rect x="2.5" y="5.5" width="19" height="13" rx="2"/><path d="M2.5 10h19M6 14.5h4"/>',
    'termometro': '<path d="M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    'casa': '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5M10 20v-5.5h4V20"/>',
    'recibo': '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    'porcentaje': '<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    'dolar': '<circle cx="12" cy="12" r="8.5"/><path d="M14.8 9.2c-.4-1-1.5-1.7-2.8-1.7-1.6 0-2.8.9-2.8 2.1 0 2.9 5.8 1.6 5.8 4.6 0 1.2-1.3 2.1-3 2.1-1.4 0-2.6-.7-3-1.8M12 6v1.5M12 16.5V18"/>',
    'calculadora': '<rect x="5" y="2.5" width="14" height="19" rx="2"/><rect x="8" y="5.5" width="8" height="3.5" rx=".5"/><path d="M8.5 12.5h.01M12 12.5h.01M15.5 12.5h.01M8.5 15.5h.01M12 15.5h.01M15.5 15.5h.01M8.5 18.5h.01M12 18.5h.01M15.5 18.5h.01"/>',
    'escudo': '<path d="M12 3 4.5 6v5.5c0 4.5 3.2 8 7.5 9.5 4.3-1.5 7.5-5 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    'lupa': '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    'calendario': '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 13.5h.01M12 13.5h.01M16 13.5h.01M8 17h.01M12 17h.01"/>',
    'libro': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5M8 7.5h8M8 11h6"/>',
    'etiqueta': '<path d="M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7l8.3 8.3a1.5 1.5 0 0 1 0 2.1l-6.4 6.4a1.5 1.5 0 0 1-2.1 0z"/><circle cx="8" cy="8" r="1.5"/>',
    'auto': '<path d="M5 16.5H3.5v-4l2-5h13l2 5v4H19"/><path d="M3.5 12.5h17M9 16.5h6"/><circle cx="7" cy="16.5" r="2"/><circle cx="17" cy="16.5" r="2"/>',
    'personas': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8 0 5 2.3 5 5.3"/>',
    'cambio': '<path d="M4 8h13l-3.5-3.5M20 16H7l3.5 3.5"/>',
    'objetivo': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    'compartir': '<circle cx="18" cy="5.5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/><path d="m8.2 10.8 7.6-4M8.2 13.2l7.6 4"/>',
    'rayo': '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
}
def icono(nombre, cls='ico'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[nombre]}</svg>')

def tarjeta(c, up):
    slug, nombre, desc, ico, _ = c
    return (f'<a class="tile" href="{up}{slug}/"><span class="tile-ico">{icono(ico)}</span>'
            f'<span class="tile-txt"><strong>{html.escape(nombre)}</strong><span>{html.escape(desc)}</span></span>'
            f'<svg class="tile-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg></a>')

def tarjeta_guia(g, up):
    return tarjeta((f'guias/{g[0]}', g[1], g[2], 'libro', ''), up)

def page(path, title, desc, body, faq=None, script='', home=False, nombre='', relacionadas=None, articulo=False):
    depth = 0 if path == '' else path.count('/') + 1
    up = '../' * depth
    faq_html, ld = '', ''
    if faq:
        faq_html = '<section class="faq"><h2>Preguntas frecuentes</h2>' + ''.join(
            f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq) + '</section>'
        ld = '<script type="application/ld+json">' + json.dumps({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]
        }, ensure_ascii=False) + '</script>'
    medio = f'<a href="{up}guias/">Guías</a><span>›</span>' if path.startswith('guias/') else ''
    if articulo:
        ld += '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'Article', 'headline': title,
              'description': desc, 'inLanguage': 'es-AR', 'dateModified': '2026-11-04', 'mainEntityOfPage': DOMINIO + '/' + path + '/',
              'publisher': {'@type': 'Organization', 'name': SITE}}, ensure_ascii=False) + '</script>'
    crumb = '' if home else f'<nav class="crumb" aria-label="Ruta"><a href="{up}">Inicio</a><span>›</span>{medio}{html.escape(nombre)}</nav>'
    full_title = title if home else f'{title} | {SITE}'
    url = DOMINIO + '/' + (path + '/' if path else '')
    URLS.append(url)

    # Calculadoras relacionadas (misma categoría primero)
    rel = ''
    actual = next((c for c in CALCS if c[0] == path), None)
    if relacionadas:
        cs = [c for s2 in relacionadas for c in CALCS if c[0] == s2]
        rel = '<section class="related"><h2>Calculadoras relacionadas</h2><div class="grid">' + ''.join(tarjeta(c, up) for c in cs) + '</div></section>'
    elif actual:
        misma = [c for c in CALCS if c[4] == actual[4] and c[0] != path]
        otras = [c for c in CALCS if c[4] != actual[4]]
        elegidas = (misma + otras)[:4]
        rel = '<section class="related"><h2>Otras calculadoras</h2><div class="grid">' + ''.join(tarjeta(c, up) for c in elegidas) + '</div></section>'

    texto = urllib.parse.quote(f'{title.split(":")[0]} {url}')
    compartir = ('' if path in ('privacidad', 'acerca', 'guias') else
        f'<div class="share"><span>¿Te sirvió? Compartilo</span>'
        f'<a class="btn wa" href="https://wa.me/?text={texto}" target="_blank" rel="noopener">WhatsApp</a>'
        f'<button class="btn" type="button" data-compartir data-url="{url}" data-titulo="{html.escape(title)}">{icono("compartir")}Compartir</button></div>')
    menu = ''.join(f'<a href="{up}#{k}">{html.escape(n.split(",")[0])}</a>' for k, n, _ in CATEGORIAS) + f'<a href="{up}guias/">Guías</a>'
    pie_guias = ''.join(f'<li><a href="{up}guias/{g[0]}/">{html.escape(g[1])}</a></li>' for g in GUIAS)
    pie_calcs = ''.join(f'<li><a href="{up}{c[0]}/">{html.escape(c[1])}</a></li>' for c in CALCS)
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
<meta property="og:site_name" content="{SITE}">
<meta property="og:image" content="{DOMINIO}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b7a5c">
<link rel="icon" href="{up}icono.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}estilo.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>
{ld}
</head>
<body{' class="home"' if home else ''}>
<header class="top"><div class="wrap">
<a class="logo" href="{up}"><span class="logo-mark">{icono('calculadora')}</span><span class="logo-txt">Cuentas<b>Claras</b></span></a>
<nav class="menu">{menu}</nav>
</div></header>
<main>
{body if home else f'<div class="wrap page">{crumb}{body}{compartir}<div class="ad"></div>{faq_html}{rel}</div>'}
</main>
<footer class="bottom"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="{up}"><span class="logo-mark">{icono('calculadora')}</span><span class="logo-txt">Cuentas<b>Claras</b></span></a>
<p>Calculadoras gratis para las cuentas de todos los días en Argentina. Sin registrarte y sin guardar tus datos.</p></div>
<div><h3>Calculadoras</h3><ul class="foot-list">{pie_calcs}</ul></div>
<div><h3>Guías</h3><ul>{pie_guias}</ul><h3 class="mt">El sitio</h3><ul><li><a href="{up}acerca/">Acerca de</a></li><li><a href="{up}privacidad/">Privacidad</a></li></ul></div>
</div>
<p class="legal">© <span data-anio></span> {SITE}. Los resultados son estimaciones orientativas y no reemplazan el asesoramiento de un contador o abogado.</p>
</div></footer>
<script src="{up}comun.js"></script>
{('<script>' + script + '</script>') if script else ''}
</body>
</html>
'''
    out = os.path.join(BASE, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)

def portada():
    secciones = ''
    for k, n, d in CATEGORIAS:
        cs = [c for c in CALCS if c[4] == k]
        secciones += (f'<section class="cat" id="{k}"><div class="cat-head"><h2>{html.escape(n)}</h2><p>{html.escape(d)}</p></div>'
                      f'<div class="grid">' + ''.join(tarjeta(c, '') for c in cs) + '</div></section>')
    chips = ''.join(f'<a href="{c[0]}/">{html.escape(c[1])}</a>' for c in CALCS[:6])
    body = f'''<section class="hero"><div class="wrap">
<p class="eyebrow">Calculadoras para Argentina · Gratis</p>
<h1>Hacé tus cuentas<br><span>en segundos.</span></h1>
<p class="lead">Sueldo, aguinaldo, indemnización, plazo fijo, préstamos, inflación y más. Resultados al instante, con el detalle de cada número.</p>
<label class="search">{icono('lupa', 'search-ico')}<input id="buscar" type="search" placeholder="Buscá una calculadora… (ej: aguinaldo)" autocomplete="off" aria-label="Buscar calculadora"></label>
<div class="chips">{chips}</div>
</div></section>
<div class="wrap">
<div class="features">
<div>{icono('rayo')}<strong>Al instante</strong><span>El resultado cambia mientras escribís.</span></div>
<div>{icono('escudo')}<strong>Privado</strong><span>Todo se calcula en tu dispositivo.</span></div>
<div>{icono('documento')}<strong>Explicado</strong><span>Te mostramos de dónde sale cada número.</span></div>
</div>
<div class="ad"></div>
<div id="calculadoras">{secciones}</div>
<section class="cat" id="guias"><div class="cat-head"><h2>Guías</h2><p>Explicaciones claras de los temas que más se consultan.</p></div><div class="grid">{''.join(tarjeta_guia(g, '') for g in GUIAS)}</div></section>
<p id="sin-resultados" class="note" hidden>No encontramos esa calculadora. Probá con otra palabra.</p>
<section class="article home-text">
<h2>Cuentas claras, sin vueltas</h2>
<p>Cada calculadora te muestra el resultado al instante mientras escribís, con el detalle de cada número para que entiendas de dónde sale. No guardamos tus datos: todo se calcula en tu propio celular o computadora.</p>
<p>Usamos las reglas de la Ley de Contrato de Trabajo y las fórmulas que usan los bancos. Aun así, cada caso tiene particularidades (convenios colectivos, adicionales, impuesto a las ganancias), así que tomá los resultados como una guía.</p>
</section>
</div>'''
    script = '''
const q = document.getElementById('buscar'), sin = document.getElementById('sin-resultados');
const norm = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
q.addEventListener('input', () => {
  const t = norm(q.value.trim()); let n = 0;
  document.querySelectorAll('#calculadoras .tile').forEach(a => { const ok = !t || norm(a.textContent).includes(t); a.hidden = !ok; if (ok) n++; });
  document.querySelectorAll('#calculadoras .cat').forEach(s => s.hidden = !s.querySelector('.tile:not([hidden])'));
  sin.hidden = n > 0;
});
'''
    page('', 'Cuentas Claras: calculadoras de sueldo, aguinaldo, indemnización, plazo fijo y más (Argentina)',
         'Calculadoras gratis para Argentina: sueldo neto, aguinaldo, vacaciones, indemnización, horas extra, plazo fijo, préstamos, inflación, alquiler, IVA, cuotas y dólar. Rápidas y sin registrarte.',
         body, home=True, script=script)

portada()
page('guias', 'Guías sobre sueldo, aguinaldo, feriados y finanzas personales',
     'Guías claras sobre aguinaldo, indemnización, feriados, cuotas y más temas de plata y trabajo en Argentina.',
     '<h1>Guías</h1><p class="lead">Explicaciones claras, con ejemplos, de los temas de plata y trabajo que más se consultan.</p><div class="grid">'
     + ''.join(tarjeta_guia(g, '../') for g in GUIAS) + '</div>', nombre='Guías')
exec(open(os.path.join(AQUI, 'paginas.py'), encoding='utf-8').read())

# sitemap.xml y robots.txt
with open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in URLS) + '</urlset>\n')
with open(os.path.join(BASE, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n')
print(len(URLS), 'páginas generadas')

# Cuentas Claras — cuentasclaro.com

Sitio de calculadoras para Argentina (sueldo, aguinaldo, vacaciones, indemnización, horas extra, plazo fijo, interés compuesto, préstamos, cuotas, inflación, alquiler, IVA, porcentajes y dólar), financiado con Google AdSense.

## Estructura

- `sitio/` — lo que se publica en https://cuentasclaro.com (GitHub Pages, ver `.github/workflows/pages.yml`).
- `herramientas/armar.py` — también tiene el catálogo (`CALCS`): nombre, ícono y categoría de cada calculadora, que arma la portada, el pie y las relacionadas.
- `herramientas/paginas.py` — el contenido de cada página (texto, preguntas frecuentes y el JavaScript de cada calculadora).
- `herramientas/armar.py` — arma las páginas de `sitio/`, el `sitemap.xml` y el `robots.txt`.

Para cambiar o agregar una calculadora: editar `herramientas/paginas.py` y correr

```sh
python3 herramientas/armar.py
```

## Anuncios

El código de AdSense (`ca-pub-1125850479848811`) lo agrega `herramientas/armar.py` en el `<head>` de cada página, y `sitio/ads.txt` autoriza a Google a vender los anuncios. Los anuncios son automáticos: se ajustan desde el panel de AdSense.

## Probar localmente

```sh
cd sitio && python3 -m http.server 8000
```

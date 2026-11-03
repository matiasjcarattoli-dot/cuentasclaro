# Cuentas Claras — cuentasclaro.com

Sitio de calculadoras para Argentina (sueldo neto, aguinaldo, vacaciones, indemnización, horas extra, plazo fijo, cuotas o contado y dólar hoy), financiado con Google AdSense.

## Estructura

- `sitio/` — lo que se publica en https://cuentasclaro.com (GitHub Pages, ver `.github/workflows/pages.yml`).
- `herramientas/paginas.py` — el contenido de cada página (texto, preguntas frecuentes y el JavaScript de cada calculadora).
- `herramientas/armar.py` — arma las páginas de `sitio/`, el `sitemap.xml` y el `robots.txt`.

Para cambiar o agregar una calculadora: editar `herramientas/paginas.py` y correr

```sh
python3 herramientas/armar.py
```

## Anuncios

En `sitio/comun.js`, poner el ID de AdSense en `ADSENSE_CLIENT` (`ca-pub-...`) y crear `sitio/ads.txt` con la línea que da AdSense.

## Probar localmente

```sh
cd sitio && python3 -m http.server 8000
```

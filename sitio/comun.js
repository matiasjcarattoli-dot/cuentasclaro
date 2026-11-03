// ===== Configuración de anuncios =====
// Cuando Google AdSense apruebe el sitio, pegá acá tu ID de editor (ej: 'ca-pub-1234567890123456').
// Los anuncios aparecen solos en cada <div class="ad"> de las páginas. Vacío = sin anuncios.
const ADSENSE_CLIENT = '';

(function cargarAnuncios() {
  if (!ADSENSE_CLIENT) return;
  const s = document.createElement('script');
  s.async = true;
  s.crossOrigin = 'anonymous';
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_CLIENT;
  document.head.appendChild(s);
  document.querySelectorAll('.ad').forEach(slot => {
    const ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.display = 'block';
    ins.setAttribute('data-ad-client', ADSENSE_CLIENT);
    ins.setAttribute('data-ad-format', 'auto');
    ins.setAttribute('data-full-width-responsive', 'true');
    slot.appendChild(ins);
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  });
})();

// ===== Utilidades =====
const $ = s => document.querySelector(s);
const pesos = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 2 });
const dolares = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 });
const num = new Intl.NumberFormat('es-AR', { maximumFractionDigits: 2 });
const $$ = n => pesos.format(isFinite(n) ? n : 0);
const pct = n => num.format(n) + ' %';
const val = id => { const v = parseFloat(String($('#' + id).value).replace(',', '.')); return isFinite(v) ? v : 0; };

function filas(rows) {
  return '<table class="detail">' + rows.map(([a, b, cls]) =>
    `<tr${cls ? ` class="${cls}"` : ''}><td>${a}</td><td>${b}</td></tr>`).join('') + '</table>';
}

// Recuerda lo que escribió la persona (solo en su navegador) y recalcula al cambiar algo.
function conectar(calcular) {
  const campos = document.querySelectorAll('.calc input, .calc select');
  const clave = 'calc:' + location.pathname;
  try {
    const guardado = JSON.parse(localStorage.getItem(clave) || '{}');
    campos.forEach(c => {
      if (!(c.id in guardado)) return;
      if (c.type === 'checkbox') c.checked = guardado[c.id]; else c.value = guardado[c.id];
    });
  } catch (e) {}
  const correr = () => {
    calcular();
    try {
      const datos = {};
      campos.forEach(c => { if (c.id) datos[c.id] = c.type === 'checkbox' ? c.checked : c.value; });
      localStorage.setItem(clave, JSON.stringify(datos));
    } catch (e) {}
  };
  campos.forEach(c => c.addEventListener('input', correr));
  correr();
}

document.querySelectorAll('[data-anio]').forEach(e => e.textContent = new Date().getFullYear());

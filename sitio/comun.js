// ===== Anuncios =====
// El código de Google AdSense (ca-pub-1125850479848811) va en el <head> de cada página,
// lo agrega herramientas/armar.py. Los anuncios los ubica Google solo (anuncios automáticos),
// y se activan o ajustan desde el panel de AdSense.

// ===== Utilidades =====
const $ = s => document.querySelector(s);
const pesos = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 2 });
const dolares = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 });
const num = new Intl.NumberFormat('es-AR', { maximumFractionDigits: 2 });
const $$ = n => pesos.format(isFinite(n) ? n : 0);
const pct = n => num.format(n) + ' %';
const val = id => { const v = parseFloat(String($('#' + id).value).replace(',', '.')); return isFinite(v) ? v : 0; };

// Lee una lista de números (uno por línea; acepta coma decimal: 2,5).
const lista = id => String($('#' + id).value).split(/[\n;\s]+/).map(x => parseFloat(x.replace('%', '').replace(',', '.'))).filter(isFinite);
// Muestra solo los campos del modo elegido: <div data-modo="x">.
const modos = (sel) => document.querySelectorAll('[data-modo]').forEach(e => e.hidden = e.dataset.modo !== $(sel).value);

function filas(rows) {
  return '<table class="detail">' + rows.map(([a, b, cls]) =>
    `<tr${cls ? ` class="${cls}"` : ''}><td>${a}</td><td>${b}</td></tr>`).join('') + '</table>';
}

// Recuerda lo que escribió la persona (solo en su navegador) y recalcula al cambiar algo.
function conectar(calcular) {
  const campos = document.querySelectorAll('.calc input, .calc select, .calc textarea');
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

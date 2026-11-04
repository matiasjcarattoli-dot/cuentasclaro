# ---------- SUELDO NETO ----------
page('sueldo-neto', 'Calculadora de sueldo neto en Argentina: de bruto a neto',
 'Calculá tu sueldo neto (en mano) a partir del bruto: jubilación 11 %, PAMI 3 %, obra social 3 % y sindicato. Gratis y al instante.',
 nombre='Sueldo neto', body='''
<h1>Calculadora de sueldo neto</h1>
<p class="lead">Poné tu sueldo bruto y te decimos cuánto cobrás en mano, con el detalle de cada descuento.</p>
<div class="card calc">
<label>Sueldo bruto mensual ($)<input id="bruto" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Aporte sindical (%) <small>0 si no estás afiliado</small><input id="sind" type="number" inputmode="decimal" min="0" step="0.1" value="0"></label>
<label>Tope de aportes ($) <small>opcional, 0 = sin tope</small><input id="tope" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el sueldo neto?</h2>
<p>Si trabajás en relación de dependencia, a tu sueldo bruto se le descuentan los <strong>aportes obligatorios</strong>, que suman un 17 %:</p>
<ul>
<li><strong>Jubilación (SIPA): 11 %</strong>.</li>
<li><strong>Ley 19.032 (PAMI): 3 %</strong>.</li>
<li><strong>Obra social: 3 %</strong>.</li>
</ul>
<p>Si estás afiliado a un sindicato, se suma la <strong>cuota sindical</strong> (en general entre 2 % y 3 %, según el convenio). Lo que queda es tu <strong>sueldo neto</strong>, el que te depositan.</p>
<h3>Ejemplo</h3>
<p>Con un bruto de $1.000.000 y sin sindicato: 11 % de jubilación ($110.000) + 3 % de PAMI ($30.000) + 3 % de obra social ($30.000) = $170.000 de descuentos. Neto: <strong>$830.000</strong>.</p>
<h3>El tope de aportes</h3>
<p>Los aportes se calculan sobre el sueldo hasta un máximo llamado <em>base imponible máxima</em>, que ARCA (ex AFIP) actualiza periódicamente. Si tu sueldo es muy alto, podés cargar ese tope para que el cálculo sea exacto.</p>
</div>
''', faq=[
 ('¿Qué porcentaje se descuenta del sueldo bruto?', 'En relación de dependencia se descuenta el 17 %: 11 % de jubilación, 3 % de PAMI (Ley 19.032) y 3 % de obra social. Si estás afiliado a un sindicato se suma la cuota sindical.'),
 ('¿Esta calculadora incluye el impuesto a las ganancias?', 'No. Ganancias depende de tus deducciones personales (cónyuge, hijos, alquiler, etc.) y solo alcanza a sueldos altos. Si te corresponde, tu neto será menor.'),
 ('¿El sueldo bruto incluye horas extra y adicionales?', 'Sí: el bruto es la suma de todos los conceptos remunerativos (básico, antigüedad, presentismo, horas extra). Los conceptos no remunerativos no llevan aportes jubilatorios.'),
], script='''
conectar(() => {
  const bruto = val('bruto'), tope = val('tope'), sind = val('sind');
  const base = tope > 0 ? Math.min(bruto, tope) : bruto;
  const jub = base * .11, pami = base * .03, os = base * .03, s = bruto * sind / 100;
  const desc = jub + pami + os + s, neto = bruto - desc;
  $('#res').innerHTML = `<div class="label">Sueldo neto (en mano)</div><div class="big">${$$(neto)}</div>` + filas([
    ['Sueldo bruto', $$(bruto)],
    ['Jubilación (11 %)', '− ' + $$(jub)],
    ['PAMI, Ley 19.032 (3 %)', '− ' + $$(pami)],
    ['Obra social (3 %)', '− ' + $$(os)],
    ...(s ? [['Sindicato (' + pct(sind) + ')', '− ' + $$(s)]] : []),
    ['Total de descuentos', '− ' + $$(desc)],
    ['Sueldo neto', $$(neto), 'total'],
  ]) + '<p class="note">No incluye impuesto a las ganancias.</p>';
});
''')

# ---------- AGUINALDO ----------
page('aguinaldo', 'Calculadora de aguinaldo (SAC): completo y proporcional',
 'Calculá tu aguinaldo de junio o diciembre: completo o proporcional por días trabajados, bruto y neto. Con fechas de pago del SAC.',
 nombre='Aguinaldo', body='''
<h1>Calculadora de aguinaldo</h1>
<p class="lead">El aguinaldo (sueldo anual complementario) es la mitad de tu mejor sueldo del semestre. Calculalo completo o proporcional.</p>
<div class="card calc">
<label>Mejor sueldo bruto del semestre ($)<input id="mejor" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Semestre<select id="sem"><option value="1">1.º (enero a junio)</option><option value="2">2.º (julio a diciembre)</option></select></label>
<label>Año<input id="anio" type="number" min="2000" max="2100"></label>
</div>
<div class="row">
<label>Fecha de ingreso <small>si entraste durante el semestre</small><input id="ini" type="date"></label>
<label>Fecha de egreso <small>si te fuiste durante el semestre</small><input id="fin" type="date"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el aguinaldo?</h2>
<p>Según la Ley de Contrato de Trabajo, el aguinaldo equivale al <strong>50 % de la mayor remuneración mensual</strong> que cobraste en cada semestre. Se paga en dos cuotas:</p>
<ul>
<li><strong>Primera cuota:</strong> hasta el 30 de junio.</li>
<li><strong>Segunda cuota:</strong> hasta el 18 de diciembre.</li>
</ul>
<p>Los empleadores tienen hasta 4 días hábiles extra para pagarlo.</p>
<h3>Aguinaldo proporcional</h3>
<p>Si no trabajaste el semestre completo (porque entraste o te fuiste en el medio), cobrás la parte proporcional: <em>mejor sueldo ÷ 2 × días trabajados ÷ días del semestre</em>.</p>
<h3>¿El aguinaldo tiene descuentos?</h3>
<p>Sí. Lleva los mismos aportes que el sueldo (17 % en total: jubilación, PAMI y obra social), por eso te mostramos también el neto estimado.</p>
</div>
''', faq=[
 ('¿Cuándo se cobra el aguinaldo?', 'La primera cuota vence el 30 de junio y la segunda el 18 de diciembre. El empleador tiene un plazo de gracia de 4 días hábiles.'),
 ('¿Qué sueldo se toma para el aguinaldo?', 'El mayor sueldo bruto mensual del semestre, incluyendo los conceptos remunerativos (horas extra, comisiones, adicionales).'),
 ('¿Me corresponde aguinaldo si trabajé pocos meses?', 'Sí, cobrás la parte proporcional a los días que trabajaste en el semestre.'),
], script='''
$('#anio').value ||= new Date().getFullYear();
conectar(() => {
  const mejor = val('mejor'), sem = $('#sem').value, anio = val('anio') || new Date().getFullYear();
  const d0 = new Date(anio, sem === '1' ? 0 : 6, 1), d1 = new Date(anio, sem === '1' ? 5 : 11, sem === '1' ? 30 : 31);
  const dia = 864e5, total = Math.round((d1 - d0) / dia) + 1;
  const parse = v => v ? new Date(v + 'T00:00:00') : null;
  let a = parse($('#ini').value), b = parse($('#fin').value);
  a = a && a > d0 ? a : d0; b = b && b < d1 ? b : d1;
  const dias = Math.max(0, Math.round((b - a) / dia) + 1);
  const bruto = mejor / 2 * dias / total, neto = bruto * .83;
  const vence = sem === '1' ? '30 de junio' : '18 de diciembre';
  $('#res').innerHTML = `<div class="label">Aguinaldo bruto</div><div class="big">${$$(bruto)}</div>` + filas([
    ['Mejor sueldo del semestre', $$(mejor)],
    ['Días trabajados', dias + ' de ' + total + (dias < total ? ' (proporcional)' : ' (completo)')],
    ['Aportes (17 %)', '− ' + $$(bruto * .17)],
    ['Aguinaldo neto estimado', $$(neto), 'total'],
  ]) + `<p class="note">Se paga hasta el ${vence} de ${anio}.</p>`;
});
''')

# ---------- VACACIONES ----------
page('vacaciones', 'Calculadora de vacaciones: días y pago según tu antigüedad',
 'Calculá cuántos días de vacaciones te corresponden según tu antigüedad (14, 21, 28 o 35 días) y cuánto te tienen que pagar, con el plus vacacional.',
 nombre='Vacaciones', body='''
<h1>Calculadora de vacaciones</h1>
<p class="lead">Averiguá cuántos días de vacaciones te tocan y cuánto te tienen que pagar por ellos.</p>
<div class="card calc">
<div class="row">
<label>Fecha de ingreso<input id="ini" type="date" value="2022-03-01"></label>
<label>Vacaciones del año<input id="anio" type="number" min="2000" max="2100"></label>
</div>
<label>Sueldo bruto mensual ($)<input id="sueldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cuántos días de vacaciones me corresponden?</h2>
<p>La Ley de Contrato de Trabajo (art. 150) fija los días <strong>corridos</strong> de vacaciones según tu antigüedad al 31 de diciembre del año:</p>
<ul>
<li>Menos de 5 años: <strong>14 días</strong>.</li>
<li>De 5 a 10 años: <strong>21 días</strong>.</li>
<li>De 10 a 20 años: <strong>28 días</strong>.</li>
<li>Más de 20 años: <strong>35 días</strong>.</li>
</ul>
<p>Si en el año trabajaste menos de la mitad de los días hábiles (por ejemplo, porque entraste en el segundo semestre), te corresponde <strong>1 día de vacaciones cada 20 días trabajados</strong>.</p>
<h2>¿Cuánto me pagan por las vacaciones?</h2>
<p>Para los empleados mensualizados, cada día de vacaciones se paga dividiendo el sueldo por <strong>25</strong> (no por 30). Esa diferencia es el famoso <strong>plus vacacional</strong>. Las vacaciones se pagan antes de empezar a tomarlas.</p>
<p>Tu convenio colectivo puede darte más días que la ley: si es así, vale el convenio.</p>
</div>
''', faq=[
 ('¿Las vacaciones son días hábiles o corridos?', 'Son días corridos (incluyen fines de semana y feriados), y deben empezar un lunes o el día hábil siguiente si ese lunes es feriado.'),
 ('¿Cuándo se pagan las vacaciones?', 'Al comenzar el período de vacaciones, junto con el aviso. El valor de cada día es el sueldo dividido 25.'),
 ('¿Entre qué fechas me pueden dar las vacaciones?', 'El empleador debe otorgarlas entre el 1 de octubre y el 30 de abril, y avisarte con al menos 45 días de anticipación.'),
], script='''
$('#anio').value ||= new Date().getFullYear();
conectar(() => {
  const anio = val('anio') || new Date().getFullYear(), sueldo = val('sueldo');
  const ini = $('#ini').value ? new Date($('#ini').value + 'T00:00:00') : null;
  if (!ini) { $('#res').innerHTML = 'Cargá tu fecha de ingreso.'; return; }
  const cierre = new Date(anio, 11, 31);
  if (ini > cierre) { $('#res').innerHTML = 'La fecha de ingreso es posterior a ese año.'; return; }
  let ant = cierre.getFullYear() - ini.getFullYear();
  if (cierre < new Date(cierre.getFullYear(), ini.getMonth(), ini.getDate())) ant--;
  let dias = ant < 5 ? 14 : ant < 10 ? 21 : ant < 20 ? 28 : 35, prop = false;
  if (ini.getFullYear() === anio) {
    const corridos = Math.round((cierre - ini) / 864e5) + 1;
    const habiles = Math.round(corridos * 5 / 7), habilesAnio = Math.round(365 * 5 / 7);
    if (habiles < habilesAnio / 2) { dias = Math.floor(habiles / 20); prop = true; }
  }
  const pago = sueldo / 25 * dias, normal = sueldo / 30 * dias;
  const textoAnt = ant < 1 ? 'menos de 1 año' : ant + (ant === 1 ? ' año' : ' años');
  $('#res').innerHTML = `<div class="label">Te corresponden</div><div class="big">${dias} días corridos</div>` + filas([
    ['Antigüedad al 31/12/' + anio, textoAnt],
    ['Valor de cada día (sueldo ÷ 25)', $$(sueldo / 25)],
    ['Lo que cobrarías esos días sin vacaciones', $$(normal)],
    ['Plus vacacional', '+ ' + $$(pago - normal)],
    ['Pago bruto de vacaciones', $$(pago), 'total'],
  ]) + (prop ? '<p class="note">Trabajaste menos de la mitad del año: corresponde 1 día cada 20 días hábiles trabajados (estimado).</p>' : '');
});
''')

# ---------- PLAZO FIJO ----------
page('plazo-fijo', 'Calculadora de plazo fijo: intereses, TEA y comparación con la inflación',
 'Simulá tu plazo fijo: cuánto ganás según la TNA y los días, la tasa efectiva anual (TEA) y si le gana a la inflación.',
 nombre='Plazo fijo', body='''
<h1>Calculadora de plazo fijo</h1>
<p class="lead">Poné cuánto querés invertir y la tasa de tu banco. Te mostramos cuánto ganás y si le gana a la inflación.</p>
<div class="card calc">
<label>Monto a invertir ($)<input id="cap" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>TNA (%) <small>tasa nominal anual de tu banco</small><input id="tna" type="number" inputmode="decimal" min="0" step="0.1" value="30"></label>
<label>Plazo (días) <small>mínimo 30</small><input id="dias" type="number" min="1" value="30"></label>
</div>
<label>Inflación mensual esperada (%) <small>opcional, para comparar</small><input id="inf" type="number" inputmode="decimal" step="0.1" value="2"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calculan los intereses de un plazo fijo?</h2>
<p>Los bancos informan la <strong>TNA</strong> (tasa nominal anual). El interés de un plazo fijo tradicional es:</p>
<p><em>Interés = monto × TNA ÷ 100 × días ÷ 365</em></p>
<p>Por ejemplo, $1.000.000 a 30 días con una TNA del 30 % te da $24.657 de intereses.</p>
<h3>TNA y TEA</h3>
<p>La <strong>TEA</strong> (tasa efectiva anual) muestra cuánto ganarías en un año si renovaras el plazo fijo cada vez, reinvirtiendo los intereses. Por eso siempre es un poco mayor que la TNA.</p>
<h3>¿Le gana a la inflación?</h3>
<p>Lo importante no es cuántos pesos ganás, sino si tu plata compra más o menos cosas al final. Si la tasa mensual del plazo fijo es menor que la inflación del mes, en términos reales perdés poder de compra.</p>
</div>
''', faq=[
 ('¿Cuál es el plazo mínimo de un plazo fijo?', 'En los plazos fijos tradicionales el plazo mínimo es de 30 días.'),
 ('¿Qué diferencia hay entre TNA y TEA?', 'La TNA es la tasa anual sin reinvertir intereses; la TEA supone que renovás el plazo fijo y reinvertís los intereses, por eso es más alta.'),
 ('¿Los plazos fijos están garantizados?', 'Los depósitos en pesos y dólares en bancos argentinos tienen una garantía de SEDESA hasta un monto máximo por persona y por banco.'),
], script='''
conectar(() => {
  const cap = val('cap'), tna = val('tna'), dias = Math.max(1, val('dias')), inf = val('inf');
  const tasaPer = tna / 100 * dias / 365, int = cap * tasaPer;
  const tea = (Math.pow(1 + tasaPer, 365 / dias) - 1) * 100;
  const tem = (Math.pow(1 + tasaPer, 30 / dias) - 1) * 100;
  let comp = '';
  if (inf) {
    const infPer = Math.pow(1 + inf / 100, dias / 30) - 1;
    const real = ((1 + tasaPer) / (1 + infPer) - 1) * 100;
    comp = `<p class="note ${real < 0 ? 'warn' : ''}">${real >= 0 ? '✓ Le gana a la inflación' : '⚠ Pierde contra la inflación'}: rendimiento real de ${pct(real)} en el período (${$$(cap * real / 100)} en poder de compra de hoy).</p>`;
  }
  $('#res').innerHTML = `<div class="label">Ganás en ${dias} días</div><div class="big">${$$(int)}</div>` + filas([
    ['Monto invertido', $$(cap)],
    ['Intereses', '+ ' + $$(int)],
    ['Total al vencimiento', $$(cap + int), 'total'],
    ['Tasa efectiva mensual', pct(tem)],
    ['TEA (renovando)', pct(tea)],
  ]) + comp;
});
''')

# ---------- CUOTAS ----------
page('cuotas', '¿Cuotas o contado? Calculadora para saber qué conviene',
 'Compará pagar en cuotas o de contado teniendo en cuenta la inflación. Calculá el costo financiero real de las cuotas y qué opción te conviene.',
 nombre='Cuotas o contado', body='''
<h1>¿Cuotas o contado?</h1>
<p class="lead">Con inflación, pagar en cuotas puede convenir aunque tengan recargo. Cargá los datos y te decimos qué te conviene.</p>
<div class="card calc">
<label>Precio de contado ($) <small>con el descuento por pagar en efectivo, si hay</small><input id="contado" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Cantidad de cuotas<input id="n" type="number" min="1" max="72" value="6"></label>
<label>Valor de cada cuota ($)<input id="cuota" type="number" inputmode="decimal" min="0" value="180000"></label>
</div>
<label>Inflación mensual esperada (%)<input id="inf" type="number" inputmode="decimal" step="0.1" value="2"></label>
<label class="check"><input id="hoy" type="checkbox"> La primera cuota se paga hoy</label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo saber si conviene pagar en cuotas?</h2>
<p>Cuando hay inflación, una cuota de $100.000 dentro de seis meses "vale" menos que $100.000 hoy, porque para entonces los precios (y en general los sueldos) subieron. Para comparar de forma justa hay que llevar todas las cuotas a <strong>valor de hoy</strong>, descontándoles la inflación esperada. Eso es el <strong>valor actual</strong>.</p>
<ul>
<li>Si el valor actual de las cuotas es <strong>menor</strong> que el precio de contado, conviene pagar en cuotas.</li>
<li>Si es <strong>mayor</strong>, conviene pagar de contado.</li>
</ul>
<h3>Tasa implícita de las cuotas</h3>
<p>También calculamos la tasa de interés mensual que te están cobrando por financiarte (la tasa implícita). Si es menor que la inflación mensual que esperás, las cuotas te convienen.</p>
<h3>Ojo con</h3>
<p>Los impuestos y cargos de la tarjeta, que a veces no están incluidos en la cuota que te muestran. Y comparar siempre contra el precio de contado <em>con descuento</em>, que es el que realmente podrías pagar.</p>
</div>
''', faq=[
 ('¿Conviene pagar en cuotas sin interés?', 'Casi siempre sí, si no hay descuento por pagar de contado: con inflación, las últimas cuotas valen menos en términos reales.'),
 ('¿Qué inflación mensual pongo?', 'Usá la inflación que esperás para los próximos meses. Una referencia es el último dato mensual del INDEC o el Relevamiento de Expectativas de Mercado del BCRA.'),
 ('¿Qué es el valor actual de las cuotas?', 'Es lo que valen hoy todas las cuotas futuras, una vez descontada la inflación. Sirve para comparar contra el precio de contado.'),
], script='''
function tasaImplicita(contado, cuota, n, hoy) {
  const va = r => { let s = 0; for (let k = 0; k < n; k++) s += cuota / Math.pow(1 + r, k + (hoy ? 0 : 1)); return s; };
  let lo = -0.99, hi = 5;
  if (va(lo) < contado || va(hi) > contado) return NaN;
  for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (va(m) > contado) lo = m; else hi = m; }
  return (lo + hi) / 2;
}
conectar(() => {
  const contado = val('contado'), n = Math.max(1, Math.round(val('n'))), cuota = val('cuota'), inf = val('inf') / 100, hoy = $('#hoy').checked;
  const total = cuota * n;
  let va = 0; for (let k = 0; k < n; k++) va += cuota / Math.pow(1 + inf, k + (hoy ? 0 : 1));
  const r = tasaImplicita(contado, cuota, n, hoy), dif = contado - va;
  const conviene = dif > 0 ? 'cuotas' : 'contado';
  $('#res').innerHTML = `<div class="label">Te conviene pagar</div><div class="big">${conviene === 'cuotas' ? 'En cuotas' : 'De contado'}</div>` +
    `<p>Ahorrás unos <strong>${$$(Math.abs(dif))}</strong> en valores de hoy.</p>` + filas([
    ['Precio de contado', $$(contado)],
    ['Total en cuotas (' + n + ' × ' + $$(cuota) + ')', $$(total)],
    ['Recargo nominal', pct((total / contado - 1) * 100)],
    ['Valor actual de las cuotas', $$(va), 'total'],
    ['Tasa implícita mensual', isFinite(r) ? pct(r * 100) : '—'],
    ['Inflación mensual esperada', pct(inf * 100)],
  ]);
});
''')

# ---------- DÓLAR ----------
page('dolar', 'Dólar hoy en Argentina: cotizaciones y conversor de pesos a dólares',
 'Cotización del dólar oficial, blue, MEP, CCL, tarjeta y cripto, y conversor de pesos a dólares y de dólares a pesos.',
 nombre='Dólar hoy', body='''
<h1>Dólar hoy y conversor</h1>
<p class="lead">Las cotizaciones del día y un conversor para pasar de pesos a dólares (o al revés) con el tipo de cambio que elijas.</p>
<div class="card calc">
<div class="row">
<label>Monto<input id="monto" type="number" inputmode="decimal" min="0" value="100"></label>
<label>Convertir<select id="dir"><option value="usd2ars">Dólares → pesos</option><option value="ars2usd">Pesos → dólares</option></select></label>
</div>
<div class="row">
<label>Tipo de dólar<select id="tipo"><option value="manual">Cotización manual</option></select></label>
<label>Cotización manual ($ por dólar)<input id="manual" type="number" inputmode="decimal" min="0" value="1400"></label>
</div>
<div id="res" class="result"></div>
</div>
<div id="cot"><p class="note">Cargando cotizaciones…</p></div>
<div class="article">
<h2>Los distintos tipos de dólar</h2>
<ul>
<li><strong>Oficial:</strong> el que publican los bancos para comprar o vender dólares por homebanking.</li>
<li><strong>Blue:</strong> el del mercado informal.</li>
<li><strong>MEP (bolsa):</strong> se obtiene comprando y vendiendo bonos en pesos y en dólares; es legal y se hace desde un broker o el banco.</li>
<li><strong>CCL (contado con liquidación):</strong> similar al MEP, pero los dólares quedan en una cuenta del exterior.</li>
<li><strong>Tarjeta:</strong> el que se aplica a los consumos en dólares con tarjeta, con impuestos incluidos.</li>
</ul>
<h3>Compra y venta</h3>
<p>Si vas a <strong>comprar</strong> dólares, mirá el precio de <em>venta</em> (es al que te los venden). Si vas a <strong>vender</strong> dólares, mirá el precio de <em>compra</em>. El conversor usa el que corresponde en cada caso.</p>
</div>
''', faq=[
 ('¿De dónde salen las cotizaciones?', 'Las tomamos de DolarApi.com, que reúne cotizaciones públicas. Pueden tener unos minutos de demora: antes de operar, confirmá el precio con tu banco o broker.'),
 ('¿Qué cotización usa el conversor?', 'Para pasar pesos a dólares usa el precio de venta (lo que pagás por cada dólar). Para pasar dólares a pesos usa el precio de compra (lo que te pagan por cada dólar).'),
], script='''
let cotis = [];
const nombres = { oficial: 'Oficial', blue: 'Blue', bolsa: 'MEP', contadoconliqui: 'CCL', tarjeta: 'Tarjeta', mayorista: 'Mayorista', cripto: 'Cripto' };
function calcular() {
  const monto = val('monto'), dir = $('#dir').value, tipo = $('#tipo').value;
  const c = cotis.find(x => x.casa === tipo);
  const compra = c ? c.compra : val('manual'), venta = c ? c.venta : val('manual');
  const tc = dir === 'ars2usd' ? venta : compra;
  if (!tc) { $('#res').innerHTML = 'Elegí un tipo de dólar o cargá una cotización.'; return; }
  const out = dir === 'ars2usd' ? dolares.format(monto / tc) : $$(monto * tc);
  $('#res').innerHTML = `<div class="label">${dir === 'ars2usd' ? $$(monto) + ' son' : dolares.format(monto) + ' son'}</div><div class="big">${out}</div>` +
    `<p class="note">Tipo de cambio usado: ${$$(tc)} (${dir === 'ars2usd' ? 'venta' : 'compra'}${c ? ', dólar ' + (nombres[c.casa] || c.nombre) : ', manual'}).</p>`;
}
conectar(calcular);
fetch('https://dolarapi.com/v1/dolares').then(r => r.json()).then(data => {
  cotis = data.filter(x => x && x.casa && x.venta);
  const sel = $('#tipo'), previo = sel.value;
  sel.innerHTML = cotis.map(x => `<option value="${x.casa}">Dólar ${nombres[x.casa] || x.nombre}</option>`).join('') + '<option value="manual">Cotización manual</option>';
  sel.value = cotis.some(x => x.casa === previo) || previo === 'manual' ? previo : 'blue';
  if (!sel.value) sel.value = cotis[0] ? cotis[0].casa : 'manual';
  const fecha = cotis[0] && cotis[0].fechaActualizacion ? new Date(cotis[0].fechaActualizacion).toLocaleString('es-AR', { dateStyle: 'short', timeStyle: 'short' }) : '';
  $('#cot').innerHTML = '<h2>Cotizaciones de hoy</h2><div class="rates">' + cotis.map(x =>
    `<div class="rate">Dólar ${nombres[x.casa] || x.nombre}<b>${$$(x.venta)}</b>Compra ${x.compra ? $$(x.compra) : '—'}</div>`).join('') +
    `</div><p class="note">Fuente: DolarApi.com${fecha ? ' · Actualizado ' + fecha : ''}. Valores de venta en grande.</p>`;
  calcular();
}).catch(() => {
  $('#cot').innerHTML = '<p class="note warn">No pudimos cargar las cotizaciones ahora. Podés usar el conversor con una cotización manual.</p>';
});
''')

# ---------- PRIVACIDAD ----------
page('privacidad', 'Política de privacidad', 'Política de privacidad y uso de cookies de Cuentas Claras.', nombre='Privacidad', body='''
<h1>Política de privacidad</h1>
<div class="article">
<p>En Cuentas Claras respetamos tu privacidad. Esta página explica qué información se usa cuando visitás el sitio.</p>
<h2>Datos que cargás en las calculadoras</h2>
<p>Los cálculos se hacen en tu propio dispositivo. Los números que escribís no se envían a ningún servidor. Para tu comodidad, el navegador puede recordar los últimos valores que usaste (almacenamiento local); podés borrarlos limpiando los datos del sitio en tu navegador.</p>
<h2>Publicidad y cookies</h2>
<p>Este sitio se financia con publicidad. Usamos Google AdSense, un servicio de Google que muestra anuncios.</p>
<ul>
<li>Proveedores externos, incluido Google, usan cookies para mostrar anuncios según las visitas anteriores de un usuario a este u otros sitios web.</li>
<li>Las cookies de publicidad de Google permiten que Google y sus socios muestren anuncios basados en tus visitas a este sitio u otros sitios de Internet.</li>
<li>Podés desactivar la publicidad personalizada desde la <a href="https://adssettings.google.com" rel="nofollow">configuración de anuncios de Google</a>, o desactivar las cookies de otros proveedores en <a href="https://www.aboutads.info/choices/" rel="nofollow">www.aboutads.info</a>.</li>
</ul>
<p>Más información sobre cómo Google usa los datos: <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">Cómo usa Google la información de los sitios que usan sus servicios</a>.</p>
<h2>Servicios de terceros</h2>
<p>La página de dólar consulta cotizaciones públicas en DolarApi.com. Esa consulta no incluye ningún dato personal.</p>
<h2>Cambios</h2>
<p>Podemos actualizar esta política. La versión vigente es siempre la publicada en esta página.</p>
</div>
''')

# ---------- ACERCA ----------
page('acerca', 'Acerca de Cuentas Claras', 'Quiénes somos y cómo hacemos las calculadoras de Cuentas Claras.', nombre='Acerca de', body='''
<h1>Acerca de Cuentas Claras</h1>
<div class="article">
<p>Cuentas Claras es un sitio de calculadoras gratuitas pensadas para resolver las cuentas de todos los días en Argentina: cuánto cobrás en mano, cuánto te toca de aguinaldo o de vacaciones, si te conviene un plazo fijo o pagar en cuotas, y a cuánto está el dólar.</p>
<h2>Cómo hacemos los cálculos</h2>
<p>Nos basamos en la Ley de Contrato de Trabajo (Ley 20.744), en la normativa vigente de aportes y en las fórmulas financieras que usan los bancos. En cada calculadora explicamos la fórmula y mostramos el detalle para que puedas verificar el resultado.</p>
<h2>Aviso</h2>
<p>Los resultados son estimaciones orientativas. Tu caso puede tener particularidades (convenio colectivo, adicionales, impuesto a las ganancias) que cambien el número final. Ante decisiones importantes, consultá a un contador o abogado laboral.</p>
<h2>Contacto</h2>
<p>¿Encontraste un error o querés proponer una calculadora nueva? Escribinos a <a href="mailto:matiasj.carattoli@gmail.com">matiasj.carattoli@gmail.com</a>.</p>
</div>
''')

# ---------- INDEMNIZACIÓN ----------
page('indemnizacion', 'Calculadora de indemnización por despido sin causa (liquidación final)',
 'Calculá tu indemnización por despido sin causa: antigüedad (art. 245), preaviso, integración del mes, vacaciones no gozadas y aguinaldo proporcional.',
 nombre='Indemnización por despido', body='''
<h1>Calculadora de indemnización por despido</h1>
<p class="lead">Si te despidieron sin causa, calculá cuánto te corresponde cobrar en la liquidación final, rubro por rubro.</p>
<div class="card calc">
<label>Mejor sueldo bruto mensual del último año ($) <small>normal y habitual</small><input id="sueldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Fecha de ingreso<input id="ini" type="date" value="2021-03-01"></label>
<label>Fecha de despido<input id="fin" type="date"></label>
</div>
<label>Tope del convenio ($) <small>opcional, 0 = sin tope</small><input id="tope" type="number" inputmode="decimal" min="0" value="0"></label>
<label class="check"><input id="preaviso" type="checkbox"> Me avisaron con preaviso (trabajé el período de preaviso)</label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Qué incluye la liquidación por despido sin causa?</h2>
<h3>1. Indemnización por antigüedad (art. 245 LCT)</h3>
<p>Un sueldo por cada año trabajado o fracción mayor a 3 meses, tomando la mejor remuneración mensual, normal y habitual del último año. Nunca puede ser menor a un sueldo. Si tu convenio tiene tope, la base se limita, pero según la jurisprudencia de la Corte (fallo Vizzoti) no puede quedar por debajo del 67 % de tu sueldo real.</p>
<h3>2. Preaviso omitido (art. 231 y 232)</h3>
<p>Si no te avisaron con anticipación, te deben el preaviso: 15 días durante el período de prueba, 1 mes si tenés menos de 5 años de antigüedad y 2 meses si tenés más.</p>
<h3>3. Integración del mes de despido (art. 233)</h3>
<p>Si el despido sin preaviso no fue el último día del mes, te pagan los días que faltan hasta fin de mes.</p>
<h3>4. Rubros que se cobran siempre</h3>
<ul>
<li>Los <strong>días trabajados</strong> del mes.</li>
<li>El <strong>aguinaldo proporcional</strong> del semestre.</li>
<li>Las <strong>vacaciones no gozadas</strong> proporcionales, con su aguinaldo.</li>
</ul>
<h3>Período de prueba</h3>
<p>Durante el período de prueba (en general los primeros 6 meses) no corresponde la indemnización por antigüedad, pero sí el preaviso de 15 días y los rubros que se cobran siempre.</p>
<p class="warn">Las leyes laborales cambian. Esta calculadora sirve como referencia; ante un despido, consultá con un abogado laboralista o en el Ministerio de Trabajo antes de firmar.</p>
</div>
''', faq=[
 ('¿Cuánto me corresponde por despido sin causa?', 'Un sueldo por cada año de antigüedad (o fracción mayor a 3 meses), más el preaviso si no te avisaron, la integración del mes, los días trabajados, el aguinaldo proporcional y las vacaciones no gozadas.'),
 ('¿En cuánto tiempo me tienen que pagar la indemnización?', 'La liquidación final debe pagarse dentro de los 4 días hábiles posteriores a la fecha de extinción del contrato.'),
 ('¿La indemnización por despido paga impuestos o aportes?', 'La indemnización por antigüedad, el preaviso y la integración no llevan aportes jubilatorios ni pagan impuesto a las ganancias. Los días trabajados, el aguinaldo y las vacaciones sí llevan aportes.'),
], script='''
$('#fin').value ||= new Date().toISOString().slice(0, 10);
conectar(() => {
  const sueldo = val('sueldo'), tope = val('tope'), conPreaviso = $('#preaviso').checked;
  const p = v => v ? new Date(v + 'T00:00:00') : null;
  const ini = p($('#ini').value), fin = p($('#fin').value);
  if (!ini || !fin || fin < ini) { $('#res').innerHTML = 'Revisá las fechas de ingreso y despido.'; return; }
  const dia = 864e5;
  let meses = (fin.getFullYear() - ini.getFullYear()) * 12 + fin.getMonth() - ini.getMonth();
  if (fin.getDate() < ini.getDate()) meses--;
  const anios = Math.floor(meses / 12), resto = meses % 12;
  const prueba = meses < 6;
  const aniosInd = prueba ? 0 : Math.max(1, anios + (resto > 3 ? 1 : 0));
  const base = tope > 0 ? Math.max(Math.min(sueldo, tope), sueldo * .67) : sueldo;
  const ind = base * aniosInd;
  const mesesPre = prueba ? .5 : anios >= 5 ? 2 : 1;
  const preav = conPreaviso ? 0 : sueldo * mesesPre;
  const finMes = new Date(fin.getFullYear(), fin.getMonth() + 1, 0).getDate();
  const integ = conPreaviso ? 0 : sueldo / 30 * (finMes - fin.getDate());
  const trab = sueldo / 30 * Math.min(30, fin.getDate());
  const semIni = new Date(fin.getFullYear(), fin.getMonth() < 6 ? 0 : 6, 1);
  const semFin = new Date(fin.getFullYear(), fin.getMonth() < 6 ? 5 : 11, fin.getMonth() < 6 ? 30 : 31);
  const desdeSem = ini > semIni ? ini : semIni;
  const sac = sueldo / 2 * (Math.round((fin - desdeSem) / dia) + 1) / (Math.round((semFin - semIni) / dia) + 1);
  const antDic = anios < 5 ? 14 : anios < 10 ? 21 : anios < 20 ? 28 : 35;
  const inicioAnio = new Date(fin.getFullYear(), 0, 1), desdeAnio = ini > inicioAnio ? ini : inicioAnio;
  const diasVac = antDic * (Math.round((fin - desdeAnio) / dia) + 1) / 365;
  const vac = sueldo / 25 * diasVac;
  const sacs = (preav + integ + vac) / 12;
  const total = ind + preav + integ + trab + sac + vac + sacs;
  const ant = anios + (anios === 1 ? ' año' : ' años') + (resto ? ' y ' + resto + (resto === 1 ? ' mes' : ' meses') : '');
  $('#res').innerHTML = `<div class="label">Total estimado a cobrar (bruto)</div><div class="big">${$$(total)}</div>` + filas([
    ['Antigüedad', ant + (prueba ? ' (período de prueba)' : '')],
    ['Indemnización por antigüedad (' + aniosInd + ' × ' + $$(base) + ')', $$(ind)],
    ['Preaviso' + (conPreaviso ? ' (otorgado)' : ' (' + (mesesPre === .5 ? '15 días' : mesesPre + (mesesPre === 1 ? ' mes' : ' meses')) + ')'), $$(preav)],
    ['Integración del mes de despido', $$(integ)],
    ['Días trabajados del mes', $$(trab)],
    ['Aguinaldo proporcional', $$(sac)],
    ['Vacaciones no gozadas (' + num.format(diasVac) + ' días)', $$(vac)],
    ['Aguinaldo sobre preaviso, integración y vacaciones', $$(sacs)],
    ['Total', $$(total), 'total'],
  ]) + '<p class="note">Los días trabajados, el aguinaldo y las vacaciones llevan aportes (17 %); la indemnización, el preaviso y la integración no.</p>';
});
''')

# ---------- HORAS EXTRA ----------
page('horas-extra', 'Calculadora de horas extra: al 50 % y al 100 %',
 'Calculá cuánto te tienen que pagar por tus horas extra al 50 % (días hábiles) y al 100 % (sábados después de las 13, domingos y feriados).',
 nombre='Horas extra', body='''
<h1>Calculadora de horas extra</h1>
<p class="lead">Calculá el valor de tu hora y cuánto te corresponde cobrar por las horas extra del mes.</p>
<div class="card calc">
<div class="row">
<label>Sueldo bruto mensual ($)<input id="sueldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
<label>Horas de tu jornada por mes <small>200 es lo habitual con 48 h semanales</small><input id="hm" type="number" min="1" value="200"></label>
</div>
<div class="row">
<label>Horas extra al 50 % <small>días hábiles</small><input id="h50" type="number" inputmode="decimal" min="0" value="10"></label>
<label>Horas extra al 100 % <small>sáb. después de 13 h, dom. y feriados</small><input id="h100" type="number" inputmode="decimal" min="0" value="4"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se pagan las horas extra?</h2>
<p>La Ley de Contrato de Trabajo (art. 201) establece que las horas extra se pagan con un recargo sobre el valor de la hora normal:</p>
<ul>
<li><strong>50 % de recargo</strong> en días comunes.</li>
<li><strong>100 % de recargo</strong> los sábados después de las 13 h, los domingos y los feriados.</li>
</ul>
<h3>¿Cómo se calcula el valor de la hora?</h3>
<p>Se divide el sueldo mensual por la cantidad de horas que trabajás en el mes según tu jornada. Con una jornada de 48 horas semanales se suele usar 200 horas por mes. Si tu jornada es de 40 horas semanales, usá unas 173.</p>
<h3>Límites</h3>
<p>La jornada máxima legal es de 8 horas diarias o 48 semanales, y las horas extra tienen un tope de 3 por día, 30 por mes y 200 por año, salvo excepciones.</p>
</div>
''', faq=[
 ('¿Cuánto se paga la hora extra en Argentina?', 'Con un recargo del 50 % en días comunes y del 100 % los sábados después de las 13 h, domingos y feriados.'),
 ('¿Las horas extra llevan descuentos?', 'Sí, son remuneración y llevan los mismos aportes que el sueldo (17 % en total).'),
 ('¿Me pueden obligar a hacer horas extra?', 'En general no, salvo casos de peligro grave o necesidades excepcionales de la empresa previstas por la ley.'),
], script='''
conectar(() => {
  const sueldo = val('sueldo'), hm = Math.max(1, val('hm')), h50 = val('h50'), h100 = val('h100');
  const hora = sueldo / hm, a = hora * 1.5 * h50, b = hora * 2 * h100, t = a + b;
  $('#res').innerHTML = `<div class="label">Te corresponden por horas extra</div><div class="big">${$$(t)}</div>` + filas([
    ['Valor de la hora normal', $$(hora)],
    ['Hora extra al 50 %', $$(hora * 1.5)],
    ['Hora extra al 100 %', $$(hora * 2)],
    [h50 + ' h al 50 %', $$(a)],
    [h100 + ' h al 100 %', $$(b)],
    ['Total bruto', $$(t), 'total'],
    ['Total neto estimado (−17 %)', $$(t * .83)],
  ]);
});
''')

# ---------- INTERÉS COMPUESTO ----------
page('interes-compuesto', 'Calculadora de interés compuesto y ahorro mensual',
 'Calculá cuánto juntás con interés compuesto: capital inicial, aporte mensual, tasa anual y plazo. Con el valor real descontando la inflación.',
 nombre='Interés compuesto', body='''
<h1>Calculadora de interés compuesto</h1>
<p class="lead">Descubrí cuánto podés juntar si ahorrás todos los meses y reinvertís lo que ganás.</p>
<div class="card calc">
<div class="row">
<label>Capital inicial ($)<input id="cap" type="number" inputmode="decimal" min="0" value="500000"></label>
<label>Aporte mensual ($)<input id="apo" type="number" inputmode="decimal" min="0" value="100000"></label>
</div>
<div class="row">
<label>Rendimiento anual (%) <small>tasa efectiva anual</small><input id="tasa" type="number" inputmode="decimal" step="0.1" value="35"></label>
<label>Plazo (años)<input id="anios" type="number" min="1" max="50" value="5"></label>
</div>
<label>Inflación anual esperada (%) <small>opcional, para ver el valor real</small><input id="inf" type="number" inputmode="decimal" step="0.1" value="25"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Qué es el interés compuesto?</h2>
<p>Es ganar intereses sobre los intereses. Cada mes, lo que ganaste se suma a tu capital y el mes siguiente también genera rendimiento. Por eso, con el tiempo, el crecimiento se acelera: el mismo ahorro rinde mucho más a 10 años que a 2.</p>
<h3>La fórmula</h3>
<p><em>Monto final = capital × (1 + i)<sup>n</sup> + aporte × ((1 + i)<sup>n</sup> − 1) ÷ i</em>, donde <em>i</em> es la tasa mensual y <em>n</em> la cantidad de meses. La tasa mensual sale de la anual: <em>i = (1 + TEA)<sup>1/12</sup> − 1</em>.</p>
<h3>Valor nominal y valor real</h3>
<p>Con inflación, los pesos del futuro compran menos. Por eso te mostramos también el <strong>valor real</strong>: cuánto representaría ese monto en pesos de hoy. Si el rendimiento es menor que la inflación, aunque tengas más pesos, tu ahorro pierde poder de compra.</p>
<h3>¿Dónde se consigue ese rendimiento?</h3>
<p>Depende del instrumento: plazos fijos, fondos comunes de inversión, cuentas remuneradas, bonos o acciones. Cuanto mayor es el rendimiento esperado, en general mayor es el riesgo.</p>
</div>
''', faq=[
 ('¿Qué diferencia hay entre interés simple y compuesto?', 'Con interés simple solo ganás sobre el capital inicial. Con interés compuesto los intereses se reinvierten y también generan intereses, por eso el monto crece más rápido.'),
 ('¿Qué tasa pongo?', 'Usá la tasa efectiva anual (TEA) del instrumento en el que vas a invertir. Si solo tenés la TNA de un plazo fijo, usá la calculadora de plazo fijo para pasarla a TEA.'),
 ('¿Los aportes se hacen al principio o al final del mes?', 'Esta calculadora supone que aportás al final de cada mes, que es el caso más común cuando se ahorra parte del sueldo.'),
], script='''
conectar(() => {
  const cap = val('cap'), apo = val('apo'), tea = val('tasa') / 100, anios = Math.max(1, Math.min(50, Math.round(val('anios')))), inf = val('inf') / 100;
  const i = Math.pow(1 + tea, 1 / 12) - 1, n = anios * 12;
  const fv = m => cap * Math.pow(1 + i, m) + (i ? apo * (Math.pow(1 + i, m) - 1) / i : apo * m);
  const total = fv(n), aportado = cap + apo * n, real = total / Math.pow(1 + inf, anios);
  let tabla = '<details class="tabla"><summary>Ver año por año</summary><table class="detail"><tr><th>Año</th><th>Aportado</th><th>Total</th></tr>';
  for (let a = 1; a <= anios; a++) tabla += `<tr><td>${a}</td><td>${$$(cap + apo * a * 12)}</td><td>${$$(fv(a * 12))}</td></tr>`;
  tabla += '</table></details>';
  $('#res').innerHTML = `<div class="label">En ${anios} ${anios === 1 ? 'año' : 'años'} tendrías</div><div class="big">${$$(total)}</div>` + filas([
    ['Total aportado', $$(aportado)],
    ['Intereses ganados', '+ ' + $$(total - aportado)],
    ['Tasa mensual equivalente', pct(i * 100)],
    ['Valor real (en pesos de hoy)', $$(real), 'total'],
  ]) + tabla;
});
''')

# ---------- PRÉSTAMO ----------
page('prestamo', 'Simulador de préstamo personal: cuota mensual e intereses',
 'Simulá tu préstamo personal con sistema francés: cuota mensual, total a pagar, intereses e IVA, y el cuadro de pagos mes a mes.',
 nombre='Préstamo personal', body='''
<h1>Simulador de préstamo personal</h1>
<p class="lead">Calculá la cuota de tu préstamo y cuánto vas a terminar pagando en total.</p>
<div class="card calc">
<label>Monto del préstamo ($)<input id="monto" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>TNA (%) <small>tasa nominal anual que informa el banco</small><input id="tna" type="number" inputmode="decimal" step="0.1" min="0" value="60"></label>
<label>Cantidad de cuotas (meses)<input id="n" type="number" min="1" max="120" value="12"></label>
</div>
<label class="check"><input id="iva" type="checkbox" checked> Sumar IVA sobre los intereses (21 %)</label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula la cuota de un préstamo?</h2>
<p>La mayoría de los préstamos personales en Argentina usan el <strong>sistema francés</strong>: pagás una cuota fija, pero al principio la mayor parte son intereses y al final, capital.</p>
<p><em>Cuota = monto × i ÷ (1 − (1 + i)<sup>−n</sup>)</em>, donde <em>i</em> es la tasa mensual (TNA ÷ 12) y <em>n</em> la cantidad de cuotas.</p>
<h3>El IVA sobre los intereses</h3>
<p>En los préstamos de bancos y financieras, los intereses pagan <strong>IVA del 21 %</strong>. Por eso la cuota real es un poco más alta que la cuota "pura" y va bajando con el tiempo, a medida que pagás menos intereses.</p>
<h3>Mirá el CFT</h3>
<p>Para comparar préstamos, el dato más importante es el <strong>CFT (costo financiero total)</strong>, que incluye intereses, IVA, seguros y comisiones. Por ley, los bancos tienen que informarlo. Esta calculadora no incluye seguros ni comisiones.</p>
</div>
''', faq=[
 ('¿Qué es el sistema francés?', 'Es el sistema de cuota fija: todas las cuotas tienen el mismo valor (sin contar el IVA), pero en las primeras pagás más intereses y en las últimas más capital.'),
 ('¿Qué diferencia hay entre TNA, TEA y CFT?', 'La TNA es la tasa anual sin capitalizar; la TEA incluye la capitalización mensual; el CFT además suma IVA, seguros y comisiones. Para comparar préstamos usá siempre el CFT.'),
 ('¿Conviene cancelar un préstamo antes?', 'Puede convenir si tenés el dinero, porque dejás de pagar intereses. Consultá si el banco cobra una comisión por precancelación.'),
], script='''
conectar(() => {
  const M = val('monto'), tna = val('tna'), n = Math.max(1, Math.min(120, Math.round(val('n')))), conIva = $('#iva').checked;
  const i = tna / 100 / 12;
  const cuota = i ? M * i / (1 - Math.pow(1 + i, -n)) : M / n;
  let saldo = M, totInt = 0, totIva = 0, primera = 0, filasT = '';
  for (let k = 1; k <= n; k++) {
    const int = saldo * i, cap = cuota - int, iva = conIva ? int * .21 : 0;
    saldo -= cap; totInt += int; totIva += iva;
    if (k === 1) primera = cuota + iva;
    filasT += `<tr><td>${k}</td><td>${$$(cap)}</td><td>${$$(int + iva)}</td><td>${$$(cuota + iva)}</td></tr>`;
  }
  const total = M + totInt + totIva, tea = (Math.pow(1 + i, 12) - 1) * 100;
  $('#res').innerHTML = `<div class="label">${conIva ? 'Primera cuota (con IVA)' : 'Cuota mensual'}</div><div class="big">${$$(conIva ? primera : cuota)}</div>` + filas([
    ['Cuota pura (sin IVA)', $$(cuota)],
    ['Intereses', $$(totInt)],
    ...(conIva ? [['IVA sobre intereses', $$(totIva)]] : []),
    ['Total a devolver', $$(total), 'total'],
    ['TEA', pct(tea)],
  ]) + `<details class="tabla"><summary>Ver cuadro de pagos</summary><table class="detail"><tr><th>Cuota</th><th>Capital</th><th>Interés${conIva ? ' + IVA' : ''}</th><th>Total</th></tr>${filasT}</table></details>`;
});
''')

# ---------- IVA ----------
page('iva', 'Calculadora de IVA: agregar o quitar el IVA de un precio',
 'Calculá el IVA de un precio en Argentina: agregá o sacá el IVA del 21 %, 10,5 % o 27 % y mirá el neto y el impuesto al instante.',
 nombre='IVA', body='''
<h1>Calculadora de IVA</h1>
<p class="lead">Sumale el IVA a un precio sin impuestos, o sacáselo a un precio final para saber el neto.</p>
<div class="card calc">
<div class="row">
<label>Monto ($)<input id="monto" type="number" inputmode="decimal" min="0" value="100000"></label>
<label>Alícuota<select id="ali"><option value="21">21 % (general)</option><option value="10.5">10,5 % (reducida)</option><option value="27">27 % (servicios públicos a empresas)</option></select></label>
</div>
<label>¿Qué querés hacer?<select id="modo"><option value="sacar">El monto ya tiene IVA: quiero saber el neto</option><option value="agregar">El monto es sin IVA: quiero sumarle el IVA</option></select></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el IVA?</h2>
<ul>
<li><strong>Para agregar el IVA:</strong> <em>precio final = neto × (1 + alícuota)</em>. Con 21 %: neto × 1,21.</li>
<li><strong>Para sacar el IVA:</strong> <em>neto = precio final ÷ (1 + alícuota)</em>. Con 21 %: precio ÷ 1,21. Ojo: no es lo mismo que restarle el 21 % al precio final.</li>
</ul>
<h3>Las alícuotas de IVA en Argentina</h3>
<ul>
<li><strong>21 %:</strong> la tasa general, que se aplica a la mayoría de los productos y servicios.</li>
<li><strong>10,5 %:</strong> tasa reducida para algunos alimentos, medicina prepaga, transporte, ciertos bienes de capital, entre otros.</li>
<li><strong>27 %:</strong> para servicios como luz, gas, agua y telecomunicaciones cuando los contrata una empresa o un responsable inscripto.</li>
</ul>
<h3>Ejemplo</h3>
<p>Si un producto cuesta $121.000 con IVA del 21 %, el precio neto es $121.000 ÷ 1,21 = <strong>$100.000</strong> y el IVA es <strong>$21.000</strong>.</p>
</div>
''', faq=[
 ('¿Por qué no puedo restarle el 21 % al precio final?', 'Porque el IVA se calcula sobre el precio neto, no sobre el final. Restarle el 21 % a $121.000 da $95.590, pero el neto real es $100.000. Hay que dividir por 1,21.'),
 ('¿Qué es el IVA discriminado?', 'Es cuando la factura muestra por separado el precio neto y el IVA. Lo usan los responsables inscriptos para computar el crédito fiscal.'),
], script='''
conectar(() => {
  const m = val('monto'), a = val('ali') / 100, agregar = $('#modo').value === 'agregar';
  const neto = agregar ? m : m / (1 + a), iva = neto * a, final = neto + iva;
  $('#res').innerHTML = `<div class="label">${agregar ? 'Precio final con IVA' : 'Precio neto (sin IVA)'}</div><div class="big">${$$(agregar ? final : neto)}</div>` + filas([
    ['Precio neto', $$(neto)],
    ['IVA (' + pct(a * 100) + ')', $$(iva)],
    ['Precio final', $$(final), 'total'],
  ]);
});
''')

# ---------- PORCENTAJES ----------
page('porcentajes', 'Calculadora de porcentajes: descuentos, aumentos y variación',
 'Calculá porcentajes al instante: cuánto es un porcentaje de un número, precio con descuento o aumento y variación porcentual entre dos valores.',
 nombre='Porcentajes', body='''
<h1>Calculadora de porcentajes</h1>
<p class="lead">Tres calculadoras en una: porcentaje de un número, descuentos o aumentos y variación entre dos valores.</p>
<div class="card calc">
<h2 class="calc-title">¿Cuánto es el X % de un número?</h2>
<div class="row">
<label>Porcentaje (%)<input id="p1" type="number" inputmode="decimal" value="15"></label>
<label>Número<input id="n1" type="number" inputmode="decimal" value="80000"></label>
</div>
<div id="r1" class="result mini"></div>
</div>
<div class="card calc">
<h2 class="calc-title">Precio con descuento o aumento</h2>
<div class="row">
<label>Precio ($)<input id="pr" type="number" inputmode="decimal" min="0" value="50000"></label>
<label>Porcentaje (%)<input id="p2" type="number" inputmode="decimal" value="20"></label>
</div>
<label>Tipo<select id="tipo"><option value="desc">Descuento</option><option value="aum">Aumento o recargo</option></select></label>
<div id="r2" class="result mini"></div>
</div>
<div class="card calc">
<h2 class="calc-title">Variación porcentual entre dos valores</h2>
<div class="row">
<label>Valor anterior<input id="a" type="number" inputmode="decimal" value="1000"></label>
<label>Valor nuevo<input id="b" type="number" inputmode="decimal" value="1250"></label>
</div>
<div id="r3" class="result mini"></div>
</div>
<div class="article">
<h2>Cómo calcular porcentajes</h2>
<ul>
<li><strong>X % de un número:</strong> número × X ÷ 100. El 15 % de 80.000 es 80.000 × 0,15 = 12.000.</li>
<li><strong>Descuento:</strong> precio × (1 − X ÷ 100). Un 20 % de descuento sobre $50.000 deja $40.000.</li>
<li><strong>Aumento:</strong> precio × (1 + X ÷ 100). Un aumento del 20 % sobre $50.000 da $60.000.</li>
<li><strong>Variación:</strong> (nuevo − anterior) ÷ anterior × 100. De 1.000 a 1.250 hay un aumento del 25 %.</li>
</ul>
<h3>Un error común</h3>
<p>Un aumento del 50 % seguido de una baja del 50 % no te deja donde empezaste: $100 + 50 % = $150, y $150 − 50 % = $75. Los porcentajes se aplican siempre sobre el valor del momento.</p>
</div>
''', faq=[
 ('¿Cómo saco el porcentaje de un número en la calculadora del celular?', 'Multiplicá el número por el porcentaje y dividí por 100. Por ejemplo, el 30 % de 2.000 es 2.000 × 30 ÷ 100 = 600.'),
 ('¿Dos descuentos del 10 % son un 20 %?', 'No: son un 19 %. El segundo descuento se aplica sobre el precio ya rebajado: 100 × 0,9 × 0,9 = 81.'),
], script='''
conectar(() => {
  const p1 = val('p1'), n1 = val('n1');
  $('#r1').innerHTML = `<div class="label">El ${num.format(p1)} % de ${num.format(n1)} es</div><div class="big">${num.format(n1 * p1 / 100)}</div>`;
  const pr = val('pr'), p2 = val('p2'), desc = $('#tipo').value === 'desc', fin = pr * (desc ? 1 - p2 / 100 : 1 + p2 / 100);
  $('#r2').innerHTML = `<div class="label">Precio ${desc ? 'con descuento' : 'con aumento'}</div><div class="big">${$$(fin)}</div><p class="note">${desc ? 'Ahorrás' : 'Pagás de más'} ${$$(Math.abs(fin - pr))}.</p>`;
  const a = val('a'), b = val('b');
  const v = a ? (b - a) / a * 100 : NaN;
  $('#r3').innerHTML = isFinite(v) ? `<div class="label">${v >= 0 ? 'Aumentó' : 'Bajó'}</div><div class="big">${pct(Math.abs(v))}</div><p class="note">Diferencia: ${num.format(b - a)}.</p>` : 'El valor anterior no puede ser 0.';
});
''')

# ---------- INFLACIÓN ----------
page('inflacion', 'Calculadora de inflación acumulada y poder adquisitivo',
 'Calculá la inflación acumulada a partir de la inflación de cada mes, la tasa anualizada y cuánto vale hoy tu dinero. Ideal para comparar con tu aumento de sueldo.',
 nombre='Inflación acumulada', body='''
<h1>Calculadora de inflación acumulada</h1>
<p class="lead">Cargá la inflación de cada mes y te decimos cuánto subieron los precios en total y cuánto vale hoy tu plata.</p>
<div class="card calc">
<label>Inflación de cada mes (%) <small>una por línea, en orden. Ejemplo: 2,4</small><textarea id="meses" rows="6">2,4
2,1
1,9
2,2
2,7
2,3</textarea></label>
<div class="row">
<label>Monto a actualizar ($)<input id="monto" type="number" inputmode="decimal" min="0" value="100000"></label>
<label>Tu aumento de sueldo en ese período (%) <small>opcional</small><input id="aum" type="number" inputmode="decimal" step="0.1" value="12"></label>
</div>
<div id="res" class="result"></div>
<p class="note">Los valores precargados son un ejemplo. Usá los datos oficiales del INDEC para tu período.</p>
</div>
<div class="article">
<h2>¿Cómo se calcula la inflación acumulada?</h2>
<p>La inflación de varios meses <strong>no se suma</strong>: se multiplica, porque cada mes los precios suben sobre los precios del mes anterior.</p>
<p><em>Inflación acumulada = (1 + i₁) × (1 + i₂) × … × (1 + iₙ) − 1</em></p>
<p>Por ejemplo, dos meses de 10 % no dan 20 %, sino 1,10 × 1,10 − 1 = <strong>21 %</strong>.</p>
<h3>¿De dónde saco los datos?</h3>
<p>El <strong>INDEC</strong> publica todos los meses el Índice de Precios al Consumidor (IPC) con la variación mensual. Cargá esos porcentajes, uno por línea, en el orden en que ocurrieron.</p>
<h3>¿Mi sueldo le ganó a la inflación?</h3>
<p>Si cargás el aumento que tuviste en el mismo período, te decimos si tu sueldo ganó o perdió poder de compra, y cuánto.</p>
</div>
''', faq=[
 ('¿Por qué la inflación acumulada es mayor que la suma de los meses?', 'Porque cada aumento se aplica sobre precios que ya habían subido. Es el mismo efecto que el interés compuesto.'),
 ('¿Qué es la inflación anualizada?', 'Es la inflación que tendrías en 12 meses si se repitiera el promedio mensual del período que cargaste.'),
 ('¿Dónde consulto la inflación oficial?', 'En el sitio del INDEC (indec.gob.ar), en la sección de Índice de Precios al Consumidor.'),
], script='''
conectar(() => {
  const m = lista('meses'), monto = val('monto'), aum = val('aum');
  if (!m.length) { $('#res').innerHTML = 'Cargá al menos un mes.'; return; }
  const fact = m.reduce((f, x) => f * (1 + x / 100), 1), acum = (fact - 1) * 100;
  const prom = (Math.pow(fact, 1 / m.length) - 1) * 100, anual = (Math.pow(1 + prom / 100, 12) - 1) * 100;
  let comp = '';
  if (aum) {
    const real = ((1 + aum / 100) / fact - 1) * 100;
    comp = `<p class="note ${real < 0 ? 'warn' : ''}">${real >= 0 ? '✓ Tu sueldo le ganó a la inflación' : '⚠ Tu sueldo perdió contra la inflación'}: ${real >= 0 ? 'ganaste' : 'perdiste'} ${pct(Math.abs(real))} de poder de compra.</p>`;
  }
  $('#res').innerHTML = `<div class="label">Inflación acumulada en ${m.length} ${m.length === 1 ? 'mes' : 'meses'}</div><div class="big">${pct(acum)}</div>` + filas([
    ['Promedio mensual', pct(prom)],
    ['Inflación anualizada', pct(anual)],
    [$$(monto) + ' de antes equivalen hoy a', $$(monto * fact), 'total'],
    [$$(monto) + ' de hoy compran lo que antes', $$(monto / fact)],
  ]) + comp;
});
''')

# ---------- ALQUILER ----------
page('alquiler', 'Calculadora de aumento de alquiler: ICL, IPC o porcentaje',
 'Calculá cuánto vas a pagar de alquiler con la próxima actualización: por porcentaje, por índice (ICL, IPC, CER, Casa Propia) o con la inflación de cada mes.',
 nombre='Aumento de alquiler', body='''
<h1>Calculadora de aumento de alquiler</h1>
<p class="lead">Calculá el nuevo valor de tu alquiler según cómo se actualice tu contrato.</p>
<div class="card calc">
<label>Alquiler actual ($)<input id="alq" type="number" inputmode="decimal" min="0" value="500000"></label>
<label>¿Cómo se actualiza tu contrato?<select id="modo">
<option value="pct">Por un porcentaje</option>
<option value="indice">Por un índice (ICL, IPC, CER, Casa Propia…)</option>
<option value="meses">Por la inflación de cada mes</option>
</select></label>
<div data-modo="pct"><label>Porcentaje de aumento (%)<input id="pct" type="number" inputmode="decimal" step="0.1" value="15"></label></div>
<div data-modo="indice" class="row">
<label>Valor del índice al inicio <small>del último período</small><input id="i0" type="number" inputmode="decimal" step="any" value="100"></label>
<label>Valor del índice ahora<input id="i1" type="number" inputmode="decimal" step="any" value="114.5"></label>
</div>
<div data-modo="meses"><label>Inflación de cada mes (%) <small>una por línea</small><textarea id="meses" rows="6">2,4
2,1
1,9
2,2
2,7
2,3</textarea></label></div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se actualiza el alquiler?</h2>
<p>Desde fines de 2023, en Argentina las partes pueden acordar libremente cómo y cada cuánto se actualiza el alquiler. Lo que vale es <strong>lo que dice tu contrato</strong>. Las formas más comunes son:</p>
<ul>
<li><strong>Por índice:</strong> el ICL (Índice para Contratos de Locación, del BCRA), el IPC (inflación del INDEC), el CER o el índice Casa Propia. Se divide el valor del índice actual por el del inicio del período y se multiplica por el alquiler.</li>
<li><strong>Por porcentaje fijo:</strong> por ejemplo, un 15 % cada cuatro meses.</li>
<li><strong>Por la inflación de cada mes:</strong> se acumula la inflación mensual del período.</li>
</ul>
<h3>La fórmula con índices</h3>
<p><em>Nuevo alquiler = alquiler actual × índice actual ÷ índice al inicio del período</em>.</p>
<h3>¿Dónde consulto los índices?</h3>
<p>El ICL lo publica el Banco Central (BCRA) a diario; el IPC, el INDEC una vez por mes. Usá los valores de las fechas que indica tu contrato.</p>
</div>
''', faq=[
 ('¿Cada cuánto me pueden aumentar el alquiler?', 'Depende del contrato. Desde el DNU 70/2023 la periodicidad y el índice son de libre acuerdo entre las partes; los contratos firmados antes siguen las reglas vigentes al momento de firmarlos.'),
 ('¿Qué es el ICL?', 'El Índice para Contratos de Locación lo publica el BCRA. Combina la inflación y la variación de los salarios, y se usó como índice obligatorio con la ley de alquileres de 2020.'),
], script='''
conectar(() => {
  modos('#modo');
  const alq = val('alq'), modo = $('#modo').value;
  let f = 1, det = '';
  if (modo === 'pct') { f = 1 + val('pct') / 100; det = 'Aumento del ' + pct(val('pct')); }
  else if (modo === 'indice') { const a = val('i0'), b = val('i1'); if (!a) { $('#res').innerHTML = 'Cargá el valor del índice al inicio.'; return; } f = b / a; det = 'Índice: ' + num.format(b) + ' ÷ ' + num.format(a); }
  else { const m = lista('meses'); f = m.reduce((x, y) => x * (1 + y / 100), 1); det = 'Inflación acumulada de ' + m.length + ' meses'; }
  const nuevo = alq * f;
  $('#res').innerHTML = `<div class="label">Nuevo alquiler</div><div class="big">${$$(nuevo)}</div>` + filas([
    ['Alquiler actual', $$(alq)],
    [det, pct((f - 1) * 100)],
    ['Diferencia por mes', '+ ' + $$(nuevo - alq)],
    ['Nuevo alquiler', $$(nuevo), 'total'],
  ]);
});
''')

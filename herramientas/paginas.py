# ---------- SUELDO NETO ----------
page('sueldo-neto', 'Calcular sueldo bruto a neto en Argentina (2026)',
 'Calculá tu sueldo neto (en mano) a partir del sueldo bruto: descuentos de jubilación 11 %, PAMI 3 %, obra social 3 % y sindicato. Gratis y al instante.',
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
 ('¿Cómo se calcula el sueldo neto a partir del bruto?', 'Al sueldo bruto se le resta el 17 % de aportes (11 % jubilación, 3 % PAMI y 3 % obra social) y la cuota sindical si estás afiliado. Por ejemplo, un bruto de $1.000.000 deja un neto de $830.000.'),
 ('¿Qué es el sueldo bruto y qué es el neto?', 'El bruto es el sueldo total antes de los descuentos; el neto es lo que efectivamente cobrás en mano, después de los aportes.'),
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
 ('¿Entre qué fechas me pueden dar las vacaciones?', 'En general entre el 1 de octubre y el 30 de abril, con aviso por escrito al menos 30 días antes (desde la Ley 27.802 de 2026). De común acuerdo se pueden tomar en otro momento del año.'),
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
<p>¿Encontraste un error o querés proponer una calculadora nueva? Escribinos a <a href="mailto:matiasj.carattoli@gmail.com">matiasj.carattoli@gmail.com</a>. También podés usar la página de <a href="../contacto/">Contacto</a>.</p>
</div>
''')

# ---------- INDEMNIZACIÓN ----------
page('indemnizacion', 'Calculadora de indemnización por despido sin causa (liquidación final)',
 'Calculá tu indemnización por despido sin causa: antigüedad (art. 245), preaviso, integración del mes, vacaciones no gozadas y aguinaldo proporcional.',
 nombre='Indemnización por despido', body='''
<h1>Calculadora de indemnización por despido</h1>
<p class="lead">Si te despidieron sin causa, calculá cuánto te corresponde cobrar en la liquidación final, rubro por rubro.</p>
<div class="card calc">
<label>Mejor sueldo bruto mensual del último año ($) <small>normal y habitual: sin aguinaldo, horas extra ni bonos extraordinarios</small><input id="sueldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
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
<p>Si no te avisaron con anticipación, te deben el preaviso: 1 mes si tenés menos de 5 años de antigüedad y 2 meses si tenés más. Desde la Ley 27.802 (2026), durante el período de prueba ya no corresponde preaviso.</p>
<h3>3. Integración del mes de despido (art. 233)</h3>
<p>Si el despido sin preaviso no fue el último día del mes, te pagan los días que faltan hasta fin de mes.</p>
<h3>4. Rubros que se cobran siempre</h3>
<ul>
<li>Los <strong>días trabajados</strong> del mes.</li>
<li>El <strong>aguinaldo proporcional</strong> del semestre.</li>
<li>Las <strong>vacaciones no gozadas</strong> proporcionales, con su aguinaldo.</li>
</ul>
<h3>Período de prueba</h3>
<p>Durante el período de prueba (en general los primeros 6 meses) no corresponde la indemnización por antigüedad ni, desde la Ley 27.802, el preaviso. Sí se cobran los días trabajados, el aguinaldo y las vacaciones proporcionales.</p>
<h3>La reforma laboral de 2026</h3>
<p>La Ley 27.802 de Modernización Laboral (marzo de 2026) mantuvo la indemnización de un sueldo por año, incorporó a la ley el piso del 67 % para el tope y aclaró que la base no incluye pagos no mensuales como el aguinaldo, ni horas extra ni bonificaciones extraordinarias. Algunos puntos están en discusión judicial y hay reglas de transición según la fecha del contrato.</p>
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
  const mesesPre = prueba ? 0 : anios >= 5 ? 2 : 1;
  const preav = conPreaviso ? 0 : sueldo * mesesPre;
  const finMes = new Date(fin.getFullYear(), fin.getMonth() + 1, 0).getDate();
  const integ = conPreaviso || prueba ? 0 : sueldo / 30 * (finMes - fin.getDate());
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
    ['Preaviso' + (prueba ? ' (no corresponde en período de prueba)' : conPreaviso ? ' (otorgado)' : ' (' + mesesPre + (mesesPre === 1 ? ' mes' : ' meses') + ')'), $$(preav)],
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

# ---------- MONOTRIBUTO ----------
# Valores vigentes desde el 1/08/2026 (ARCA). Actualizar en febrero y agosto.
MONO = [('A', 12009410.45, 49527.18, 49527.18), ('B', 17595182.74, 56379.08, 56379.08),
        ('C', 24670494.31, 66020.12, 64530.58), ('D', 30628651.43, 84612.93, 82564.81),
        ('E', 36028231.33, 119811.45, 108267.51), ('F', 45151659.41, 150784.21, 129930.65),
        ('G', 53995798.87, 230312.94, 158815.05), ('H', 81924660.37, 522706.68, 317895.01),
        ('I', 91699761.90, 963747.86, 474992.78), ('J', 105012519.20, 1167299.76, 580793.69),
        ('K', 126610838.75, 1614446.04, 702103.24)]
def _m(n): return f'{n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
tabla_mono = ''.join(f'<tr><td>{c}</td><td>$ {_m(t)}</td><td>$ {_m(s)}</td><td>$ {_m(v)}</td></tr>' for c, t, s, v in MONO)
page('monotributo', 'Calculadora de monotributo 2026: categoría y cuota mensual',
 'Calculá en qué categoría del monotributo estás según tu facturación y cuánto pagás por mes. Valores de ARCA vigentes desde agosto de 2026.',
 nombre='Monotributo', body=f'''
<h1>Calculadora de monotributo</h1>
<p class="lead">Poné cuánto facturás y te decimos en qué categoría te corresponde estar y cuánto pagás por mes.</p>
<div class="card calc">
<div class="row">
<label>Facturación<input id="ing" type="number" inputmode="decimal" min="0" value="2000000"></label>
<label>Período<select id="per"><option value="mes">Por mes (promedio)</option><option value="anio">Últimos 12 meses</option></select></label>
</div>
<label>Actividad<select id="act"><option value="s">Prestación de servicios</option><option value="v">Venta de cosas muebles</option></select></label>
<div id="res" class="result"></div>
<p class="note">Valores vigentes desde el 1 de agosto de 2026. La categoría también depende de la superficie, la energía consumida y el alquiler que pagás: si superás alguno de esos topes, te corresponde una categoría más alta.</p>
</div>
<div class="article">
<h2>Tabla de categorías del monotributo (desde agosto 2026)</h2>
<table class="detail big-table"><tr><th>Cat.</th><th>Facturación anual hasta</th><th>Cuota servicios</th><th>Cuota venta</th></tr>{tabla_mono}</table>
<p class="note">La cuota incluye el impuesto integrado, el aporte jubilatorio (SIPA) y la obra social. Fuente: ARCA.</p>
<h2>¿Cómo se elige la categoría?</h2>
<p>Se toma lo que facturaste en los <strong>últimos 12 meses</strong> y se busca la primera categoría cuyo tope no superás. Además hay otros parámetros (superficie del local, energía eléctrica y alquileres) que pueden subirte de categoría.</p>
<h3>Recategorización</h3>
<p>Dos veces por año, en <strong>enero y julio</strong>, tenés que revisar tu facturación y recategorizarte si cambió. Las escalas se actualizan por inflación en <strong>febrero y agosto</strong>.</p>
<h3>¿Qué pasa si supero la categoría K?</h3>
<p>Quedás <strong>excluido del monotributo</strong> y pasás al régimen general (responsable inscripto), con IVA y Ganancias. Conviene consultarlo con un contador antes de llegar al tope.</p>
</div>
''', faq=[
 ('¿Qué incluye la cuota del monotributo?', 'Tres conceptos: el impuesto integrado, el aporte al sistema jubilatorio (SIPA) y el aporte a la obra social. Si estás en relación de dependencia o sos jubilado, en algunos casos no pagás los aportes.'),
 ('¿Cuándo vence el monotributo?', 'La cuota vence todos los meses, en general el día 20. Se puede pagar con débito automático, tarjeta, homebanking o con el código de pago de ARCA.'),
 ('¿Cada cuánto cambian los valores?', 'Las escalas se actualizan dos veces por año según la inflación, en febrero y en agosto.'),
], script='''
const MONO = ''' + json.dumps([[c, t, s, v] for c, t, s, v in MONO]) + ''';
conectar(() => {
  const ing = val('ing'), anual = $('#per').value === 'mes' ? ing * 12 : ing, act = $('#act').value;
  const cat = MONO.find(c => anual <= c[1]);
  if (!cat) { $('#res').innerHTML = `<div class="label">Facturación anual de ${$$(anual)}</div><div class="big">Superás el monotributo</div><p class="note warn">El tope de la categoría K es ${$$(MONO[10][1])}. Te corresponde el régimen general: consultá con un contador.</p>`; return; }
  const cuota = act === 's' ? cat[2] : cat[3], margen = cat[1] - anual;
  $('#res').innerHTML = `<div class="label">Te corresponde la categoría</div><div class="big">${cat[0]}</div>` + filas([
    ['Facturación anual', $$(anual)],
    ['Tope de la categoría ' + cat[0], $$(cat[1])],
    ['Te queda de margen', $$(margen)],
    ['Cuota mensual', $$(cuota), 'total'],
  ]);
});
''')

# ---------- EMPLEADA DOMÉSTICA ----------
# Mínimos de noviembre 2026 (aumento 1,6 %, CNTCP). Formato: [hora con retiro, hora sin retiro, mes con retiro, mes sin retiro]
DOM = {'generales': ['Tareas generales', 4174.62, 4451.49, 512142.96, 562837.52],
       'cuidado': ['Asistencia y cuidado de personas', 4451.49, 4923.50, 562837.52, 620420.85],
       'especificas': ['Tareas específicas', 4700.21, 5098.84, 575394.53, 633782.08],
       'caseros': ['Caseros (solo sin retiro)', None, 4451.49, None, 562837.52]}
def _c(x): return '—' if x is None else '$ ' + _m(x)
tabla_dom = ''.join(f'<tr><td>{v[0]}</td><td>{_c(v[1])}</td><td>{_c(v[2])}</td><td>{_c(v[3])}</td><td>{_c(v[4])}</td></tr>' for v in DOM.values())
page('empleada-domestica', 'Calculadora de sueldo de empleada doméstica (noviembre 2026)',
 'Calculá el sueldo del personal de casas particulares por hora o por mes según la categoría, con antigüedad y zona desfavorable. Valores mínimos de noviembre 2026.',
 nombre='Sueldo de empleada doméstica', body=f'''
<h1>Sueldo de empleada doméstica</h1>
<p class="lead">Calculá cuánto corresponde pagarle al personal de casas particulares según la categoría y las horas.</p>
<div class="card calc">
<div class="row">
<label>Categoría<select id="cat"><option value="generales">Tareas generales</option><option value="cuidado">Cuidado de personas</option><option value="especificas">Tareas específicas</option><option value="caseros">Caseros</option></select></label>
<label>Modalidad<select id="mod"><option value="con">Con retiro</option><option value="sin">Sin retiro</option></select></label>
</div>
<div class="row">
<label>Forma de pago<select id="forma"><option value="hora">Por hora</option><option value="mes">Mensual (jornada completa)</option></select></label>
<label>Horas por semana <small>si es por hora</small><input id="hs" type="number" inputmode="decimal" min="0" value="12"></label>
</div>
<div class="row">
<label>Antigüedad (años) <small>+1 % por año</small><input id="ant" type="number" min="0" max="50" value="0"></label>
<label>Valor hora acordado ($) <small>opcional, si pagás más del mínimo</small><input id="propio" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<label class="check"><input id="zona" type="checkbox"> Zona desfavorable (+30 %)</label>
<div id="res" class="result"></div>
<p class="note">Valores mínimos de noviembre de 2026. Son pisos: se puede pagar más. Confirmá los montos en la resolución oficial de la Comisión Nacional de Trabajo en Casas Particulares.</p>
</div>
<div class="article">
<h2>Escala salarial de casas particulares (noviembre 2026)</h2>
<table class="detail big-table"><tr><th>Categoría</th><th>Hora c/retiro</th><th>Hora s/retiro</th><th>Mes c/retiro</th><th>Mes s/retiro</th></tr>{tabla_dom}</table>
<h2>¿Cómo se calcula?</h2>
<ul>
<li><strong>Por hora:</strong> valor hora × horas por semana × 4,33 (semanas promedio por mes).</li>
<li><strong>Mensual:</strong> se usa el sueldo mensual de la escala, que corresponde a una jornada completa.</li>
<li><strong>Antigüedad:</strong> se suma un 1 % del sueldo por cada año trabajado con el mismo empleador.</li>
<li><strong>Zona desfavorable:</strong> en La Pampa, Río Negro, Chubut, Neuquén, Santa Cruz, Tierra del Fuego y el partido de Patagones se suma un 30 %.</li>
</ul>
<h3>Si hace varias tareas</h3>
<p>Si la trabajadora hace tareas de distintas categorías (por ejemplo, limpieza y cuidado de chicos), corresponde pagarle toda la jornada con la categoría mejor paga.</p>
<h3>Aportes y aguinaldo</h3>
<p>Además del sueldo, el empleador paga los aportes y contribuciones en ARCA según las horas semanales, y corresponden aguinaldo, vacaciones y licencias como en cualquier trabajo registrado.</p>
</div>
''', faq=[
 ('¿Qué es con retiro y sin retiro?', 'Con retiro: la trabajadora vuelve a su casa al terminar la jornada. Sin retiro: vive en el lugar de trabajo. La modalidad sin retiro tiene valores más altos.'),
 ('¿La empleada doméstica cobra aguinaldo?', 'Sí. Cobra aguinaldo en junio y diciembre, igual que cualquier trabajador registrado: la mitad del mejor sueldo del semestre.'),
 ('¿Cuánto se paga por hora a una empleada doméstica en noviembre 2026?', 'El mínimo para tareas generales con retiro es de alrededor de $4.175 por hora, según la escala de noviembre de 2026.'),
], script='''
const DOM = ''' + json.dumps(DOM, ensure_ascii=False) + ''';
conectar(() => {
  const d = DOM[$('#cat').value], sin = $('#mod').value === 'sin' || $('#cat').value === 'caseros', mes = $('#forma').value === 'mes';
  const ant = Math.max(0, val('ant')), zona = $('#zona').checked, propio = val('propio'), hs = val('hs');
  const hora = propio > 0 ? propio : d[sin ? 2 : 1];
  const base = mes ? d[sin ? 4 : 3] : hora * hs * 52 / 12;
  const adAnt = base * ant / 100, adZona = base * (zona ? .3 : 0), total = base + adAnt + adZona;
  $('#res').innerHTML = `<div class="label">Sueldo mensual estimado</div><div class="big">${$$(total)}</div>` + filas([
    ['Categoría', d[0] + (sin ? ', sin retiro' : ', con retiro')],
    [mes ? 'Sueldo mensual de escala' : 'Valor hora × ' + num.format(hs) + ' h/semana', mes ? $$(base) : $$(hora) + ' → ' + $$(base)],
    ...(ant ? [['Antigüedad (' + ant + ' %)', '+ ' + $$(adAnt)]] : []),
    ...(zona ? [['Zona desfavorable (30 %)', '+ ' + $$(adZona)]] : []),
    ['Total', $$(total), 'total'],
  ]) + (mes ? '' : `<p class="note">Valor por semana: ${$$(hora * hs)}.</p>`);
});
''')

# ---------- DÍAS HÁBILES ----------
FERIADOS = {
 # 2026 (feriados nacionales; Decreto 1103/2026 agregó el 9/11)
 '2026-01-01': 'Año Nuevo', '2026-02-16': 'Carnaval', '2026-02-17': 'Carnaval', '2026-03-24': 'Día de la Memoria',
 '2026-04-02': 'Malvinas / Jueves Santo', '2026-04-03': 'Viernes Santo', '2026-05-01': 'Día del Trabajador', '2026-05-25': 'Revolución de Mayo',
 '2026-06-15': 'Paso a la Inmortalidad de Güemes', '2026-06-20': 'Día de la Bandera', '2026-07-09': 'Día de la Independencia',
 '2026-08-17': 'Paso a la Inmortalidad de San Martín', '2026-10-12': 'Día de la Diversidad Cultural', '2026-11-09': 'Visita del Papa León XIV',
 '2026-11-23': 'Día de la Soberanía Nacional', '2026-12-08': 'Inmaculada Concepción', '2026-12-25': 'Navidad',
 # 2027 (según la ley de feriados; puede cambiar por decreto)
 '2027-01-01': 'Año Nuevo', '2027-02-08': 'Carnaval', '2027-02-09': 'Carnaval', '2027-03-24': 'Día de la Memoria', '2027-03-26': 'Viernes Santo',
 '2027-04-02': 'Malvinas', '2027-05-01': 'Día del Trabajador', '2027-05-25': 'Revolución de Mayo', '2027-06-21': 'Paso a la Inmortalidad de Güemes',
 '2027-06-20': 'Día de la Bandera', '2027-07-09': 'Día de la Independencia', '2027-08-16': 'Paso a la Inmortalidad de San Martín',
 '2027-10-11': 'Día de la Diversidad Cultural', '2027-11-20': 'Día de la Soberanía Nacional', '2027-12-08': 'Inmaculada Concepción', '2027-12-25': 'Navidad',
}
NO_LABORABLES = {'2026-03-23': 'Día no laborable con fines turísticos', '2026-07-10': 'Día no laborable con fines turísticos',
                 '2026-12-07': 'Día no laborable con fines turísticos', '2027-03-25': 'Jueves Santo (no laborable)'}
page('dias-habiles', 'Calculadora de días hábiles entre dos fechas (Argentina)',
 'Calculá cuántos días hábiles hay entre dos fechas en Argentina, descontando fines de semana y feriados nacionales 2026 y 2027. También suma días hábiles a una fecha.',
 nombre='Días hábiles', body='''
<h1>Calculadora de días hábiles</h1>
<p class="lead">Contá los días hábiles entre dos fechas o averiguá qué fecha es dentro de X días hábiles, con los feriados de Argentina.</p>
<div class="card calc">
<label>¿Qué querés calcular?<select id="modo"><option value="entre">Días hábiles entre dos fechas</option><option value="sumar">Sumar días hábiles a una fecha</option></select></label>
<div class="row">
<label>Desde<input id="d0" type="date"></label>
<div data-modo="entre"><label>Hasta<input id="d1" type="date"></label></div>
<div data-modo="sumar"><label>Cantidad de días hábiles<input id="n" type="number" min="1" max="500" value="10"></label></div>
</div>
<label class="check"><input id="nolab" type="checkbox" checked> Contar los días no laborables (turísticos y Jueves Santo) como no hábiles</label>
<div id="res" class="result"></div>
<p class="note">Incluye los feriados nacionales de 2026 y 2027. Los feriados provinciales o locales no están incluidos.</p>
</div>
<div class="article">
<h2>¿Qué es un día hábil?</h2>
<p>En general, son los días de <strong>lunes a viernes que no son feriados</strong>. Los sábados, domingos y feriados nacionales no cuentan. Los <strong>días no laborables</strong> (como los "puentes" turísticos) son optativos para el empleador: en la administración pública no se trabaja, pero en el sector privado depende de cada empresa.</p>
<h3>¿Para qué sirve?</h3>
<ul>
<li>Calcular plazos legales: por ejemplo, el pago de la liquidación final vence a los <strong>4 días hábiles</strong>.</li>
<li>Saber cuándo llega una transferencia o un trámite que tarda "X días hábiles".</li>
<li>Planificar entregas, vencimientos y vacaciones.</li>
</ul>
<p>Mirá también nuestra guía con el <a href="../guias/feriados-2026/">calendario completo de feriados 2026</a>.</p>
</div>
''', faq=[
 ('¿El sábado es día hábil?', 'En la mayoría de los trámites y plazos no: se cuentan solo los días de lunes a viernes que no son feriados. Algunos plazos laborales sí consideran el sábado; revisá la norma que aplica en tu caso.'),
 ('¿Los días no laborables son hábiles?', 'Para la administración pública no. En el sector privado, el empleador decide si se trabaja. Por eso la calculadora te deja elegir.'),
], script='''
const FER = ''' + json.dumps(FERIADOS, ensure_ascii=False) + ''', NOLAB = ''' + json.dumps(NO_LABORABLES, ensure_ascii=False) + ''';
const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
if (!$('#d0').value) $('#d0').value = iso(hoy);
if (!$('#d1').value) { const x = new Date(hoy); x.setMonth(x.getMonth() + 1); $('#d1').value = iso(x); }
const fmt = d => d.toLocaleDateString('es-AR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
conectar(() => {
  modos('#modo');
  const nolab = $('#nolab').checked;
  const libre = d => { const k = iso(d), w = d.getDay(); return w === 0 || w === 6 || FER[k] || (nolab && NOLAB[k]); };
  const p = v => v ? new Date(v + 'T00:00:00') : null;
  const a = p($('#d0').value);
  if (!a) { $('#res').innerHTML = 'Elegí una fecha de inicio.'; return; }
  if ($('#modo').value === 'entre') {
    let b = p($('#d1').value); if (!b) { $('#res').innerHTML = 'Elegí la fecha final.'; return; }
    let x = new Date(Math.min(a, b)), fin = new Date(Math.max(a, b)), hab = 0, tot = 0, fer = [];
    while (x <= fin) { tot++; if (!libre(x)) hab++; else { const k = iso(x); if (FER[k] || (nolab && NOLAB[k])) fer.push(x.toLocaleDateString('es-AR', { day: 'numeric', month: 'short' }) + ': ' + (FER[k] || NOLAB[k])); } x.setDate(x.getDate() + 1); }
    $('#res').innerHTML = `<div class="label">Días hábiles (incluyendo ambas fechas)</div><div class="big">${hab}</div>` + filas([
      ['Días corridos', tot], ['Fines de semana y feriados', tot - hab]]) + (fer.length ? `<p class="note">Feriados en el período: ${fer.join(' · ')}</p>` : '');
  } else {
    const n = Math.max(1, Math.round(val('n'))); let x = new Date(a), c = 0;
    while (c < n) { x.setDate(x.getDate() + 1); if (!libre(x)) c++; }
    $('#res').innerHTML = `<div class="label">${n} días hábiles después del ${a.toLocaleDateString('es-AR')}</div><div class="big">${x.toLocaleDateString('es-AR')}</div><p class="note">Es ${fmt(x)}.</p>`;
  }
});
''')

# =================== GUÍAS ===================
def _rel(slug): return next(g[3] for g in GUIAS if g[0] == slug)
def _filas_fer(lista):
    return '<table class="detail big-table"><tr><th>Fecha</th><th>Feriado</th><th>Tipo</th></tr>' + ''.join(
        f'<tr><td>{f}</td><td>{n}</td><td>{t}</td></tr>' for f, n, t in lista) + '</table>'

page('guias/feriados-2026', 'Feriados 2026 en Argentina: calendario completo y fines de semana largos',
 'Todos los feriados 2026 en Argentina: inamovibles, trasladables, días no laborables, el feriado del 9 de noviembre por la visita del Papa y los fines de semana largos que quedan.',
 nombre='Feriados 2026', articulo=True, relacionadas=_rel('feriados-2026'), body='<h1>Feriados 2026 en Argentina</h1>' + '''
<p class="lead">El calendario completo de feriados nacionales y días no laborables de 2026, con los fines de semana largos que quedan en el año.</p>
<p class="note">Actualizado el 4 de noviembre de 2026.</p>
<h2>Lo que queda de 2026</h2>
<ul>
<li><strong>Lunes 9 de noviembre:</strong> feriado nacional por la visita del Papa León XIV (Decreto 1103/2026). Fin de semana largo del 7 al 9.</li>
<li><strong>Martes 10 de noviembre:</strong> feriado solo en la Ciudad de Buenos Aires y en Córdoba.</li>
<li><strong>Miércoles 11 de noviembre:</strong> feriado solo en la provincia de Buenos Aires.</li>
<li><strong>Lunes 23 de noviembre:</strong> Día de la Soberanía Nacional (trasladado del viernes 20). Fin de semana largo del 21 al 23.</li>
<li><strong>Lunes 7 de diciembre:</strong> día no laborable con fines turísticos.</li>
<li><strong>Martes 8 de diciembre:</strong> Inmaculada Concepción. Con el puente, fin de semana largo de cuatro días, del 5 al 8.</li>
<li><strong>Viernes 25 de diciembre:</strong> Navidad. Fin de semana largo del 25 al 27.</li>
</ul>
<h2>Calendario completo de feriados 2026</h2>
''' + _filas_fer([
 ('Jueves 1 de enero', 'Año Nuevo', 'Inamovible'), ('Lunes 16 y martes 17 de febrero', 'Carnaval', 'Inamovible'),
 ('Lunes 23 de marzo', 'Puente turístico', 'No laborable'), ('Martes 24 de marzo', 'Día Nacional de la Memoria por la Verdad y la Justicia', 'Inamovible'),
 ('Jueves 2 de abril', 'Día del Veterano y de los Caídos en Malvinas (y Jueves Santo)', 'Inamovible'), ('Viernes 3 de abril', 'Viernes Santo', 'Inamovible'),
 ('Viernes 1 de mayo', 'Día del Trabajador', 'Inamovible'), ('Lunes 25 de mayo', 'Revolución de Mayo', 'Inamovible'),
 ('Lunes 15 de junio', 'Paso a la Inmortalidad del Gral. Güemes (del 17/6)', 'Trasladable'), ('Sábado 20 de junio', 'Paso a la Inmortalidad del Gral. Belgrano', 'Inamovible'),
 ('Jueves 9 de julio', 'Día de la Independencia', 'Inamovible'), ('Viernes 10 de julio', 'Puente turístico', 'No laborable'),
 ('Lunes 17 de agosto', 'Paso a la Inmortalidad del Gral. San Martín', 'Trasladable'), ('Lunes 12 de octubre', 'Día del Respeto a la Diversidad Cultural', 'Trasladable'),
 ('Lunes 9 de noviembre', 'Visita del Papa León XIV', 'Feriado nacional (Decreto 1103/2026)'), ('Lunes 23 de noviembre', 'Día de la Soberanía Nacional (del 20/11)', 'Trasladable'),
 ('Lunes 7 de diciembre', 'Puente turístico', 'No laborable'), ('Martes 8 de diciembre', 'Inmaculada Concepción de María', 'Inamovible'),
 ('Viernes 25 de diciembre', 'Navidad', 'Inamovible')]) + '''
<h2>Feriado, día no laborable y puente: ¿qué diferencia hay?</h2>
<ul>
<li><strong>Feriado inamovible:</strong> se respeta en su fecha. No se trabaja, y si trabajás, te lo tienen que pagar doble.</li>
<li><strong>Feriado trasladable:</strong> si cae martes o miércoles, pasa al lunes anterior; si cae jueves o viernes, al lunes siguiente.</li>
<li><strong>Día no laborable (puente turístico):</strong> en el sector público no se trabaja; en el privado, decide el empleador. Si trabajás, cobrás el sueldo normal, sin recargo.</li>
</ul>
<h2>¿Cuánto me pagan si trabajo un feriado?</h2>
<p>Si trabajás un feriado nacional, te corresponde cobrar ese día <strong>doble</strong>. Si es un día no laborable y el empleador decide que se trabaje, se paga como un día común.</p>
<p>Para contar plazos que excluyen feriados, usá la <a href="../../dias-habiles/">calculadora de días hábiles</a>.</p>
''', faq=[
 ('¿El 9 de noviembre de 2026 es feriado?', 'Sí. El Decreto 1103/2026 lo declaró feriado nacional por la visita del Papa León XIV. El 10 es feriado solo en CABA y Córdoba, y el 11 solo en la provincia de Buenos Aires.'),
 ('¿El 7 de diciembre de 2026 es feriado?', 'No: es un día no laborable con fines turísticos. En el sector privado decide el empleador.'),
 ('¿Cuántos fines de semana largos quedan en 2026?', 'Desde noviembre quedan cuatro: del 7 al 9 de noviembre, del 21 al 23 de noviembre, del 5 al 8 de diciembre y del 25 al 27 de diciembre.'),
])

page('guias/aguinaldo-diciembre-2026', 'Aguinaldo diciembre 2026: cuándo se cobra y cómo calcularlo',
 'Cuándo se paga el aguinaldo de diciembre 2026, cómo se calcula el medio aguinaldo completo o proporcional, cuánto se descuenta y ejemplos con números.',
 nombre='Aguinaldo de diciembre 2026', articulo=True, relacionadas=_rel('aguinaldo-diciembre-2026'), body='''
<h1>Aguinaldo de diciembre 2026: cuándo se cobra y cuánto te toca</h1>
<p class="lead">Todo lo que tenés que saber sobre la segunda cuota del aguinaldo: fecha de pago, cómo se calcula y ejemplos.</p>
<p class="note">Actualizado el 4 de noviembre de 2026.</p>
<h2>¿Cuándo se cobra el aguinaldo de diciembre 2026?</h2>
<p>La segunda cuota del aguinaldo (o SAC, sueldo anual complementario) vence el <strong>viernes 18 de diciembre de 2026</strong>. Los empleadores tienen un plazo de gracia de <strong>4 días hábiles</strong>, así que el pago puede llegar hasta el <strong>jueves 24 de diciembre</strong>.</p>
<h2>¿Cómo se calcula?</h2>
<p>El aguinaldo es el <strong>50 % del mejor sueldo bruto</strong> que cobraste entre julio y diciembre. Se toma el sueldo con todos los conceptos remunerativos: básico, antigüedad, presentismo, horas extra y comisiones.</p>
<h3>Ejemplo: aguinaldo completo</h3>
<p>Si trabajaste todo el semestre y tu mejor sueldo bruto fue de $1.200.000, el aguinaldo bruto es de <strong>$600.000</strong>. Con los descuentos del 17 % (jubilación, PAMI y obra social), cobrás unos <strong>$498.000</strong> en mano.</p>
<h3>Ejemplo: aguinaldo proporcional</h3>
<p>Si entraste a trabajar el 1 de octubre, trabajaste 92 de los 184 días del semestre. Con un mejor sueldo de $1.000.000: $1.000.000 ÷ 2 × 92 ÷ 184 = <strong>$250.000</strong> brutos.</p>
<p>Hacé tu cuenta exacta con la <a href="../../aguinaldo/">calculadora de aguinaldo</a>.</p>
<h2>¿Quiénes cobran aguinaldo?</h2>
<ul>
<li>Todos los trabajadores en relación de dependencia registrados, del sector privado y público.</li>
<li>El personal de casas particulares.</li>
<li>Los jubilados y pensionados, que lo cobran junto con el haber de diciembre.</li>
</ul>
<p>Los monotributistas y autónomos no cobran aguinaldo, porque no tienen un empleador.</p>
<h2>¿El aguinaldo paga Ganancias?</h2>
<p>Sí: si tu sueldo supera el mínimo, el aguinaldo se suma a tus ingresos del año para el impuesto a las ganancias, y la retención puede aparecer en el recibo de diciembre.</p>
''', faq=[
 ('¿Hasta qué día me pueden pagar el aguinaldo de diciembre 2026?', 'Vence el 18 de diciembre, pero el empleador tiene 4 días hábiles más: el último día es el jueves 24 de diciembre de 2026.'),
 ('¿Se puede pagar el aguinaldo en cuotas?', 'No, en principio debe pagarse completo. Solo algunos convenios o acuerdos homologados permiten otras modalidades.'),
 ('Si me fui de la empresa, ¿cobro aguinaldo?', 'Sí, te corresponde el aguinaldo proporcional a los días trabajados en el semestre, que se paga con la liquidación final.'),
])

page('guias/como-calcular-indemnizacion', 'Cómo calcular la indemnización por despido sin causa paso a paso',
 'Guía para calcular la indemnización por despido sin causa en Argentina: antigüedad, preaviso, integración del mes, vacaciones y aguinaldo proporcional, con un ejemplo.',
 nombre='Cómo calcular la indemnización', articulo=True, relacionadas=_rel('como-calcular-indemnizacion'), body='''
<h1>Cómo calcular la indemnización por despido</h1>
<p class="lead">Si te despidieron sin causa, esto es lo que te corresponde cobrar, explicado rubro por rubro y con un ejemplo.</p>
<h2>1. Indemnización por antigüedad</h2>
<p>Es <strong>un sueldo por cada año trabajado</strong>, o por cada fracción mayor a tres meses (art. 245 de la Ley de Contrato de Trabajo). Se toma la mejor remuneración mensual, normal y habitual del último año. Nunca puede ser menor a un sueldo.</p>
<h2>2. Preaviso</h2>
<p>Si no te avisaron del despido con anticipación, te deben el preaviso:</p>
<ul>
<li><strong>Nada</strong> si estabas en el período de prueba (desde la Ley 27.802 de 2026).</li>
<li><strong>1 mes</strong> si tenías menos de 5 años de antigüedad.</li>
<li><strong>2 meses</strong> si tenías 5 años o más.</li>
</ul>
<h2>3. Integración del mes de despido</h2>
<p>Si te despidieron sin preaviso y no fue el último día del mes, te pagan los días que faltaban hasta fin de mes.</p>
<h2>4. Lo que se cobra siempre</h2>
<ul>
<li>Los <strong>días trabajados</strong> del último mes.</li>
<li>El <strong>aguinaldo proporcional</strong> del semestre.</li>
<li>Las <strong>vacaciones no gozadas</strong> proporcionales, con su aguinaldo.</li>
</ul>
<h2>Ejemplo</h2>
<p>Ana entró el 1 de marzo de 2021 y la despidieron sin causa ni preaviso el 15 de noviembre de 2026, con un sueldo de $1.000.000. Tiene 5 años y 8 meses de antigüedad, así que:</p>
<ul>
<li>Antigüedad: 6 sueldos (5 años + la fracción de 8 meses) = $6.000.000.</li>
<li>Preaviso: 2 meses = $2.000.000.</li>
<li>Integración: 15 días = $500.000.</li>
<li>Más los días trabajados, el aguinaldo proporcional y las vacaciones.</li>
</ul>
<p>En total, Ana debería cobrar más de <strong>$10 millones</strong>. Hacé tu propio cálculo con la <a href="../../indemnizacion/">calculadora de indemnización</a>.</p>
<h2>¿Cuándo me la tienen que pagar?</h2>
<p>La liquidación final debe pagarse dentro de los <strong>4 días hábiles</strong> posteriores al despido. Antes de firmar cualquier acuerdo, consultá con un abogado laboralista o en el Ministerio de Trabajo.</p>
<h2>¿Qué cambió con la reforma laboral de 2026?</h2>
<p>La <strong>Ley 27.802 de Modernización Laboral</strong> (publicada el 6 de marzo de 2026) mantuvo el cálculo de un sueldo por año, pero aclaró que la base es solo la remuneración <strong>mensual, normal y habitual</strong>: no entran el aguinaldo, las vacaciones, las horas extra ni los bonos extraordinarios. También incorporó a la ley el piso del 67 % para el tope, eliminó el preaviso durante el período de prueba y creó el Fondo de Asistencia Laboral, que no reemplaza tu indemnización. Algunos artículos, como el pago en cuotas, fueron cuestionados en la Justicia.</p>
<p class="warn">Las leyes laborales cambian. Esta guía es orientativa y no reemplaza el asesoramiento profesional.</p>
''', faq=[
 ('¿La indemnización paga impuestos?', 'La indemnización por antigüedad, el preaviso y la integración no llevan aportes ni pagan Ganancias. Los días trabajados, el aguinaldo y las vacaciones sí llevan aportes.'),
 ('¿Me corresponde indemnización en el período de prueba?', 'No corresponde la indemnización por antigüedad y, desde la Ley 27.802 de 2026, tampoco el preaviso. Sí cobrás los días trabajados, el aguinaldo y las vacaciones proporcionales.'),
])

page('guias/cuotas-o-contado', '¿Conviene pagar en cuotas o de contado? Cómo decidir con inflación',
 'Cómo saber si conviene pagar en cuotas o de contado en Argentina: cuotas sin interés, descuentos por efectivo, inflación y el valor actual de las cuotas, con ejemplos.',
 nombre='¿Cuotas o contado?', articulo=True, relacionadas=_rel('cuotas-o-contado'), body='''
<h1>¿Conviene pagar en cuotas o de contado?</h1>
<p class="lead">Con inflación, pagar en cuotas puede salir más barato aunque tenga recargo. Te explicamos cómo hacer la cuenta.</p>
<h2>La clave: lo que valen hoy tus cuotas</h2>
<p>Una cuota de $100.000 que pagás dentro de seis meses no "pesa" lo mismo que $100.000 hoy, porque para entonces los precios (y en general los sueldos) subieron. Para comparar de forma justa hay que llevar las cuotas a <strong>valor de hoy</strong>, descontándoles la inflación esperada.</p>
<h2>Tres casos típicos</h2>
<h3>1. Cuotas sin interés y sin descuento de contado</h3>
<p>Conviene casi siempre pagar en cuotas: pagás lo mismo, pero más adelante, con pesos que valen menos.</p>
<h3>2. Cuotas sin interés, pero con descuento por pagar de contado</h3>
<p>Depende del descuento y de la inflación. Ejemplo: un producto de $600.000 en 6 cuotas sin interés o $540.000 de contado (10 % de descuento). Con una inflación del 2 % mensual, las 6 cuotas de $100.000 valen hoy unos $560.000: <strong>conviene el contado</strong>, porque $540.000 es menos.</p>
<h3>3. Cuotas con interés</h3>
<p>Calculá la tasa de interés mensual que te cobran y comparala con la inflación que esperás. Si la tasa es <strong>menor</strong> que la inflación, las cuotas te convienen.</p>
<p>Hacé tu cuenta con la <a href="../../cuotas/">calculadora de cuotas o contado</a>.</p>
<h2>Ojo con esto</h2>
<ul>
<li><strong>Los costos de la tarjeta:</strong> a veces la cuota que te muestran no incluye impuestos, seguros o comisiones.</li>
<li><strong>El pago mínimo:</strong> si después no podés pagar el total del resumen, los intereses de la tarjeta son muy altos y anulan cualquier ventaja.</li>
<li><strong>La plata que no gastás:</strong> si pagás en cuotas, el dinero que te queda tiene que estar a salvo de la inflación (por ejemplo, en una cuenta remunerada o un plazo fijo). Si lo dejás quieto, la ventaja se achica.</li>
</ul>
''', faq=[
 ('¿Qué son las cuotas sin interés?', 'Son cuotas que suman el mismo precio que el contado de lista. Pero si el comercio ofrece un descuento por pagar en efectivo, en realidad sí tienen un costo.'),
 ('¿Qué inflación uso para comparar?', 'La que esperás para los próximos meses. Una referencia es el último dato mensual del INDEC o el Relevamiento de Expectativas de Mercado del BCRA.'),
])

# ---------- SUELDO BRUTO DESDE NETO ----------
page('sueldo-bruto', 'Sueldo bruto: calcular el bruto a partir del neto',
 'Calculá qué sueldo bruto necesitás para cobrar un determinado neto en mano. Ideal para negociar un sueldo o una oferta de trabajo.',
 nombre='Sueldo bruto desde el neto', body='''
<h1>Calculadora de sueldo bruto desde el neto</h1>
<p class="lead">¿Querés cobrar una cifra en mano? Te decimos cuánto tiene que ser el sueldo bruto para llegar a eso.</p>
<div class="card calc">
<label>Sueldo neto que querés cobrar ($)<input id="neto" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Aporte sindical (%) <small>0 si no estás afiliado</small><input id="sind" type="number" inputmode="decimal" min="0" step="0.1" value="0"></label>
<label>Tope de aportes ($) <small>opcional, 0 = sin tope</small><input id="tope" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se pasa de neto a bruto?</h2>
<p>En relación de dependencia te descuentan un <strong>17 %</strong> del bruto (11 % jubilación, 3 % PAMI y 3 % obra social), más la cuota sindical si estás afiliado. Por eso, para saber el bruto hay que <strong>dividir</strong> el neto por lo que queda después de los descuentos:</p>
<p><em>Bruto = neto ÷ (1 − 0,17 − sindicato)</em></p>
<p>Por ejemplo, para cobrar $1.000.000 en mano sin sindicato, el bruto tiene que ser $1.000.000 ÷ 0,83 = <strong>$1.204.819</strong>. No alcanza con sumarle el 17 % al neto: eso daría $1.170.000 y te quedarías corto.</p>
<h3>¿Para qué sirve?</h3>
<p>En las entrevistas y en las ofertas de trabajo casi siempre se habla de sueldo <strong>bruto</strong>. Si sabés cuánto necesitás en mano, con esta cuenta sabés qué cifra pedir.</p>
</div>
''', faq=[
 ('¿Cuál es el sueldo bruto?', 'Es el sueldo total que figura en tu contrato o recibo antes de los descuentos de jubilación, PAMI, obra social y sindicato. Es la cifra que se usa en las ofertas de trabajo.'),
 ('¿Cuánto es el bruto de un sueldo neto?', 'Sin sindicato, el bruto es el neto dividido 0,83. Por ejemplo, un neto de $830.000 corresponde a un bruto de $1.000.000.'),
 ('¿El cálculo incluye Ganancias?', 'No. Si tu sueldo está alcanzado por el impuesto a las ganancias, vas a necesitar un bruto mayor para llegar al mismo neto.'),
], script='''
conectar(() => {
  const neto = val('neto'), s = val('sind') / 100, tope = val('tope');
  let bruto = neto / (1 - .17 - s);
  if (tope > 0 && bruto > tope) bruto = (neto + .17 * tope) / (1 - s);
  const base = tope > 0 ? Math.min(bruto, tope) : bruto;
  $('#res').innerHTML = `<div class="label">Necesitás un sueldo bruto de</div><div class="big">${$$(bruto)}</div>` + filas([
    ['Aportes (17 %)', '− ' + $$(base * .17)],
    ...(s ? [['Sindicato (' + pct(s * 100) + ')', '− ' + $$(bruto * s)]] : []),
    ['Neto en mano', $$(neto), 'total'],
  ]) + '<p class="note">No incluye impuesto a las ganancias.</p>';
});
''')

# ---------- PRECIO DE VENTA ----------
page('precio-de-venta', 'Calculadora de precio de venta: costo, ganancia, comisiones e IVA',
 'Calculá a qué precio vender un producto para ganar lo que querés, teniendo en cuenta el costo, la comisión de Mercado Libre o Mercado Pago, el envío y el IVA.',
 nombre='Precio de venta', body='''
<h1>Calculadora de precio de venta</h1>
<p class="lead">Para emprendedores y vendedores: calculá a qué precio publicar para ganar lo que querés después de comisiones e impuestos.</p>
<div class="card calc">
<div class="row">
<label>Costo del producto ($)<input id="costo" type="number" inputmode="decimal" min="0" value="10000"></label>
<label>Ganancia que querés (%) <small>sobre el costo</small><input id="gan" type="number" inputmode="decimal" step="0.1" value="50"></label>
</div>
<div class="row">
<label>Comisión de la plataforma (%) <small>Mercado Libre, Mercado Pago, tarjeta…</small><input id="com" type="number" inputmode="decimal" min="0" step="0.1" value="13"></label>
<label>Costo fijo por venta ($) <small>envío, packaging…</small><input id="fijo" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<label class="check"><input id="iva" type="checkbox"> Sumar IVA (21 %) — si sos responsable inscripto</label>
<div id="res" class="result"></div>
<p class="note">Cargá la comisión actual de tu plataforma: cambia según la categoría, el tipo de publicación y el plazo de cobro.</p>
</div>
<div class="article">
<h2>¿Cómo calcular el precio de venta?</h2>
<p>El error más común es sumarle la ganancia al costo y listo. Pero si vendés por una plataforma, la <strong>comisión se cobra sobre el precio final</strong>, no sobre el costo. Por eso hay que calcular el precio "de atrás para adelante":</p>
<p><em>Precio = (costo + ganancia + costos fijos) ÷ (1 − comisión)</em></p>
<p>Si además sos responsable inscripto, al precio sin impuestos se le suma el 21 % de IVA.</p>
<h3>Ganancia sobre el costo y margen sobre la venta</h3>
<p>No son lo mismo. Si un producto te cuesta $100 y lo vendés a $150, ganaste un <strong>50 % sobre el costo</strong>, pero tu <strong>margen sobre la venta</strong> es del 33 % ($50 de cada $150). La calculadora te muestra los dos.</p>
<h3>Si sos monotributista</h3>
<p>No sumás IVA, pero tené en cuenta la cuota mensual del monotributo dentro de tus costos. Podés calcularla con la <a href="../monotributo/">calculadora de monotributo</a>.</p>
</div>
''', faq=[
 ('¿Cuánto cobra de comisión Mercado Libre?', 'Depende de la categoría del producto y del tipo de publicación (clásica o premium), y cambia con el tiempo. Revisá el costo exacto al publicar y cargalo en la calculadora.'),
 ('¿Qué diferencia hay entre markup y margen?', 'El markup es la ganancia sobre el costo; el margen es la ganancia sobre el precio de venta. Un markup del 100 % equivale a un margen del 50 %.'),
], script='''
conectar(() => {
  const costo = val('costo'), gan = val('gan') / 100, com = val('com') / 100, fijo = val('fijo'), iva = $('#iva').checked ? .21 : 0;
  const neto = costo * (1 + gan) + fijo, div = 1 / (1 + iva) - com;
  if (div <= 0) { $('#res').innerHTML = 'La comisión es demasiado alta.'; return; }
  const precio = neto / div, comision = precio * com, impuesto = precio - precio / (1 + iva), ganancia = costo * gan;
  $('#res').innerHTML = `<div class="label">Precio de venta</div><div class="big">${$$(precio)}</div>` + filas([
    ['Costo', $$(costo)],
    ...(fijo ? [['Costos fijos', $$(fijo)]] : []),
    ['Comisión de la plataforma (' + pct(com * 100) + ')', $$(comision)],
    ...(iva ? [['IVA (21 %)', $$(impuesto)]] : []),
    ['Tu ganancia', $$(ganancia), 'total'],
    ['Margen sobre la venta', precio ? pct(ganancia / precio * 100) : '—'],
  ]);
});
''')

# ---------- META DE AHORRO ----------
page('ahorro-objetivo', 'Calculadora de meta de ahorro: cuánto ahorrar por mes',
 'Calculá cuánto tenés que ahorrar por mes para llegar a tu objetivo (un viaje, un auto, un fondo de emergencia), con o sin rendimiento.',
 nombre='Meta de ahorro', body='''
<h1>¿Cuánto tengo que ahorrar por mes?</h1>
<p class="lead">Poné tu meta y el plazo, y te decimos cuánto separar cada mes para llegar.</p>
<div class="card calc">
<div class="row">
<label>Meta ($)<input id="meta" type="number" inputmode="decimal" min="0" value="5000000"></label>
<label>Plazo (meses)<input id="n" type="number" min="1" max="600" value="12"></label>
</div>
<div class="row">
<label>Lo que ya tenés ahorrado ($)<input id="ya" type="number" inputmode="decimal" min="0" value="0"></label>
<label>Rendimiento anual (%) <small>opcional, TEA de donde ahorrás</small><input id="tea" type="number" inputmode="decimal" step="0.1" value="0"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>Cómo armar un plan de ahorro</h2>
<ol>
<li><strong>Definí la meta en números:</strong> cuánto cuesta lo que querés y para cuándo.</li>
<li><strong>Calculá el ahorro mensual</strong> con esta calculadora.</li>
<li><strong>Separalo apenas cobrás,</strong> no "lo que sobre a fin de mes". Una transferencia automática ayuda mucho.</li>
<li><strong>Hacé que la plata rinda:</strong> una cuenta remunerada, un fondo común de inversión o un plazo fijo hacen que necesites ahorrar menos por mes.</li>
</ol>
<h3>Ojo con la inflación</h3>
<p>Si tu meta es comprar algo que sube de precio, ajustá la meta por la inflación esperada o revisala cada algunos meses. Podés estimar cuánto va a costar con la <a href="../inflacion/">calculadora de inflación</a>.</p>
</div>
''', faq=[
 ('¿Cuánto conviene tener de fondo de emergencia?', 'Una referencia habitual es entre 3 y 6 meses de tus gastos fijos, en un lugar donde lo puedas sacar rápido.'),
 ('¿Qué rendimiento pongo?', 'La tasa efectiva anual (TEA) del lugar donde vas a ahorrar. Si no sabés, dejalo en 0 y la calculadora te da el ahorro sin intereses.'),
], script='''
conectar(() => {
  const meta = val('meta'), n = Math.max(1, Math.round(val('n'))), ya = val('ya'), tea = val('tea') / 100;
  const i = Math.pow(1 + tea, 1 / 12) - 1, crece = Math.pow(1 + i, n);
  const falta = meta - ya * crece;
  if (falta <= 0) { $('#res').innerHTML = `<div class="label">¡Ya llegás!</div><div class="big">${$$(0)} por mes</div><p class="note">Con lo que tenés ahorrado${tea ? ' y el rendimiento' : ''} alcanzás la meta.</p>`; return; }
  const cuota = i ? falta * i / (crece - 1) : falta / n, aportado = ya + cuota * n;
  $('#res').innerHTML = `<div class="label">Tenés que ahorrar por mes</div><div class="big">${$$(cuota)}</div>` + filas([
    ['Total que vas a poner', $$(aportado)],
    ['Lo que te dan los intereses', $$(meta - aportado)],
    ['Meta', $$(meta), 'total'],
  ]);
});
''')

# ---------- CONVERSOR DE TASAS ----------
page('tasas', 'Conversor de tasas: TNA a TEA y a tasa mensual (TEM)',
 'Convertí tasas de interés al instante: de TNA a TEA, de TEA a TNA y a tasa efectiva mensual (TEM), para plazos fijos, préstamos y billeteras virtuales.',
 nombre='Conversor de tasas', body='''
<h1>Conversor de tasas: TNA, TEA y TEM</h1>
<p class="lead">Pasá cualquier tasa a las otras para comparar plazos fijos, cuentas remuneradas y préstamos.</p>
<div class="card calc">
<div class="row">
<label>Tasa (%)<input id="t" type="number" inputmode="decimal" step="0.01" value="30"></label>
<label>Tipo de tasa<select id="tipo"><option value="tna">TNA (nominal anual)</option><option value="tea">TEA (efectiva anual)</option><option value="tem">TEM (efectiva mensual)</option></select></label>
</div>
<label>Período de capitalización (días) <small>30 para plazos fijos mensuales, 1 para cuentas que pagan a diario</small><input id="d" type="number" min="1" max="365" value="30"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Qué es cada tasa?</h2>
<ul>
<li><strong>TNA (tasa nominal anual):</strong> es la que publican los bancos. No considera que los intereses se reinvierten.</li>
<li><strong>TEA (tasa efectiva anual):</strong> lo que ganarías o pagarías en un año reinvirtiendo los intereses. Es la que sirve para comparar.</li>
<li><strong>TEM (tasa efectiva mensual):</strong> lo que ganás o pagás en un mes. Sirve para comparar con la inflación mensual.</li>
</ul>
<h3>Las fórmulas</h3>
<p><em>Tasa del período = TNA × días ÷ 365</em> · <em>TEA = (1 + tasa del período)<sup>365/días</sup> − 1</em></p>
<p>Por eso una cuenta que paga intereses todos los días tiene una TEA más alta que un plazo fijo a 30 días con la misma TNA.</p>
<p>¿Querés entenderlo mejor? Leé la guía <a href="../guias/tna-tea-cft/">TNA, TEA, TEM y CFT explicados</a>.</p>
</div>
''', faq=[
 ('¿Cómo paso de TNA a tasa mensual?', 'Para un plazo fijo a 30 días: tasa mensual = TNA × 30 ÷ 365. Una TNA del 30 % equivale a un 2,47 % mensual.'),
 ('¿Por qué la TEA es mayor que la TNA?', 'Porque supone que reinvertís los intereses y ganás intereses sobre los intereses (interés compuesto).'),
], script='''
conectar(() => {
  const t = val('t') / 100, tipo = $('#tipo').value, d = Math.max(1, Math.min(365, Math.round(val('d'))));
  let per;
  if (tipo === 'tna') per = t * d / 365;
  else if (tipo === 'tea') per = Math.pow(1 + t, d / 365) - 1;
  else per = Math.pow(1 + t, d / 30) - 1;
  const tna = per * 365 / d * 100, tea = (Math.pow(1 + per, 365 / d) - 1) * 100, tem = (Math.pow(1 + per, 30 / d) - 1) * 100, ted = (Math.pow(1 + per, 1 / d) - 1) * 100;
  $('#res').innerHTML = `<div class="label">Tasa efectiva anual (TEA)</div><div class="big">${pct(tea)}</div>` + filas([
    ['TNA', pct(tna)], ['TEM (mensual)', pct(tem)], ['Tasa diaria', num.format(ted.toFixed(4)) + ' %'], ['TEA', pct(tea), 'total'],
  ]);
});
''')

# ---------- COSTO DE UN VIAJE ----------
page('costo-viaje', 'Calculadora de costo de viaje en auto: nafta, peajes y por persona',
 'Calculá cuánto cuesta un viaje en auto: litros de nafta, gasto en combustible, peajes y cuánto pone cada uno si viajan varios.',
 nombre='Costo de un viaje en auto', body='''
<h1>¿Cuánto cuesta el viaje en auto?</h1>
<p class="lead">Calculá la nafta y los peajes de tu viaje, y cuánto le toca poner a cada uno.</p>
<div class="card calc">
<div class="row">
<label>Distancia (km) <small>solo ida</small><input id="km" type="number" inputmode="decimal" min="0" value="400"></label>
<label>Consumo del auto (litros cada 100 km)<input id="cons" type="number" inputmode="decimal" min="0" step="0.1" value="8"></label>
</div>
<div class="row">
<label>Precio del litro ($) <small>cargá el precio actual de tu estación</small><input id="litro" type="number" inputmode="decimal" min="0" value="1500"></label>
<label>Peajes y estacionamiento ($) <small>total del viaje</small><input id="peaje" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<div class="row">
<label>Personas que viajan<input id="pers" type="number" min="1" max="20" value="2"></label>
<label class="check" style="align-self:end"><input id="iv" type="checkbox" checked> Ida y vuelta</label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el gasto de nafta?</h2>
<p><em>Litros = km × consumo ÷ 100</em> y <em>gasto = litros × precio del litro</em>. Un auto que gasta 8 litros cada 100 km, en un viaje de 400 km, usa 32 litros.</p>
<h3>¿Cuánto consume mi auto?</h3>
<p>Los autos chicos suelen gastar entre 5 y 7 litros cada 100 km en ruta; los medianos, entre 6 y 9; las camionetas, 10 o más. En ciudad el consumo es mayor. Si tu auto te muestra "km por litro", dividí 100 por ese número: 12,5 km/l son 8 litros cada 100 km.</p>
<h3>Para gastar menos</h3>
<ul>
<li>Manejá a velocidad constante: en ruta, pasar de 110 a 130 km/h puede subir el consumo bastante.</li>
<li>Revisá la presión de las cubiertas y no lleves peso de más.</li>
<li>Usá el aire acondicionado con moderación.</li>
</ul>
</div>
''', faq=[
 ('¿Cómo paso de km por litro a litros cada 100 km?', 'Dividí 100 por los km por litro. Por ejemplo, 12,5 km/l equivalen a 8 litros cada 100 km.'),
 ('¿Cómo dividimos los gastos del viaje?', 'Lo más simple es sumar nafta y peajes y dividir por la cantidad de personas. Si además hubo otros gastos, usá la calculadora para dividir gastos.'),
], script='''
conectar(() => {
  const km = val('km') * ($('#iv').checked ? 2 : 1), cons = val('cons'), litro = val('litro'), peaje = val('peaje'), pers = Math.max(1, Math.round(val('pers')));
  const litros = km * cons / 100, nafta = litros * litro, total = nafta + peaje;
  $('#res').innerHTML = `<div class="label">Costo total del viaje</div><div class="big">${$$(total)}</div>` + filas([
    ['Kilómetros', num.format(km) + ' km'],
    ['Litros de combustible', num.format(litros) + ' l'],
    ['Combustible', $$(nafta)],
    ...(peaje ? [['Peajes y estacionamiento', $$(peaje)]] : []),
    ['Por persona (' + pers + ')', $$(total / pers), 'total'],
  ]);
});
''')

# ---------- DIVIDIR GASTOS ----------
page('dividir-gastos', 'Calculadora para dividir gastos entre amigos: quién le debe a quién',
 'Dividí los gastos de una salida, un asado o un viaje entre amigos: cargá cuánto puso cada uno y te decimos quién le tiene que transferir a quién.',
 nombre='Dividir gastos', body='''
<h1>Dividir gastos entre amigos</h1>
<p class="lead">Cargá cuánto puso cada uno y te decimos quién le tiene que pasar plata a quién, con la menor cantidad de transferencias.</p>
<div class="card calc">
<label>¿Quién puso cuánto? <small>una persona por línea: nombre y monto. Si alguien no puso nada, escribí 0</small><textarea id="lista" rows="6">Ana 24000
Bruno 6000
Caro 0
Diego 12000</textarea></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo funciona?</h2>
<ol>
<li>Se suma todo lo que se gastó y se divide por la cantidad de personas.</li>
<li>Cada uno compara lo que puso con lo que le toca: si puso de más, tiene que recibir; si puso de menos, tiene que pagar.</li>
<li>Se arman las transferencias para que cada uno quede saldado, con la menor cantidad de movimientos posible.</li>
</ol>
<p>Sirve para asados, cumpleaños, viajes, regalos en grupo o los gastos de una casa compartida.</p>
<h3>Si alguien gasta más de una vez</h3>
<p>Sumá todo lo que puso esa persona y escribí el total en su línea. Si una misma persona aparece dos veces, la calculadora suma sus montos.</p>
</div>
''', faq=[
 ('¿Cómo se divide un gasto en partes iguales?', 'Se suma el total y se divide por la cantidad de personas. Después, cada uno paga o recibe la diferencia entre lo que le toca y lo que puso.'),
 ('¿Puedo poner montos con centavos?', 'Sí. Escribilos con coma o con punto, por ejemplo: Ana 1500,50.'),
], script='''
conectar(() => {
  const gente = {};
  String($('#lista').value).split('\\n').forEach(l => {
    const m = l.trim().match(/^(.*?)[\\s:=-]+\\$?\\s*([\\d.,]+)$/) || l.trim().match(/^(.+)$/);
    if (!m || !m[1].trim()) return;
    const nombre = m[1].trim(), monto = m[2] ? parseFloat(m[2].replace(/\\.(?=\\d{3}(\\D|$))/g, '').replace(',', '.')) || 0 : 0;
    gente[nombre] = (gente[nombre] || 0) + monto;
  });
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const nombres = Object.keys(gente);
  if (nombres.length < 2) { $('#res').innerHTML = 'Cargá al menos dos personas.'; return; }
  const total = nombres.reduce((s, n) => s + gente[n], 0), parte = total / nombres.length;
  const saldo = nombres.map(n => ({ n, s: gente[n] - parte }));
  const deudores = saldo.filter(x => x.s < -0.005).sort((a, b) => a.s - b.s), acreedores = saldo.filter(x => x.s > 0.005).sort((a, b) => b.s - a.s);
  const pagos = []; let i = 0, j = 0;
  while (i < deudores.length && j < acreedores.length) {
    const m = Math.min(-deudores[i].s, acreedores[j].s);
    pagos.push(`<li><strong>${esc(deudores[i].n)}</strong> le pasa <strong>${$$(m)}</strong> a <strong>${esc(acreedores[j].n)}</strong></li>`);
    deudores[i].s += m; acreedores[j].s -= m;
    if (Math.abs(deudores[i].s) < 0.005) i++; if (Math.abs(acreedores[j].s) < 0.005) j++;
  }
  $('#res').innerHTML = `<div class="label">A cada uno le toca</div><div class="big">${$$(parte)}</div>` + filas([
    ['Total gastado', $$(total)], ['Personas', nombres.length]]) +
    (pagos.length ? '<h3>Transferencias</h3><ul class="split-out">' + pagos.join('') + '</ul>' : '<p class="note">Están todos a mano.</p>');
});
''')

# ---------- HORAS TRABAJADAS ----------
page('horas-trabajadas', 'Calculadora de horas trabajadas: sumá entradas y salidas',
 'Sumá las horas trabajadas en la semana o el mes a partir de los horarios de entrada y salida, descontando el descanso, y calculá cuánto cobrás por hora.',
 nombre='Horas trabajadas', body='''
<h1>Calculadora de horas trabajadas</h1>
<p class="lead">Cargá tus horarios de entrada y salida y te decimos cuántas horas trabajaste en total.</p>
<div class="card calc">
<label>Horarios <small>un día por línea, con el formato entrada-salida. Ejemplo: 9:00-18:30</small><textarea id="lista" rows="6">9:00-18:00
9:00-18:30
8:30-17:00
9:00-18:00
9:00-14:00</textarea></label>
<div class="row">
<label>Descanso por día (minutos)<input id="desc" type="number" min="0" value="60"></label>
<label>Valor de la hora ($) <small>opcional</small><input id="vh" type="number" inputmode="decimal" min="0" value="0"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se suman las horas?</h2>
<p>Las horas no se suman como números comunes, porque una hora tiene 60 minutos y no 100. Por eso conviene pasar todo a minutos, sumar y volver a pasar a horas. Por ejemplo, de 9:00 a 18:30 son 9 h 30 min; si descontás 1 hora de almuerzo, quedan 8 h 30 min, que en decimal son <strong>8,5 horas</strong>.</p>
<h3>Turnos de noche</h3>
<p>Si salís después de la medianoche (por ejemplo, 22:00-6:00), la calculadora lo detecta y cuenta las horas correctamente.</p>
<h3>¿Y si me pasé de la jornada?</h3>
<p>Si trabajaste más horas que tu jornada legal o de convenio, te corresponden horas extra. Calculalas con la <a href="../horas-extra/">calculadora de horas extra</a>.</p>
</div>
''', faq=[
 ('¿Cómo paso minutos a horas decimales?', 'Dividí los minutos por 60. Por ejemplo, 45 minutos son 0,75 horas; 8 h 45 min son 8,75 horas.'),
 ('¿Cuál es la jornada máxima legal en Argentina?', 'La Ley de Jornada de Trabajo fija 8 horas diarias o 48 semanales, con excepciones según la actividad y el convenio.'),
], script='''
conectar(() => {
  const desc = Math.max(0, val('desc')), vh = val('vh');
  let tot = 0, dias = 0, malas = 0;
  String($('#lista').value).split('\\n').forEach(l => {
    const m = l.trim().match(/^(\\d{1,2})[:.,h]?(\\d{2})?\\s*(?:-|a|–|hasta)\\s*(\\d{1,2})[:.,h]?(\\d{2})?$/i);
    if (!l.trim()) return;
    if (!m) { malas++; return; }
    const a = (+m[1]) * 60 + (+(m[2] || 0)), b0 = (+m[3]) * 60 + (+(m[4] || 0));
    let b = b0 <= a ? b0 + 1440 : b0;
    tot += Math.max(0, b - a - desc); dias++;
  });
  const h = Math.floor(tot / 60), mi = Math.round(tot % 60);
  $('#res').innerHTML = `<div class="label">Total trabajado</div><div class="big">${h} h ${String(mi).padStart(2, '0')} min</div>` + filas([
    ['Días', dias], ['En horas decimales', num.format(tot / 60) + ' h'], ['Promedio por día', dias ? num.format(tot / 60 / dias) + ' h' : '—'],
    ...(vh ? [['A cobrar (' + $$(vh) + ' por hora)', $$(tot / 60 * vh), 'total']] : []),
  ]) + (malas ? `<p class="note warn">No entendimos ${malas} ${malas === 1 ? 'línea' : 'líneas'}. Usá el formato 9:00-18:00.</p>` : '');
});
''')

# ---------- REGLA DE TRES ----------
page('regla-de-tres', 'Regla de 3 simple: calculadora online directa e inversa',
 'Resolvé una regla de tres simple directa o inversa al instante, con la explicación paso a paso y ejemplos de la vida diaria.',
 nombre='Regla de tres', body='''
<h1>Calculadora de regla de 3 simple</h1>
<p class="lead">Si A es a B, ¿cuánto es C? Resolvelo al instante, directa o inversa.</p>
<div class="card calc">
<label>Tipo<select id="tipo"><option value="d">Directa (si uno sube, el otro sube)</option><option value="i">Inversa (si uno sube, el otro baja)</option></select></label>
<div class="row">
<label>Si A<input id="a" type="number" inputmode="decimal" step="any" value="3"></label>
<label>… es a B<input id="b" type="number" inputmode="decimal" step="any" value="1500"></label>
</div>
<label>Entonces C es a…<input id="c" type="number" inputmode="decimal" step="any" value="5"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>Regla de tres directa</h2>
<p>Se usa cuando las dos cantidades aumentan juntas. Ejemplo: si 3 kg de pan cuestan $1.500, ¿cuánto cuestan 5 kg? <em>X = 5 × 1.500 ÷ 3 = $2.500</em>.</p>
<h2>Regla de tres inversa</h2>
<p>Se usa cuando una cantidad sube y la otra baja. Ejemplo: si 3 personas pintan una casa en 10 días, ¿cuánto tardan 5 personas? <em>X = 3 × 10 ÷ 5 = 6 días</em>.</p>
<h3>¿Cómo sé cuál usar?</h3>
<p>Preguntate: si una cantidad se duplica, ¿la otra también se duplica (directa) o se reduce a la mitad (inversa)?</p>
</div>
''', faq=[
 ('¿Cómo se hace una regla de 3 simple?', 'Si A es a B, entonces C es a X. En la directa, X = C × B ÷ A. Por ejemplo: si 3 kg cuestan $1.500, 5 kg cuestan 5 × 1.500 ÷ 3 = $2.500.'),
 ('¿Cuál es la fórmula de la regla de tres simple?', 'Directa: X = C × B ÷ A. Inversa: X = A × B ÷ C.'),
 ('¿Sirve para calcular porcentajes?', 'Sí: si 100 es a 80.000, el 15 es a X = 15 × 80.000 ÷ 100 = 12.000. También podés usar la calculadora de porcentajes.'),
], script='''
conectar(() => {
  const a = val('a'), b = val('b'), c = val('c'), inv = $('#tipo').value === 'i';
  if (inv ? !c : !a) { $('#res').innerHTML = 'No se puede dividir por cero.'; return; }
  const x = inv ? a * b / c : c * b / a;
  $('#res').innerHTML = `<div class="label">Resultado</div><div class="big">${num.format(x)}</div><p class="note">${inv ? `X = ${num.format(a)} × ${num.format(b)} ÷ ${num.format(c)}` : `X = ${num.format(c)} × ${num.format(b)} ÷ ${num.format(a)}`}</p>`;
});
''')

page('guias/sueldo-bruto-y-neto', '¿Qué es el sueldo bruto y neto? Diferencia y cómo calcularlo',
 'Diferencia entre sueldo bruto y neto en Argentina: qué descuentos tiene el recibo de sueldo (jubilación, PAMI, obra social, sindicato, Ganancias) y cómo calcularlos.',
 nombre='Sueldo bruto y neto', articulo=True, relacionadas=_rel('sueldo-bruto-y-neto'), body='''
<h1>¿Qué es el sueldo bruto y el sueldo neto?</h1>
<div class="card" style="margin:0 0 20px"><p style="margin:0"><strong>En resumen:</strong> el <strong>sueldo bruto</strong> es el total antes de los descuentos y el <strong>sueldo neto</strong> es lo que cobrás en mano. La diferencia son los aportes: en relación de dependencia te descuentan un <strong>17 %</strong> del bruto (más la cuota sindical si estás afiliado). Con un bruto de $1.000.000, cobrás $830.000 de neto.</p></div>
<p class="lead">Por qué cobrás menos de lo que dice tu contrato, y cómo leer cada línea del recibo de sueldo.</p>
<h2>Bruto, neto y "de bolsillo"</h2>
<ul>
<li><strong>Sueldo bruto:</strong> es el total que te asigna el empleador antes de los descuentos. Es la cifra que se usa en las ofertas de trabajo y en los convenios.</li>
<li><strong>Sueldo neto:</strong> es lo que efectivamente te depositan, después de los descuentos. También se lo llama "de bolsillo" o "en mano".</li>
</ul>
<h2>Los descuentos del recibo</h2>
<table class="detail big-table"><tr><th>Concepto</th><th>Porcentaje</th><th>Para qué es</th></tr>
<tr><td>Jubilación (SIPA)</td><td>11 %</td><td>Tu futura jubilación</td></tr>
<tr><td>Ley 19.032 (PAMI)</td><td>3 %</td><td>La obra social de los jubilados</td></tr>
<tr><td>Obra social</td><td>3 %</td><td>Tu cobertura de salud</td></tr>
<tr><td>Cuota sindical</td><td>2 % a 3 %</td><td>Solo si estás afiliado al sindicato</td></tr>
<tr><td>Impuesto a las ganancias</td><td>Variable</td><td>Solo para sueldos altos</td></tr></table>
<p>En total, sin sindicato ni Ganancias, te descuentan el <strong>17 %</strong>. Con un bruto de $1.000.000, cobrás $830.000.</p>
<h2>Conceptos remunerativos y no remunerativos</h2>
<p>En el recibo vas a ver dos tipos de montos. Los <strong>remunerativos</strong> (básico, antigüedad, presentismo, horas extra) llevan descuentos y cuentan para el aguinaldo y la indemnización. Los <strong>no remunerativos</strong> (algunas sumas fijas acordadas en paritarias) no llevan aportes jubilatorios, aunque a veces sí aporte a la obra social.</p>
<h2>Lo que paga el empleador</h2>
<p>Además de tu bruto, el empleador paga <strong>contribuciones patronales</strong> (jubilación, obra social, ART, etc.). No salen de tu sueldo, por eso no las ves descontadas, pero hacen que tu costo para la empresa sea mayor que tu bruto.</p>
<p>Calculá tu caso con la <a href="../../sueldo-neto/">calculadora de sueldo neto</a> o, al revés, con la de <a href="../../sueldo-bruto/">sueldo bruto desde el neto</a>.</p>
''', faq=[
 ('¿Cuál es la diferencia entre sueldo bruto y neto?', 'El bruto es el sueldo antes de los descuentos y el neto es lo que te depositan. La diferencia son los aportes obligatorios (17 %) y, si corresponde, la cuota sindical y el impuesto a las ganancias.'),
 ('¿Cómo paso de bruto a neto?', 'Multiplicá el bruto por 0,83 (si no estás afiliado a un sindicato). Para pasar de neto a bruto, dividí el neto por 0,83.'),
 ('¿Cuánto me descuentan del sueldo en Argentina?', 'En relación de dependencia, el 17 % del bruto (11 % jubilación, 3 % PAMI y 3 % obra social), más la cuota sindical si estás afiliado y Ganancias si corresponde.'),
 ('¿El sueldo que me ofrecen en una entrevista es bruto o neto?', 'Casi siempre es bruto. Para saber cuánto vas a cobrar, restale el 17 %.'),
])

page('guias/tna-tea-cft', '¿Qué significa TNA, TEA, TEM y CFT? Explicación simple con ejemplos',
 'Qué es la TNA, la TEA, la TEM y el CFT, cómo se calculan y cuál mirar para comparar plazos fijos, billeteras virtuales, préstamos y tarjetas en Argentina.',
 nombre='TNA, TEA, TEM y CFT', articulo=True, relacionadas=_rel('tna-tea-cft'), body='''
<h1>¿Qué significa TNA, TEA, TEM y CFT?</h1>
<div class="card" style="margin:0 0 20px"><p style="margin:0"><strong>En resumen:</strong> <strong>TNA</strong> es la tasa nominal anual (la que publica el banco), <strong>TEA</strong> es la tasa efectiva anual (lo que ganás en un año reinvirtiendo los intereses), <strong>TEM</strong> es la tasa efectiva mensual (lo que ganás en un mes) y <strong>CFT</strong> es el costo financiero total de un préstamo, con intereses, IVA, seguros y comisiones.</p></div>
<p class="lead">Las siglas que aparecen en cada plazo fijo, préstamo o billetera virtual, explicadas con ejemplos.</p>
<h2>TNA: tasa nominal anual</h2>
<p>Es la tasa que publican bancos y billeteras. Indica cuánto pagan o cobran en un año <strong>sin reinvertir los intereses</strong>. Sirve para calcular los intereses de un período: un plazo fijo de $1.000.000 a 30 días con una TNA del 30 % paga $1.000.000 × 0,30 × 30 ÷ 365 = <strong>$24.658</strong>.</p>
<h2>TEM: tasa efectiva mensual</h2>
<p>Es lo que ganás o pagás en un mes. Con una TNA del 30 % a 30 días, la TEM es del <strong>2,47 %</strong>. Es la mejor tasa para comparar con la <strong>inflación mensual</strong>: si la TEM es menor, perdés poder de compra.</p>
<h2>TEA: tasa efectiva anual</h2>
<p>Muestra lo que ganarías en un año si <strong>reinvertís los intereses</strong> cada vez. Con la misma TNA del 30 %, renovando mes a mes, la TEA es del <strong>34,5 %</strong>. Cuanto más seguido se capitalizan los intereses (por ejemplo, a diario en una cuenta remunerada), más alta es la TEA.</p>
<h2>CFT: costo financiero total</h2>
<p>Es la tasa que importa cuando <strong>pedís plata prestada</strong>. Incluye los intereses y también el IVA, los seguros y las comisiones. Por ley, bancos y financieras tienen que informarlo, y en letra más grande que la TNA. Para comparar préstamos o financiaciones con tarjeta, <strong>mirá siempre el CFT</strong>.</p>
<h2>¿Cuál uso para qué?</h2>
<ul>
<li><strong>Para comparar inversiones:</strong> la TEA (o la TEM si comparás con la inflación).</li>
<li><strong>Para comparar préstamos:</strong> el CFT.</li>
<li><strong>Para calcular los intereses de un plazo fijo:</strong> la TNA.</li>
</ul>
<p>Convertí una tasa en otra con el <a href="../../tasas/">conversor de tasas</a>.</p>
''', faq=[
 ('¿Qué significa TNA?', 'Tasa Nominal Anual. Es la tasa de interés anual que informan los bancos, sin considerar la reinversión de los intereses. Sirve para calcular los intereses de un período: monto × TNA × días ÷ 365.'),
 ('¿Qué significa TEM?', 'Tasa Efectiva Mensual. Es lo que ganás o pagás en un mes. Con un plazo fijo a 30 días se calcula como TNA × 30 ÷ 365; es la mejor tasa para comparar con la inflación mensual.'),
 ('¿Qué significa TEA?', 'Tasa Efectiva Anual. Es lo que ganarías en un año si reinvertís los intereses cada vez. Siempre es mayor que la TNA.'),
 ('¿Qué es mejor, una TNA o una TEA alta?', 'Para comparar entre opciones de inversión usá la TEA, porque incluye la reinversión de intereses. Dos productos con la misma TNA pueden tener TEA distintas.'),
 ('¿Qué es el CFTEA?', 'Es el costo financiero total expresado como tasa efectiva anual. Es el número más completo para comparar el costo de un préstamo.'),
])

page('guias/vacaciones-cuantos-dias', 'Vacaciones: cuántos días te corresponden según la ley',
 'Cuántos días de vacaciones corresponden por antigüedad en Argentina, cuándo se toman, con cuánta anticipación te tienen que avisar y cómo se pagan.',
 nombre='Vacaciones: cuántos días', articulo=True, relacionadas=_rel('vacaciones-cuantos-dias'), body='''
<h1>Vacaciones: cuántos días te corresponden</h1>
<p class="lead">Lo que dice la Ley de Contrato de Trabajo sobre las vacaciones pagas, explicado en simple.</p>
<h2>Días según la antigüedad</h2>
<table class="detail big-table"><tr><th>Antigüedad al 31 de diciembre</th><th>Días corridos</th></tr>
<tr><td>Menos de 5 años</td><td>14 días</td></tr>
<tr><td>De 5 a 10 años</td><td>21 días</td></tr>
<tr><td>De 10 a 20 años</td><td>28 días</td></tr>
<tr><td>Más de 20 años</td><td>35 días</td></tr></table>
<p>Son <strong>días corridos</strong>: incluyen sábados, domingos y feriados. Tu convenio colectivo puede darte más días; nunca menos.</p>
<h2>Si entraste hace poco</h2>
<p>Para tener las vacaciones completas tenés que haber trabajado, como mínimo, la <strong>mitad de los días hábiles</strong> del año. Si no llegás, te corresponde <strong>1 día de vacaciones cada 20 días trabajados</strong>.</p>
<h2>¿Cuándo se toman?</h2>
<ul>
<li>En general se otorgan entre el <strong>1 de octubre y el 30 de abril</strong>. De común acuerdo, se pueden tomar en otro momento del año.</li>
<li>Te tienen que avisar la fecha con al menos <strong>30 días de anticipación</strong>, por escrito (antes eran 45; lo cambió la Ley 27.802 de 2026).</li>
<li>Se pueden <strong>fraccionar</strong> de común acuerdo, en tramos de al menos 7 días.</li>
<li>Si la empresa organiza las vacaciones por turnos, al menos una vez cada 3 años te tienen que tocar en verano.</li>
<li>Tienen que empezar un lunes, o el día hábil siguiente si ese lunes es feriado.</li>
</ul>
<h2>¿Cómo se pagan?</h2>
<p>Se pagan <strong>antes de empezar</strong> a tomarlas. Para los mensualizados, cada día vale el sueldo dividido 25 (no por 30): esa diferencia es el <strong>plus vacacional</strong>. Las vacaciones no se pueden cambiar por dinero, salvo cuando termina la relación laboral y quedaron días sin tomar.</p>
<p>Calculá tus días y el pago con la <a href="../../vacaciones/">calculadora de vacaciones</a>.</p>
''', faq=[
 ('¿Me pueden dar las vacaciones en invierno?', 'El período general es del 1 de octubre al 30 de abril, pero desde la reforma de 2026 se pueden tomar en otro momento si hay acuerdo entre vos y el empleador.'),
 ('¿Puedo fraccionar las vacaciones?', 'Sí: desde la Ley 27.802 de 2026, de común acuerdo se pueden dividir en tramos de al menos 7 días corridos.'),
])

page('guias/recategorizacion-monotributo', 'Recategorización del monotributo: cuándo y cómo hacerla',
 'Cuándo hay que recategorizarse en el monotributo, qué parámetros se miran, cómo se hace en el sitio de ARCA y qué pasa si no lo hacés.',
 nombre='Recategorización del monotributo', articulo=True, relacionadas=_rel('recategorizacion-monotributo'), body='''
<h1>Recategorización del monotributo</h1>
<p class="lead">Dos veces por año tenés que revisar si seguís en la categoría correcta. Te explicamos cómo.</p>
<h2>¿Cuándo hay que recategorizarse?</h2>
<p>La recategorización es <strong>semestral</strong>: se hace en <strong>enero</strong> (mirando los últimos 12 meses hasta diciembre) y en <strong>julio</strong> (los 12 meses hasta junio). ARCA informa cada vez la fecha límite exacta, que suele caer en los primeros días de febrero y de agosto, cuando también se actualizan los valores de las categorías.</p>
<h2>¿Qué se mira?</h2>
<ul>
<li>Los <strong>ingresos brutos</strong> (lo que facturaste) en los últimos 12 meses.</li>
<li>La <strong>superficie</strong> del local, si tenés.</li>
<li>La <strong>energía eléctrica</strong> consumida en el local.</li>
<li>Los <strong>alquileres</strong> que pagás por el local.</li>
</ul>
<p>Te corresponde la categoría más alta que resulte de cualquiera de esos parámetros.</p>
<h2>Paso a paso</h2>
<ol>
<li>Sumá lo que facturaste en los últimos 12 meses. Podés verlo en "Mis comprobantes" de ARCA.</li>
<li>Fijate en la tabla cuál es tu categoría. Lo podés hacer con la <a href="../../monotributo/">calculadora de monotributo</a>.</li>
<li>Entrá al <strong>Portal Monotributo</strong> de ARCA con tu clave fiscal y elegí <strong>Recategorizarme</strong>.</li>
<li>Completá los datos y confirmá. Si tu categoría no cambió, no hace falta hacer nada.</li>
</ol>
<h2>¿Qué pasa si no me recategorizo?</h2>
<p>Si te correspondía subir y no lo hiciste, ARCA puede <strong>recategorizarte de oficio</strong> y cobrarte la diferencia con intereses y una multa. Si superás el tope de la categoría más alta, quedás excluido del monotributo y pasás al régimen general.</p>
<p class="note">Esta guía es orientativa. Para tu caso puntual, consultá con un contador.</p>
''', faq=[
 ('¿Qué pasa si facturé menos?', 'Podés recategorizarte a una categoría más baja y pagar una cuota menor. No es obligatorio, pero te conviene.'),
 ('¿Cuántas veces al año me recategorizo?', 'Dos: en enero y en julio, mirando lo facturado en los últimos 12 meses.'),
])

# ---------- JUBILACIÓN ----------
# Valores de ANSES de noviembre 2026 (movilidad 1,93 %, Res. ANSES 304/2026; bono Decreto 1296/2026). Actualizar todos los meses.
JUB = {'mes': 'noviembre de 2026', 'minimo': 444158.46, 'maximo': 2988765.82, 'bono': 70000, 'aumento': 1.93}
page('jubilacion', 'Calculadora de jubilación: haber, bono de ANSES y aguinaldo (noviembre 2026)',
 'Calculá cuánto cobra un jubilado de ANSES con el bono de $70.000, el aumento por movilidad y el medio aguinaldo de diciembre. Valores de noviembre de 2026.',
 nombre='Jubilación, bono y aguinaldo', body=f'''
<h1>Calculadora de jubilación, bono y aguinaldo</h1>
<p class="lead">Poné tu haber de ANSES y te decimos cuánto te corresponde de bono, cuánto cobrás en total y cuánto vas a cobrar de aguinaldo.</p>
<div class="card calc">
<label>Haber bruto mensual ($) <small>lo que figura en tu recibo, sin el bono</small><input id="haber" type="number" inputmode="decimal" min="0" value="{JUB['minimo']}"></label>
<label>Aumento del mes próximo (%) <small>opcional, cuando ANSES lo anuncie</small><input id="aum" type="number" inputmode="decimal" step="0.01" value="0"></label>
<div id="res" class="result"></div>
<p class="note">Valores de {JUB['mes']}: haber mínimo $ 444.158,46, haber máximo $ 2.988.765,82 y bono de hasta $ 70.000. Confirmá los montos en ANSES.</p>
</div>
<div class="article">
<h2>¿Cómo se calcula el bono para jubilados?</h2>
<p>Quienes cobran la <strong>jubilación mínima o menos</strong> reciben el bono completo de $70.000. Quienes cobran un poco más reciben un bono <strong>proporcional</strong>, para que nadie quede por debajo de la mínima más el bono: en {JUB['mes']}, $ 514.158,46. Si tu haber supera ese monto, no cobrás bono.</p>
<h2>¿Cómo aumentan las jubilaciones?</h2>
<p>Desde 2024, los haberes se actualizan <strong>todos los meses según la inflación</strong> (IPC del INDEC), con dos meses de desfase. Por ejemplo, el aumento de noviembre de 2026 ({str(JUB['aumento']).replace('.', ',')} %) corresponde a la inflación de septiembre.</p>
<h2>Aguinaldo de jubilados</h2>
<p>El medio aguinaldo equivale al <strong>50 % del haber más alto</strong> del semestre. Se paga junto con el haber de junio y el de diciembre. El bono <strong>no</strong> se tiene en cuenta para calcularlo.</p>
<h3>Descuentos</h3>
<p>ANSES descuenta del haber el aporte al PAMI y, si corresponde, otras retenciones. El bono no tiene descuentos. Esta calculadora muestra montos brutos.</p>
</div>
''', faq=[
 ('¿Cuánto cobra un jubilado de la mínima en noviembre de 2026?', 'El haber mínimo es de $444.158,46 y, con el bono de $70.000, el total es de $514.158,46.'),
 ('¿El bono de $70.000 se cobra con el aguinaldo?', 'El bono se paga aparte y no forma parte del cálculo del aguinaldo, que es el 50 % del mejor haber del semestre.'),
 ('¿Cuándo se cobra el aguinaldo de los jubilados?', 'Junto con el haber de diciembre, según el calendario de pagos de ANSES que va por terminación de DNI.'),
], script='''
const JUB = ''' + json.dumps(JUB) + ''';
conectar(() => {
  const haber = val('haber'), aum = val('aum') / 100;
  const bono = Math.max(0, Math.min(JUB.bono, JUB.minimo + JUB.bono - haber));
  const nuevo = haber * (1 + aum), sac = Math.max(haber, nuevo) / 2;
  $('#res').innerHTML = `<div class="label">Total a cobrar este mes</div><div class="big">${$$(haber + bono)}</div>` + filas([
    ['Haber', $$(haber)],
    ['Bono', bono > 0 ? '+ ' + $$(bono) : 'No corresponde'],
    ...(aum ? [['Haber con el aumento (' + pct(aum * 100) + ')', $$(nuevo)]] : []),
    ['Medio aguinaldo estimado', $$(sac), 'total'],
  ]) + (haber > JUB.maximo ? '<p class="note warn">El haber supera el máximo de ANSES. Revisá el monto.</p>' : '');
});
''')

# ---------- PLAZO FIJO UVA ----------
page('plazo-fijo-uva', 'Plazo fijo UVA: cómo se calcula y cuánto rinde (calculadora)',
 'Simulá un plazo fijo UVA: capital ajustado por inflación más la tasa adicional, y comparalo con un plazo fijo tradicional para ver cuál conviene.',
 nombre='Plazo fijo UVA', body='''
<h1>Calculadora de plazo fijo UVA</h1>
<p class="lead">Simulá cuánto ganás con un plazo fijo UVA, que ajusta por inflación, y comparalo con un plazo fijo tradicional.</p>
<div class="card calc">
<div class="row">
<label>Monto a invertir ($)<input id="cap" type="number" inputmode="decimal" min="0" value="1000000"></label>
<label>Plazo (días) <small>mínimo 90</small><input id="dias" type="number" min="90" max="1095" value="90"></label>
</div>
<div class="row">
<label>Inflación mensual esperada (%)<input id="inf" type="number" inputmode="decimal" step="0.1" value="2"></label>
<label>Tasa adicional UVA (TNA %) <small>la que ofrezca tu banco</small><input id="tnauva" type="number" inputmode="decimal" step="0.1" value="1"></label>
</div>
<label>TNA del plazo fijo tradicional (%) <small>para comparar</small><input id="tna" type="number" inputmode="decimal" step="0.1" value="30"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el plazo fijo UVA?</h2>
<ol>
<li>El día que lo constituís, tu capital se pasa a UVA: <em>UVA compradas = capital ÷ valor de la UVA ese día</em>.</li>
<li>Al vencimiento, esas UVA se pasan a pesos al valor de la UVA de ese día, que subió con la inflación.</li>
<li>Sobre ese monto ajustado, el banco suma la tasa adicional por los días del plazo.</li>
</ol>
<p>Por ejemplo, con $1.000.000, una inflación del 2 % mensual y 90 días, el capital ajustado queda en unos $1.061.000, y con 1 % de tasa adicional cobrás alrededor de $1.063.800.</p>
<h2>¿Cómo funciona el plazo fijo UVA?</h2>
<p>El capital se convierte a <strong>UVA</strong> (Unidad de Valor Adquisitivo), una unidad que publica el Banco Central y que sube todos los días siguiendo la inflación. Al vencimiento, tus UVA se vuelven a pasar a pesos al valor de ese día, y además el banco te paga una <strong>tasa adicional</strong> (en general baja, alrededor del 1 % anual).</p>
<p><em>Monto final ≈ capital × (UVA final ÷ UVA inicial) × (1 + tasa adicional × días ÷ 365)</em></p>
<h3>¿Cuándo conviene?</h3>
<ul>
<li><strong>Conviene el UVA</strong> si creés que la inflación de los próximos meses va a ser mayor que la tasa del plazo fijo tradicional.</li>
<li><strong>Conviene el tradicional</strong> si la tasa fija le gana a la inflación que esperás.</li>
</ul>
<p>El UVA te protege de una suba inesperada de la inflación; el tradicional te asegura un monto fijo en pesos.</p>
<h3>Cosas a tener en cuenta</h3>
<ul>
<li>El plazo mínimo es de <strong>90 días</strong>. Algunos bancos ofrecen UVA precancelables, que se pueden retirar antes a una tasa menor.</li>
<li>La UVA sigue a la inflación con <strong>cierto rezago</strong> (alrededor de un mes y medio), así que en los primeros meses refleja la inflación pasada.</li>
<li>Si la inflación fuera negativa, el banco garantiza que no cobrás menos de lo que invertiste.</li>
</ul>
</div>
''', faq=[
 ('¿Cómo se calcula el plazo fijo UVA?', 'Se pasa el capital a UVA al valor del día, al vencimiento se vuelven a pasar a pesos al nuevo valor de la UVA (que siguió a la inflación) y se suma la tasa adicional que paga el banco por los días del plazo.'),
 ('¿Qué es la UVA?', 'Es la Unidad de Valor Adquisitivo, que publica el BCRA y se actualiza a diario por el índice CER, que sigue a la inflación.'),
 ('¿Cuál es el plazo mínimo de un plazo fijo UVA?', 'El plazo mínimo es de 90 días. Algunos bancos ofrecen la opción precancelable, que permite retirar antes con una tasa menor.'),
], script='''
conectar(() => {
  const cap = val('cap'), dias = Math.max(90, Math.round(val('dias'))), inf = val('inf') / 100, tu = val('tnauva') / 100, tna = val('tna') / 100;
  const ajuste = Math.pow(1 + inf, dias / 30), capAj = cap * ajuste, intUva = capAj * tu * dias / 365;
  const uva = capAj + intUva, trad = cap * (1 + tna * dias / 365), dif = uva - trad;
  $('#res').innerHTML = `<div class="label">Cobrarías al vencimiento (estimado)</div><div class="big">${$$(uva)}</div>` + filas([
    ['Ajuste por inflación', '+ ' + $$(capAj - cap)],
    ['Interés adicional (' + pct(tu * 100) + ' TNA)', '+ ' + $$(intUva)],
    ['Ganancia total', $$(uva - cap), 'total'],
    ['Con plazo fijo tradicional (' + pct(tna * 100) + ' TNA)', $$(trad)],
  ]) + `<p class="note ${dif < 0 ? 'warn' : ''}">${dif >= 0 ? '✓ Con esa inflación conviene el UVA' : '⚠ Con esa inflación conviene el tradicional'}: diferencia de ${$$(Math.abs(dif))}.</p>`;
});
''')

# ---------- GUÍA: QUÉ HACER SI TE DESPIDEN ----------
page('guias/que-hacer-si-me-despiden', 'Qué hacer si te despiden: los pasos para cobrar todo',
 'Guía paso a paso si te despiden en Argentina: qué firmar y qué no, cuándo te tienen que pagar, el certificado de trabajo, el seguro de desempleo y a dónde reclamar.',
 nombre='Qué hacer si te despiden', articulo=True, relacionadas=_rel('que-hacer-si-me-despiden'), body='''
<h1>Qué hacer si te despiden</h1>
<p class="lead">Un despido es un mal momento, pero hay pasos concretos para que cobres todo lo que te corresponde.</p>
<h2>1. No firmes nada sin leerlo</h2>
<p>Nunca firmes una <strong>renuncia</strong> si te están despidiendo: si renunciás, perdés la indemnización. Si te dan un papel para firmar, podés poner "recibí copia" con la fecha, que solo prueba que te lo entregaron, no que estás de acuerdo.</p>
<h2>2. Pedí que el despido sea por escrito</h2>
<p>El despido tiene que comunicarse <strong>por escrito</strong> (carta documento o telegrama) e indicar si es con causa o sin causa. Si te lo dicen solo de palabra, podés intimar a tu empleador por <strong>telegrama laboral</strong>, que es gratuito para los trabajadores en el Correo Argentino.</p>
<h2>3. Calculá lo que te corresponde</h2>
<p>Si es sin causa, te corresponde la indemnización por antigüedad, el preaviso (si no te avisaron), la integración del mes, los días trabajados, el aguinaldo y las vacaciones proporcionales. Hacé la cuenta con la <a href="../../indemnizacion/">calculadora de indemnización</a> antes de ir a cobrar.</p>
<h2>4. La liquidación final</h2>
<p>Te la tienen que pagar dentro de los <strong>4 días hábiles</strong> desde el despido. Revisá el recibo rubro por rubro. Si no estás de acuerdo con los montos, podés cobrar y firmar "en disconformidad" o "a cuenta de mayor cantidad", para poder reclamar la diferencia después.</p>
<h2>5. El certificado de trabajo</h2>
<p>El empleador te tiene que entregar el <strong>certificado de trabajo</strong> (art. 80 de la LCT), con tus fechas, tareas, sueldos y aportes. Lo vas a necesitar para el seguro de desempleo y para tu próximo trabajo.</p>
<h2>6. Pedí el seguro de desempleo</h2>
<p>Si te despidieron sin causa y tenés suficientes meses de aportes, podés pedir la <strong>prestación por desempleo</strong> en ANSES. Hay un plazo para hacerlo desde el despido, así que no lo dejes para último momento.</p>
<h2>7. Si no te pagan o te pagan menos</h2>
<p>Podés reclamar en el <strong>Ministerio de Trabajo</strong> de tu jurisdicción o, en la Ciudad de Buenos Aires, en el <strong>SECLO</strong> (conciliación obligatoria antes de un juicio). Un abogado laboralista te puede asesorar; muchos cobran solo si ganás, y los colegios de abogados suelen tener consultorios gratuitos.</p>
<p class="warn">Esta guía es orientativa y no reemplaza el asesoramiento de un abogado laboralista.</p>
''', faq=[
 ('¿Me pueden despedir sin pagarme nada?', 'Solo si el despido es con justa causa y la causa está probada, o durante el período de prueba (en ese caso igual cobrás días trabajados, aguinaldo y vacaciones proporcionales). Si discutís la causa, se puede reclamar.'),
 ('¿Tengo que firmar el recibo de la liquidación final?', 'Podés firmarlo para cobrar, pero si no estás de acuerdo con los montos escribí "en disconformidad" o "a cuenta de mayor cantidad" antes de tu firma.'),
])

# ---------- GUÍA: LICENCIAS ----------
page('guias/licencias-por-ley', 'Licencias laborales por ley en Argentina: cuántos días te corresponden',
 'Licencias especiales de la Ley de Contrato de Trabajo: matrimonio, nacimiento, fallecimiento de un familiar, exámenes, maternidad, enfermedad y vacaciones. Cuántos días son y cómo se pagan.',
 nombre='Licencias por ley', articulo=True, relacionadas=_rel('licencias-por-ley'), body='''
<h1>Licencias laborales por ley</h1>
<p class="lead">Cuántos días te corresponden por casamiento, nacimiento de un hijo, exámenes, enfermedad y otras situaciones.</p>
<h2>Licencias especiales (art. 158 de la LCT)</h2>
<table class="detail big-table"><tr><th>Motivo</th><th>Días</th></tr>
<tr><td>Nacimiento de un hijo (otro progenitor)</td><td>2 días corridos</td></tr>
<tr><td>Matrimonio</td><td>10 días corridos</td></tr>
<tr><td>Fallecimiento del cónyuge o conviviente, hijos o padres</td><td>3 días corridos</td></tr>
<tr><td>Fallecimiento de un hermano</td><td>1 día</td></tr>
<tr><td>Examen en la secundaria o la universidad</td><td>2 días corridos por examen, hasta 10 por año</td></tr></table>
<p>Son <strong>licencias pagas</strong>: cobrás el sueldo normal. Muchos convenios colectivos dan más días; revisá el tuyo. Para las licencias por examen, la ley exige presentar el comprobante de que rendiste.</p>
<h2>Licencia por maternidad</h2>
<p>Son <strong>90 días</strong>: en general 45 antes y 45 después del parto, aunque se puede pedir tomar 30 antes y 60 después. Durante la licencia no cobrás sueldo del empleador sino una <strong>asignación de ANSES</strong> equivalente.</p>
<h2>Enfermedad o accidente inculpable</h2>
<p>Si te enfermás o te accidentás fuera del trabajo, seguís cobrando tu sueldo durante:</p>
<ul>
<li><strong>3 meses</strong> por año si tenés menos de 5 años de antigüedad.</li>
<li><strong>6 meses</strong> si tenés 5 años o más.</li>
<li>El doble (<strong>6 y 12 meses</strong>) si tenés cargas de familia.</li>
</ul>
<p>Tenés que avisarle al empleador y presentar el certificado médico. Si el accidente o la enfermedad es por el trabajo, lo cubre la ART.</p>
<h2>Vacaciones</h2>
<p>Entre 14 y 35 días corridos por año según tu antigüedad. Mirá la guía de <a href="../vacaciones-cuantos-dias/">vacaciones</a>.</p>
<p class="note">Guía orientativa basada en la Ley de Contrato de Trabajo. La reforma laboral de 2026 (Ley 27.802) cambió otros puntos, como las vacaciones; revisá tu convenio colectivo y, ante dudas, consultá en el Ministerio de Trabajo.</p>
''', faq=[
 ('¿Cuántos días de licencia tengo por casamiento?', 'La Ley de Contrato de Trabajo da 10 días corridos de licencia paga por matrimonio. Algunos convenios dan más.'),
 ('¿Cuántos días de licencia por paternidad hay en Argentina?', 'La ley general da 2 días corridos por nacimiento de un hijo. Muchos convenios y empresas otorgan más.'),
])

# ---------- GUÍA: CÓMO PEDIR UN AUMENTO ----------
page('guias/como-pedir-un-aumento', 'Cómo pedir un aumento de sueldo: cuándo, cuánto y cómo',
 'Consejos prácticos para pedir un aumento de sueldo en Argentina: cómo calcular cuánto perdiste con la inflación, qué porcentaje pedir, cuándo hacerlo y qué decir.',
 nombre='Cómo pedir un aumento', articulo=True, relacionadas=_rel('como-pedir-un-aumento'), body='''
<h1>Cómo pedir un aumento de sueldo</h1>
<p class="lead">Con inflación, pedir un aumento no es un capricho: es mantener lo que ganás. Así podés prepararte para que salga bien.</p>
<h2>1. Hacé la cuenta: ¿cuánto perdiste?</h2>
<p>Compará tu último aumento con la inflación desde ese momento. Si en el último año tu sueldo subió 15 % y la inflación fue 25 %, perdiste alrededor de un <strong>8 % de poder de compra</strong>. Calculalo con la <a href="../../inflacion/">calculadora de inflación</a>, que te dice si tu sueldo le ganó o perdió.</p>
<h2>2. Averiguá cuánto se paga en el mercado</h2>
<p>Mirá avisos de empleo para tu puesto, encuestas salariales y la escala de tu convenio colectivo. Si sabés que el mercado paga más, tenés un argumento concreto.</p>
<h2>3. Juntá tus logros</h2>
<p>Anotá qué resultados lograste: proyectos que terminaste, clientes, ahorros que generaste, tareas nuevas que tomaste. Con números, mejor. El argumento más fuerte es "esto es lo que aporto", no "lo necesito".</p>
<h2>4. Elegí el momento</h2>
<ul>
<li>Después de un buen resultado o de terminar un proyecto.</li>
<li>Antes de que se definan los presupuestos del año (en muchas empresas, hacia fin de año).</li>
<li>En una reunión pedida para eso, no en un pasillo.</li>
</ul>
<h2>5. Pedí una cifra concreta</h2>
<p>Llevá un número, no un "lo que puedan". Hablá siempre de <strong>sueldo bruto</strong>: si sabés cuánto querés en mano, pasalo a bruto con la <a href="../../sueldo-bruto/">calculadora de bruto desde el neto</a>. Pedí un poco más de lo que esperás para tener margen.</p>
<h2>6. Si te dicen que no</h2>
<p>Preguntá qué tendrías que lograr para que sea posible y cuándo lo pueden revisar. Pedí que quede por escrito. Si no hay respuesta, puede ser una señal para buscar otras opciones.</p>
''', faq=[
 ('¿Cuánto aumento tengo que pedir?', 'Como mínimo, lo que te haga recuperar la inflación desde tu último aumento. Si además asumiste más responsabilidades o el mercado paga más, sumalo como argumento.'),
 ('¿Cada cuánto se puede pedir un aumento?', 'No hay una regla, pero con inflación es razonable revisarlo al menos una o dos veces por año, además de los aumentos de convenio.'),
])

# ---------- SUELDO POR HORA ----------
page('sueldo-por-hora', 'Calculadora de sueldo por hora: de mensual a hora y al revés',
 'Calculá cuánto ganás por hora, por día y por semana a partir de tu sueldo mensual, o cuánto cobrarías por mes con un valor hora.',
 nombre='Sueldo por hora', body='''
<h1>Calculadora de sueldo por hora</h1>
<p class="lead">Pasá tu sueldo mensual a valor hora, o al revés, para comparar trabajos o presupuestar.</p>
<div class="card calc">
<label>¿Qué tenés?<select id="modo"><option value="mes">Un sueldo mensual</option><option value="hora">Un valor por hora</option></select></label>
<div class="row">
<div data-modo="mes"><label>Sueldo mensual ($)<input id="mes" type="number" inputmode="decimal" min="0" value="1000000"></label></div>
<div data-modo="hora"><label>Valor por hora ($)<input id="hora" type="number" inputmode="decimal" min="0" value="6000"></label></div>
<label>Horas por semana<input id="hs" type="number" inputmode="decimal" min="1" max="100" value="45"></label>
</div>
<label>Días que trabajás por semana<input id="dias" type="number" min="1" max="7" value="5"></label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cómo se calcula el sueldo por hora?</h2>
<p>Un mes tiene en promedio <strong>4,33 semanas</strong> (52 semanas ÷ 12 meses). Entonces:</p>
<p><em>Valor hora = sueldo mensual ÷ (horas por semana × 4,33)</em></p>
<p>Con un sueldo de $1.000.000 y 45 horas semanales, trabajás unas 195 horas por mes: cada hora vale unos <strong>$5.128</strong>.</p>
<h3>Para comparar trabajos</h3>
<p>Dos sueldos iguales no valen lo mismo si uno pide 40 horas por semana y otro 48. Pasar todo a valor hora te muestra cuál paga mejor tu tiempo. Sumá también el tiempo de viaje si es muy distinto.</p>
<h3>Para freelancers</h3>
<p>Si trabajás por tu cuenta, al valor hora sumale lo que no cobrás cuando no trabajás (vacaciones, días sin clientes) y tus costos: monotributo, equipos, internet. Un valor hora "de empleado" suele quedarse corto.</p>
</div>
''', faq=[
 ('¿Cuántas horas tiene un mes de trabajo?', 'Depende de tu jornada: con 40 horas semanales son unas 173 horas por mes; con 45, unas 195; con 48, unas 208.'),
 ('¿El valor hora es bruto o neto?', 'Es el mismo tipo de monto que cargues: si ponés tu sueldo bruto, el valor hora es bruto; si ponés el neto, es neto.'),
], script='''
conectar(() => {
  modos('#modo');
  const hs = Math.max(1, val('hs')), dias = Math.max(1, Math.min(7, Math.round(val('dias')))), hm = hs * 52 / 12;
  const porMes = $('#modo').value === 'mes', mes = porMes ? val('mes') : val('hora') * hm, hora = mes / hm;
  $('#res').innerHTML = `<div class="label">${porMes ? 'Ganás por hora' : 'Ganarías por mes'}</div><div class="big">${$$(porMes ? hora : mes)}</div>` + filas([
    ['Horas por mes', num.format(hm) + ' h'],
    ['Por hora', $$(hora)],
    ['Por día (' + num.format(hs / dias) + ' h)', $$(hora * hs / dias)],
    ['Por semana', $$(hora * hs)],
    ['Por mes', $$(mes), 'total'],
    ['Por año (12 meses + aguinaldo)', $$(mes * 13)],
  ]);
});
''')

# ---------- CUENTA REMUNERADA ----------
page('cuenta-remunerada', 'Calculadora de cuenta remunerada: cuánto rinde tu plata por día',
 'Calculá cuánto te rinde la plata en una cuenta remunerada o billetera virtual (Mercado Pago, Ualá, Naranja X y otras) por día, por mes y por año según la TNA.',
 nombre='Cuenta remunerada', body='''
<h1>¿Cuánto rinde mi plata en una cuenta remunerada?</h1>
<p class="lead">Poné tu saldo y la tasa que te paga tu billetera o banco, y te decimos cuánto ganás por día, por mes y por año.</p>
<div class="card calc">
<div class="row">
<label>Saldo ($)<input id="saldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
<label>TNA (%) <small>la que muestra tu app</small><input id="tna" type="number" inputmode="decimal" step="0.1" min="0" value="28"></label>
</div>
<div class="row">
<label>Tope de saldo que remunera ($) <small>opcional, 0 = sin tope</small><input id="tope" type="number" inputmode="decimal" min="0" value="0"></label>
<label>Inflación mensual esperada (%) <small>opcional</small><input id="inf" type="number" inputmode="decimal" step="0.1" value="2"></label>
</div>
<div id="res" class="result"></div>
<p class="note">Las tasas de las billeteras cambian seguido: usá la que figura hoy en tu app.</p>
</div>
<div class="article">
<h2>¿Cómo funcionan las cuentas remuneradas?</h2>
<p>Las billeteras virtuales y algunos bancos pagan intereses <strong>todos los días</strong> por el saldo que dejás en la cuenta. Como los intereses de hoy se suman al saldo y mañana también rinden, la ganancia real es un poco mayor que la que indica la TNA.</p>
<p><em>Ganancia por día = saldo × TNA ÷ 365</em></p>
<h3>Ventajas</h3>
<ul>
<li>La plata está <strong>disponible siempre</strong>: la podés usar o transferir cuando quieras.</li>
<li>No hay plazo mínimo, como en el plazo fijo.</li>
</ul>
<h3>Cosas a tener en cuenta</h3>
<ul>
<li>Muchas billeteras tienen un <strong>tope de saldo</strong>: por encima, el dinero no rinde o rinde menos.</li>
<li>En las billeteras, en general la plata se invierte en un <strong>fondo común de inversión</strong> de bajo riesgo, que no tiene la garantía de depósitos de los bancos.</li>
<li>La tasa cambia casi todas las semanas.</li>
</ul>
<p>Si no vas a necesitar la plata por un tiempo, compará con un <a href="../plazo-fijo/">plazo fijo</a>.</p>
</div>
''', faq=[
 ('¿Cuánto rinde $1.000.000 en Mercado Pago?', 'Depende de la tasa del día. Con una TNA del 28 %, rinden unos $767 por día y unos $23.300 por mes. Cargá la tasa actual en la calculadora para ver el número exacto.'),
 ('¿Conviene más la cuenta remunerada o el plazo fijo?', 'El plazo fijo suele pagar una tasa algo más alta a cambio de inmovilizar la plata 30 días o más. La cuenta remunerada paga un poco menos pero te deja usar el dinero cuando quieras.'),
], script='''
conectar(() => {
  const saldo = val('saldo'), tna = val('tna') / 100, tope = val('tope'), inf = val('inf') / 100;
  const base = tope > 0 ? Math.min(saldo, tope) : saldo, d = tna / 365;
  const dia = base * d, mes = base * (Math.pow(1 + d, 30) - 1), anio = base * (Math.pow(1 + d, 365) - 1);
  const tem = (Math.pow(1 + d, 30) - 1) * 100, tea = (Math.pow(1 + d, 365) - 1) * 100;
  let comp = '';
  if (inf) { const r = ((1 + tem / 100) / (1 + inf) - 1) * 100; comp = `<p class="note ${r < 0 ? 'warn' : ''}">${r >= 0 ? '✓ Le gana a la inflación' : '⚠ Pierde contra la inflación'}: ${pct(r)} real por mes.</p>`; }
  $('#res').innerHTML = `<div class="label">Ganás por mes (30 días)</div><div class="big">${$$(mes)}</div>` + filas([
    ['Por día', $$(dia)],
    ['Por mes', $$(mes)],
    ['Por año (reinvirtiendo)', $$(anio), 'total'],
    ['Tasa mensual efectiva', pct(tem)],
    ['TEA', pct(tea)],
    ...(tope > 0 && saldo > tope ? [['Saldo que no rinde', $$(saldo - tope)]] : []),
  ]) + comp;
});
''')

# ---------- CRÉDITO HIPOTECARIO UVA ----------
page('credito-hipotecario-uva', 'Simulador de crédito hipotecario UVA: cuota e ingreso necesario',
 'Simulá un crédito hipotecario UVA: cuota inicial, cuánto tenés que ganar para que te lo den, cuánto sube la cuota con la inflación y el total a pagar.',
 nombre='Crédito hipotecario UVA', body='''
<h1>Simulador de crédito hipotecario UVA</h1>
<p class="lead">Calculá la cuota inicial de un crédito hipotecario UVA, el ingreso que te piden y cómo puede evolucionar la cuota.</p>
<div class="card calc">
<div class="row">
<label>Monto del crédito ($)<input id="monto" type="number" inputmode="decimal" min="0" value="80000000"></label>
<label>Plazo (años)<input id="anios" type="number" min="1" max="40" value="20"></label>
</div>
<div class="row">
<label>Tasa anual (TNA %) <small>la que ofrece el banco, sobre UVA</small><input id="tna" type="number" inputmode="decimal" step="0.1" min="0" value="4.5"></label>
<label>Relación cuota-ingreso (%) <small>la que exige el banco, suele ser 25 % a 35 %</small><input id="rel" type="number" min="1" max="100" value="25"></label>
</div>
<label>Inflación mensual esperada (%) <small>para estimar cómo sube la cuota</small><input id="inf" type="number" inputmode="decimal" step="0.1" value="2"></label>
<div id="res" class="result"></div>
<p class="note">Simulación orientativa: no incluye seguros, gastos de escritura ni comisiones. Cada banco tiene sus propias condiciones.</p>
</div>
<div class="article">
<h2>¿Cómo funciona un crédito UVA?</h2>
<p>El monto que te prestan se convierte a <strong>UVA</strong>, una unidad que sube todos los días con la inflación. Vos devolvés una cantidad fija de UVA por mes (sistema francés), pero como cada UVA vale más pesos con el tiempo, <strong>la cuota en pesos va subiendo</strong> al ritmo de la inflación.</p>
<p>A cambio, la tasa de interés es baja (en general, de un dígito anual), y la cuota inicial es mucho menor que en un crédito a tasa fija.</p>
<h3>¿Cuánto tengo que ganar?</h3>
<p>Los bancos piden que la cuota no supere un porcentaje de los ingresos del hogar, en general entre el <strong>25 % y el 35 %</strong>. Por eso el ingreso necesario es la cuota dividida por ese porcentaje.</p>
<h3>El riesgo principal</h3>
<p>Si tu sueldo sube <strong>menos que la inflación</strong> durante mucho tiempo, la cuota va a pesar cada vez más en tu presupuesto. Antes de tomar un crédito UVA, dejá margen y averiguá si el banco ofrece opciones de extensión de plazo cuando la cuota supera cierto porcentaje del sueldo.</p>
<p>Leé más en la guía <a href="../guias/credito-hipotecario-uva/">Cómo funciona el crédito hipotecario UVA</a>.</p>
</div>
''', faq=[
 ('¿Cuánto tengo que ganar para un crédito hipotecario UVA?', 'Depende del monto, el plazo y la tasa. Como referencia, el ingreso del hogar tiene que ser unas 3 a 4 veces la cuota inicial, según la relación que exija cada banco.'),
 ('¿La cuota de un crédito UVA sube todos los meses?', 'Sí: la cantidad de UVA es fija, pero el valor de la UVA en pesos sube con la inflación, así que la cuota en pesos también sube.'),
], script='''
conectar(() => {
  const M = val('monto'), n = Math.max(1, Math.round(val('anios'))) * 12, i = val('tna') / 100 / 12, rel = Math.max(1, val('rel')) / 100, inf = val('inf') / 100;
  const cuota = i ? M * i / (1 - Math.pow(1 + i, -n)) : M / n;
  const c12 = cuota * Math.pow(1 + inf, 12), c60 = cuota * Math.pow(1 + inf, 60);
  $('#res').innerHTML = `<div class="label">Cuota inicial</div><div class="big">${$$(cuota)}</div>` + filas([
    ['Ingreso mínimo del hogar (' + pct(rel * 100) + ')', $$(cuota / rel), 'total'],
    ['Cantidad de cuotas', n],
    ['Cuota en 1 año (con ' + pct(inf * 100) + ' mensual)', $$(c12)],
    ['Cuota en 5 años', $$(c60)],
    ['Total a devolver, en pesos de hoy', $$(cuota * n)],
  ]) + '<p class="note">"En pesos de hoy" significa sin contar la inflación: es lo que pagarías si los precios no subieran.</p>';
});
''')

# ---------- CALCULAR EDAD ----------
page('edad', 'Calcular edad exacta: años, meses y días',
 'Calculá tu edad exacta en años, meses y días a partir de tu fecha de nacimiento, cuántos días viviste y cuánto falta para tu próximo cumpleaños.',
 nombre='Calcular edad', body='''
<h1>Calcular edad</h1>
<p class="lead">Poné una fecha de nacimiento y te decimos la edad exacta, cuántos días pasaron y cuánto falta para el próximo cumpleaños.</p>
<div class="card calc">
<div class="row">
<label>Fecha de nacimiento<input id="nac" type="date" value="1995-06-15"></label>
<label>Calcular al día <small>por defecto, hoy</small><input id="ref" type="date"></label>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Para qué sirve?</h2>
<ul>
<li>Saber la edad exacta para un trámite, una jubilación o un seguro.</li>
<li>Calcular la edad que tenía alguien en una fecha determinada.</li>
<li>Saber cuántos días faltan para un cumpleaños.</li>
</ul>
<h3>¿Cómo se calcula?</h3>
<p>Se cuentan los años completos desde la fecha de nacimiento, después los meses completos y por último los días que sobran. Los años bisiestos se tienen en cuenta automáticamente.</p>
</div>
''', faq=[
 ('¿Cómo calculo mi edad exacta?', 'Restá el año de nacimiento al año actual y, si todavía no pasó tu cumpleaños este año, restá uno más. La calculadora además te da los meses y días.'),
 ('¿Qué pasa si nací un 29 de febrero?', 'En los años que no son bisiestos, se suele considerar que el cumpleaños es el 1 de marzo (o el 28 de febrero, según el uso).'),
], script='''
const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
if (!$('#ref').value) $('#ref').value = iso(new Date());
conectar(() => {
  const p = v => v ? new Date(v + 'T00:00:00') : null, a = p($('#nac').value), b = p($('#ref').value) || new Date();
  if (!a || b < a) { $('#res').innerHTML = 'Revisá las fechas.'; return; }
  let y = b.getFullYear() - a.getFullYear(), m = b.getMonth() - a.getMonth(), d = b.getDate() - a.getDate();
  if (d < 0) { m--; d += new Date(b.getFullYear(), b.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  const dias = Math.round((b - a) / 864e5);
  let prox = new Date(b.getFullYear(), a.getMonth(), a.getDate()); if (prox < b) prox = new Date(b.getFullYear() + 1, a.getMonth(), a.getDate());
  const falta = Math.round((prox - b) / 864e5);
  $('#res').innerHTML = `<div class="label">Edad</div><div class="big">${y} ${y === 1 ? 'año' : 'años'}</div>` + filas([
    ['Exacta', `${y} años, ${m} ${m === 1 ? 'mes' : 'meses'} y ${d} ${d === 1 ? 'día' : 'días'}`],
    ['Días vividos', num.format(dias)],
    ['Semanas', num.format(Math.floor(dias / 7))],
    ['Próximo cumpleaños', falta === 0 ? '¡Hoy!' : `en ${falta} ${falta === 1 ? 'día' : 'días'} (cumple ${y + 1})`],
    ['Día en que nació', a.toLocaleDateString('es-AR', { weekday: 'long' })],
  ]);
});
''')

# ---------- DÍAS ENTRE FECHAS ----------
page('dias-entre-fechas', 'Calculadora de días entre fechas y sumar días a una fecha',
 'Calculá cuántos días corridos, semanas y meses hay entre dos fechas, o qué fecha es si sumás o restás días. Rápido y gratis.',
 nombre='Días entre fechas', body='''
<h1>Días entre fechas</h1>
<p class="lead">Contá los días corridos entre dos fechas, o averiguá qué fecha es dentro de X días.</p>
<div class="card calc">
<label>¿Qué querés calcular?<select id="modo"><option value="entre">Días entre dos fechas</option><option value="sumar">Sumar o restar días a una fecha</option></select></label>
<div class="row">
<label>Fecha<input id="d0" type="date"></label>
<div data-modo="entre"><label>Hasta<input id="d1" type="date"></label></div>
<div data-modo="sumar"><label>Días <small>negativo para restar</small><input id="n" type="number" value="90"></label></div>
</div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Para qué sirve?</h2>
<ul>
<li>Saber cuántos días faltan para un viaje, un vencimiento o un evento.</li>
<li>Calcular la fecha en que termina un plazo de 30, 60 o 90 días corridos.</li>
<li>Contar cuántos días duró algo.</li>
</ul>
<p>Si el plazo es en <strong>días hábiles</strong> (sin fines de semana ni feriados), usá la <a href="../dias-habiles/">calculadora de días hábiles</a>.</p>
</div>
''', faq=[
 ('¿Se cuentan el primer y el último día?', 'La calculadora muestra la diferencia entre las dos fechas (sin contar el primer día). Si necesitás incluir los dos extremos, sumale 1.'),
], script='''
const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
const hoy = new Date(); if (!$('#d0').value) $('#d0').value = iso(hoy);
if (!$('#d1').value) $('#d1').value = iso(new Date(hoy.getFullYear(), 11, 31));
conectar(() => {
  modos('#modo');
  const p = v => v ? new Date(v + 'T00:00:00') : null, a = p($('#d0').value);
  if (!a) { $('#res').innerHTML = 'Elegí una fecha.'; return; }
  if ($('#modo').value === 'entre') {
    const b = p($('#d1').value); if (!b) { $('#res').innerHTML = 'Elegí la otra fecha.'; return; }
    const d = Math.round((b - a) / 864e5), ad = Math.abs(d);
    $('#res').innerHTML = `<div class="label">Diferencia</div><div class="big">${num.format(ad)} ${ad === 1 ? 'día' : 'días'}</div>` + filas([
      ['Semanas', num.format(Math.floor(ad / 7)) + ' y ' + (ad % 7) + ' días'], ['Meses (aprox.)', num.format(ad / 30.44)], ['Incluyendo ambos días', num.format(ad + 1)]]);
  } else {
    const x = new Date(a); x.setDate(x.getDate() + Math.round(val('n')));
    $('#res').innerHTML = `<div class="label">La fecha es</div><div class="big">${x.toLocaleDateString('es-AR')}</div><p class="note">${x.toLocaleDateString('es-AR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}</p>`;
  }
});
''')

# ---------- CONSUMO ELÉCTRICO ----------
APARATOS = [('Aire acondicionado 3000 frigorías (frío)', 1200), ('Aire acondicionado 2250 frigorías (frío)', 900), ('Estufa eléctrica / caloventor', 2000),
            ('Heladera con freezer', 150), ('Lavarropas', 500), ('Termotanque eléctrico', 1500), ('Pava eléctrica', 2000), ('Microondas', 1000),
            ('Plancha', 1200), ('Televisor LED 50"', 100), ('Computadora de escritorio', 200), ('Notebook', 60), ('Ventilador de pie', 60), ('Lámpara LED', 9)]
opciones = ''.join(f'<option value="{w}">{n} (~{w} W)</option>' for n, w in APARATOS)
page('consumo-electrico', 'Calculadora de consumo eléctrico: cuánto gasta cada electrodoméstico',
 'Calculá cuánto consume de luz un aire acondicionado, una estufa, la heladera u otro electrodoméstico, en kWh y en pesos por mes.',
 nombre='Consumo eléctrico', body=f'''
<h1>¿Cuánto gasta de luz un electrodoméstico?</h1>
<p class="lead">Elegí el aparato y cuánto lo usás, y te decimos cuántos kWh consume y cuánto te cuesta por mes.</p>
<div class="card calc">
<label>Electrodoméstico<select id="ap"><option value="0">Otro (cargá la potencia)</option>{opciones}</select></label>
<div class="row">
<label>Potencia (W) <small>figura en la etiqueta del aparato</small><input id="w" type="number" inputmode="decimal" min="0" value="1200"></label>
<label>Horas de uso por día<input id="h" type="number" inputmode="decimal" min="0" max="24" step="0.5" value="6"></label>
</div>
<div class="row">
<label>Días de uso por mes<input id="d" type="number" min="1" max="31" value="30"></label>
<label>Precio del kWh ($) <small>dividí el total de energía de tu factura por los kWh</small><input id="precio" type="number" inputmode="decimal" min="0" value="150"></label>
</div>
<div id="res" class="result"></div>
<p class="note">Las potencias son valores aproximados. Los aparatos con termostato (aire, heladera, estufa) no funcionan a máxima potencia todo el tiempo, así que el consumo real suele ser menor.</p>
</div>
<div class="article">
<h2>¿Cómo se calcula el consumo?</h2>
<p><em>Consumo (kWh) = potencia (W) × horas de uso ÷ 1.000</em>. Un aire acondicionado de 1.200 W usado 6 horas consume 7,2 kWh por día, unos 216 kWh por mes.</p>
<h3>¿Cuánto vale el kWh?</h3>
<p>Depende de tu distribuidora, tu provincia, tu nivel de subsidio y cuánto consumís. Para sacarlo, mirá tu factura: dividí el importe del cargo variable (energía) por los kWh consumidos. Recordá que la factura además tiene un cargo fijo e impuestos.</p>
<h3>Consejos para gastar menos</h3>
<ul>
<li>Poné el aire acondicionado en <strong>24 °C</strong>: cada grado menos aumenta bastante el consumo.</li>
<li>Elegí aparatos con <strong>etiqueta de eficiencia A</strong> o mejor, y aires "inverter".</li>
<li>Las estufas eléctricas y los termotanques son de los aparatos que más gastan.</li>
<li>Desenchufá lo que no usás: muchos aparatos consumen en modo espera.</li>
</ul>
</div>
''', faq=[
 ('¿Cuánto gasta un aire acondicionado por mes?', 'Un equipo de 3000 frigorías usado 6 horas por día consume alrededor de 200 kWh por mes. Multiplicalo por el precio del kWh de tu factura para saber el costo.'),
 ('¿Qué consume más, el aire o la estufa eléctrica?', 'En general, la estufa eléctrica o el caloventor, que consumen unos 2.000 W. Un aire acondicionado frío-calor inverter es más eficiente para calefaccionar.'),
], script='''
$('#ap').addEventListener('change', () => { if (+$('#ap').value) { $('#w').value = $('#ap').value; $('#w').dispatchEvent(new Event('input')); } });
conectar(() => {
  const w = val('w'), h = Math.min(24, val('h')), d = val('d'), precio = val('precio');
  const kd = w * h / 1000, km = kd * d;
  $('#res').innerHTML = `<div class="label">Costo por mes (energía)</div><div class="big">${$$(km * precio)}</div>` + filas([
    ['Consumo por día', num.format(kd) + ' kWh'],
    ['Consumo por mes', num.format(km) + ' kWh', 'total'],
    ['Costo por día', $$(kd * precio)],
    ['Costo por hora de uso', $$(w / 1000 * precio)],
  ]);
});
''')

# =================== GUÍAS ===================
page('guias/credito-hipotecario-uva', 'Cómo funciona el crédito hipotecario UVA: cuota, requisitos y riesgos',
 'Qué es un crédito hipotecario UVA, cómo se calcula la cuota, cuánto tenés que ganar, qué gastos tiene y cuáles son sus riesgos, explicado en simple.',
 nombre='Crédito hipotecario UVA', articulo=True, relacionadas=_rel('credito-hipotecario-uva'), body='''
<h1>Cómo funciona el crédito hipotecario UVA</h1>
<p class="lead">La forma más común de comprar una vivienda con crédito en Argentina, explicada paso a paso.</p>
<h2>¿Qué es la UVA?</h2>
<p>La <strong>Unidad de Valor Adquisitivo</strong> es una unidad que publica el Banco Central y que sube todos los días siguiendo la inflación (a través del índice CER). Si los precios suben un 2 % en un mes, la UVA también sube alrededor de un 2 %, con algo de rezago.</p>
<h2>¿Cómo se calcula la cuota?</h2>
<ol>
<li>El monto que te prestan se pasa a UVA al valor del día en que se otorga el crédito.</li>
<li>Se calcula una cuota fija <strong>en UVA</strong>, con el sistema francés y una tasa baja (en general, de un dígito anual).</li>
<li>Cada mes, la cuota en UVA se pasa a pesos al valor de ese día. Por eso <strong>la cuota en pesos sube con la inflación</strong>.</li>
</ol>
<p>Simulá tu caso con la <a href="../../credito-hipotecario-uva/">calculadora de crédito hipotecario UVA</a>.</p>
<h2>¿Qué piden los bancos?</h2>
<ul>
<li><strong>Ingresos demostrables:</strong> que la cuota no supere entre el 25 % y el 35 % del ingreso del hogar.</li>
<li><strong>Antigüedad laboral</strong> y buen historial crediticio.</li>
<li>Un <strong>ahorro previo</strong>: en general financian hasta el 75 % u 80 % del valor de la vivienda, así que necesitás el resto más los gastos.</li>
</ul>
<h2>Los gastos que no tenés que olvidar</h2>
<p>Además del anticipo, hay que pagar la escritura, la tasación, los seguros, el sellado (según la provincia) y, si hay, la comisión inmobiliaria. En total pueden sumar un porcentaje importante del valor de la propiedad: pedí el detalle antes de firmar.</p>
<h2>Ventajas y riesgos</h2>
<ul>
<li><strong>Ventaja:</strong> la cuota inicial es mucho más baja que en un crédito a tasa fija, y en general se parece a un alquiler.</li>
<li><strong>Riesgo:</strong> si los sueldos suben menos que la inflación durante un tiempo largo, la cuota pesa cada vez más. Conviene no tomar el máximo que te ofrecen y dejar margen.</li>
</ul>
<p class="note">Guía orientativa. Las condiciones cambian según el banco y el momento.</p>
''', faq=[
 ('¿Cuánto financian los bancos en un crédito hipotecario UVA?', 'En general, hasta el 75 % u 80 % del valor de la vivienda. El resto y los gastos de escritura los tenés que poner vos.'),
 ('¿Se puede cancelar antes un crédito UVA?', 'Sí. Podés hacer pagos anticipados parciales o totales; consultá si el banco cobra comisión.'),
])

page('guias/donde-tener-los-ahorros', 'Dónde tener los ahorros en pesos: cuenta remunerada, plazo fijo, UVA y fondos',
 'Comparación de las opciones más comunes para ahorrar en pesos en Argentina: cuenta remunerada, plazo fijo tradicional, plazo fijo UVA y fondos comunes de inversión.',
 nombre='Dónde tener tus ahorros', articulo=True, relacionadas=_rel('donde-tener-los-ahorros'), body='''
<h1>Dónde tener tus ahorros en pesos</h1>
<p class="lead">Las opciones más comunes y simples para que tus pesos no pierdan valor, comparadas.</p>
<h2>Comparación rápida</h2>
<table class="detail big-table"><tr><th>Opción</th><th>Disponibilidad</th><th>Rendimiento</th><th>Riesgo</th></tr>
<tr><td>Cuenta remunerada / billetera</td><td>Inmediata</td><td>Tasa variable, algo menor</td><td>Bajo</td></tr>
<tr><td>Plazo fijo tradicional</td><td>Desde 30 días</td><td>Tasa fija conocida</td><td>Bajo (garantía de depósitos)</td></tr>
<tr><td>Plazo fijo UVA</td><td>Desde 90 días</td><td>Inflación + tasa adicional</td><td>Bajo</td></tr>
<tr><td>Fondo común money market</td><td>Inmediata o 24 h</td><td>Similar a cuenta remunerada</td><td>Bajo</td></tr>
<tr><td>Fondos de renta fija / bonos</td><td>24 a 72 h</td><td>Puede ser mayor</td><td>Medio</td></tr></table>
<h2>¿Cuál elijo?</h2>
<ul>
<li><strong>Para el fondo de emergencia o la plata del mes:</strong> una cuenta remunerada o un money market, que podés usar en cualquier momento.</li>
<li><strong>Si no vas a necesitar la plata por un mes o más:</strong> un plazo fijo, que suele pagar algo más.</li>
<li><strong>Si te preocupa que la inflación suba:</strong> el plazo fijo UVA te protege, a cambio de inmovilizar la plata 90 días.</li>
<li><strong>Para plazos largos y si aceptás algo de riesgo:</strong> fondos de renta fija o bonos, mejor con asesoramiento.</li>
</ul>
<h2>La regla de oro: compará con la inflación</h2>
<p>Lo importante no es cuántos pesos ganás, sino si tu plata compra más o menos cosas al final. Compará siempre la <strong>tasa mensual</strong> con la <strong>inflación mensual</strong>. Usá el <a href="../../tasas/">conversor de tasas</a> para pasar la TNA a tasa mensual.</p>
<p class="note">Esta guía es informativa y no es una recomendación de inversión. Antes de invertir, informate sobre cada producto y sus riesgos.</p>
''', faq=[
 ('¿Los plazos fijos tienen garantía?', 'Sí, los depósitos en bancos argentinos tienen una garantía de SEDESA hasta un monto por persona y por banco. Las cuentas remuneradas de billeteras que invierten en fondos no tienen esa garantía.'),
 ('¿Qué es un fondo money market?', 'Es un fondo común de inversión que invierte en instrumentos de muy corto plazo y bajo riesgo. Muchas billeteras virtuales invierten el saldo de sus usuarios en este tipo de fondos.'),
])

page('guias/resumen-tarjeta-de-credito', 'Cómo leer el resumen de la tarjeta de crédito: pago mínimo, intereses y fechas',
 'Qué significa cada parte del resumen de la tarjeta de crédito: fecha de cierre y vencimiento, pago mínimo, intereses, CFT y cómo evitar pagar de más.',
 nombre='Resumen de la tarjeta', articulo=True, relacionadas=_rel('resumen-tarjeta-de-credito'), body='''
<h1>Cómo leer el resumen de la tarjeta de crédito</h1>
<p class="lead">Lo que significa cada número del resumen y cómo evitar los intereses más caros.</p>
<h2>Las fechas clave</h2>
<ul>
<li><strong>Fecha de cierre:</strong> el último día en que las compras entran en este resumen. Lo que compres después pasa al resumen siguiente.</li>
<li><strong>Fecha de vencimiento:</strong> el último día para pagar sin intereses ni recargos.</li>
<li><strong>Próximo cierre y vencimiento:</strong> te sirven para planificar compras. Comprar justo después del cierre te da casi dos meses hasta que tenés que pagar.</li>
</ul>
<h2>Pago total y pago mínimo</h2>
<p>El <strong>pago total</strong> cancela todo lo que debés y no genera intereses. El <strong>pago mínimo</strong> es lo menos que podés pagar para no estar en mora, pero sobre todo lo que no pagaste se cobran <strong>intereses de financiación</strong>, que son de los más caros del sistema.</p>
<p class="warn">Pagar el mínimo todos los meses hace que una deuda chica se vuelva grande. Si podés, pagá el total; si no, pagá lo más que puedas.</p>
<h2>Otros conceptos del resumen</h2>
<ul>
<li><strong>Intereses de financiación:</strong> se cobran sobre el saldo que no pagaste.</li>
<li><strong>Intereses punitorios:</strong> se suman si no pagás ni el mínimo antes del vencimiento.</li>
<li><strong>Cuotas:</strong> figuran como "cuota 3/6", por ejemplo. Cada mes se suma la cuota correspondiente.</li>
<li><strong>Impuestos y percepciones:</strong> en compras en dólares o en el exterior pueden sumarse percepciones que después, en algunos casos, se pueden recuperar.</li>
<li><strong>TNA, TEA y CFT:</strong> el resumen informa las tasas de financiación. El CFT es el costo total, el que importa. Leé la <a href="../tna-tea-cft/">guía de tasas</a>.</li>
</ul>
<h2>Consejos</h2>
<ol>
<li>Anotá tus cuotas pendientes para saber cuánto vas a pagar los próximos meses.</li>
<li>Activá el débito automático del pago total si podés.</li>
<li>Antes de financiar una compra grande, fijate si conviene pagar en cuotas o de contado con la <a href="../../cuotas/">calculadora de cuotas</a>.</li>
</ol>
''', faq=[
 ('¿Qué pasa si pago el mínimo de la tarjeta?', 'No entrás en mora, pero sobre el saldo que no pagaste te cobran intereses de financiación (más IVA), y ese saldo se suma al próximo resumen.'),
 ('¿Cuándo conviene comprar con tarjeta?', 'Justo después de la fecha de cierre: la compra entra en el resumen siguiente y tenés más tiempo hasta el vencimiento.'),
])

# ---------- LIQUIDACIÓN POR RENUNCIA ----------
page('liquidacion-renuncia', 'Calculadora de liquidación final por renuncia',
 'Calculá cuánto cobrás si renunciás a tu trabajo: días trabajados, aguinaldo proporcional y vacaciones no gozadas. Con el plazo de pago y cómo renunciar.',
 nombre='Liquidación por renuncia', body='''
<h1>Calculadora de liquidación por renuncia</h1>
<p class="lead">Si renunciás, no cobrás indemnización, pero sí te deben varios rubros. Calculá tu liquidación final.</p>
<div class="card calc">
<label>Sueldo bruto mensual ($)<input id="sueldo" type="number" inputmode="decimal" min="0" value="1000000"></label>
<div class="row">
<label>Fecha de ingreso<input id="ini" type="date" value="2022-03-01"></label>
<label>Último día de trabajo<input id="fin" type="date"></label>
</div>
<label>Días de vacaciones de este año que ya te tomaste<input id="tomadas" type="number" min="0" max="35" value="0"></label>
<label class="check"><input id="sinpre" type="checkbox"> No di los 15 días de preaviso</label>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Qué cobro si renuncio?</h2>
<p>Cuando renunciás no te corresponde indemnización por antigüedad, pero sí:</p>
<ul>
<li>Los <strong>días trabajados</strong> del último mes.</li>
<li>El <strong>aguinaldo proporcional</strong> del semestre.</li>
<li>Las <strong>vacaciones no gozadas</strong> del año, en proporción a lo trabajado, más su aguinaldo.</li>
</ul>
<h2>¿Cómo renunciar?</h2>
<p>La renuncia tiene que ser <strong>por escrito</strong>: lo habitual es enviar un <strong>telegrama laboral</strong>, que es gratuito para el trabajador, o hacerla ante la autoridad administrativa del trabajo. Una renuncia de palabra o por mensaje puede traer problemas.</p>
<h3>El preaviso del trabajador</h3>
<p>Si renunciás, la ley te pide avisar con <strong>15 días de anticipación</strong>. Si no lo hacés, el empleador puede descontarte esos 15 días de la liquidación. La calculadora te deja marcarlo.</p>
<h3>¿Cuándo me pagan?</h3>
<p>La liquidación final se paga dentro de los <strong>4 días hábiles</strong> después del último día de trabajo. También te tienen que dar el certificado de trabajo.</p>
<p>Si en vez de renunciar te despidieron, usá la <a href="../indemnizacion/">calculadora de indemnización</a>.</p>
</div>
''', faq=[
 ('¿Si renuncio me pagan las vacaciones?', 'Sí, te pagan las vacaciones no gozadas proporcionales a lo que trabajaste en el año, más el aguinaldo sobre ese monto.'),
 ('¿Si renuncio cobro el aguinaldo?', 'Sí, el aguinaldo proporcional a los días trabajados en el semestre.'),
 ('¿Cuánto preaviso tengo que dar si renuncio?', 'La Ley de Contrato de Trabajo pide 15 días de preaviso al trabajador que renuncia.'),
], script='''
$('#fin').value ||= new Date().toISOString().slice(0, 10);
conectar(() => {
  const sueldo = val('sueldo'), tomadas = Math.max(0, val('tomadas')), sinpre = $('#sinpre').checked;
  const p = v => v ? new Date(v + 'T00:00:00') : null, ini = p($('#ini').value), fin = p($('#fin').value), dia = 864e5;
  if (!ini || !fin || fin < ini) { $('#res').innerHTML = 'Revisá las fechas.'; return; }
  let anios = fin.getFullYear() - ini.getFullYear(); if (new Date(fin.getFullYear(), ini.getMonth(), ini.getDate()) > fin) anios--;
  const trab = sueldo / 30 * Math.min(30, fin.getDate());
  const semIni = new Date(fin.getFullYear(), fin.getMonth() < 6 ? 0 : 6, 1), semFin = new Date(fin.getFullYear(), fin.getMonth() < 6 ? 5 : 11, fin.getMonth() < 6 ? 30 : 31);
  const desde = ini > semIni ? ini : semIni;
  const sac = sueldo / 2 * (Math.round((fin - desde) / dia) + 1) / (Math.round((semFin - semIni) / dia) + 1);
  const diasAnio = anios < 5 ? 14 : anios < 10 ? 21 : anios < 20 ? 28 : 35;
  const ia = new Date(fin.getFullYear(), 0, 1), dA = ini > ia ? ini : ia;
  const diasVac = Math.max(0, diasAnio * (Math.round((fin - dA) / dia) + 1) / 365 - tomadas);
  const vac = sueldo / 25 * diasVac, sacVac = vac / 12, desc = sinpre ? sueldo / 2 : 0;
  const total = trab + sac + vac + sacVac - desc;
  $('#res').innerHTML = `<div class="label">Liquidación final estimada (bruto)</div><div class="big">${$$(total)}</div>` + filas([
    ['Días trabajados del mes', $$(trab)],
    ['Aguinaldo proporcional', $$(sac)],
    ['Vacaciones no gozadas (' + num.format(diasVac) + ' días)', $$(vac)],
    ['Aguinaldo sobre vacaciones', $$(sacVac)],
    ...(sinpre ? [['Descuento por falta de preaviso (15 días)', '− ' + $$(desc)]] : []),
    ['Total', $$(total), 'total'],
  ]) + '<p class="note">A estos montos se les descuentan los aportes (17 %).</p>';
});
''')

# ---------- PROMOCIONES DEL SÚPER ----------
page('promociones', 'Calculadora de promociones: 2x1, 3x2 y segunda unidad al 70 %',
 'Calculá cuánto ahorrás de verdad con las promociones del supermercado: 2x1, 3x2, 4x3, segunda unidad con descuento y porcentajes. Precio real por unidad.',
 nombre='Promociones del súper', body='''
<h1>¿Cuánto ahorro con la promo?</h1>
<p class="lead">2x1, 3x2, segunda unidad al 70 %… Calculá el descuento real y el precio que pagás por cada unidad.</p>
<div class="card calc">
<div class="row">
<label>Precio de cada unidad ($)<input id="precio" type="number" inputmode="decimal" min="0" value="2000"></label>
<label>Unidades que llevás<input id="cant" type="number" min="1" max="200" value="2"></label>
</div>
<label>Promoción<select id="promo">
<option value="2x1">2x1 (llevás 2, pagás 1)</option>
<option value="3x2">3x2 (llevás 3, pagás 2)</option>
<option value="4x3">4x3 (llevás 4, pagás 3)</option>
<option value="segunda">Segunda unidad con descuento</option>
<option value="porc">Descuento en todas las unidades</option>
</select></label>
<div data-modo="segunda"><label>Descuento de la segunda unidad (%)<input id="d2" type="number" min="0" max="100" value="70"></label></div>
<div data-modo="porc"><label>Descuento (%)<input id="dp" type="number" min="0" max="100" value="25"></label></div>
<div id="res" class="result"></div>
</div>
<div class="article">
<h2>¿Cuánto es el descuento real de cada promo?</h2>
<table class="detail big-table"><tr><th>Promoción</th><th>Descuento real</th></tr>
<tr><td>2x1</td><td>50 %</td></tr>
<tr><td>Segunda unidad al 80 %</td><td>40 %</td></tr>
<tr><td>Segunda unidad al 70 %</td><td>35 %</td></tr>
<tr><td>3x2</td><td>33 %</td></tr>
<tr><td>4x3</td><td>25 %</td></tr>
<tr><td>Segunda unidad al 50 %</td><td>25 %</td></tr></table>
<p>Ojo: "segunda unidad al 70 %" significa que la segunda tiene un <strong>70 % de descuento</strong>. Comprando dos, el descuento total es del 35 %, no del 70 %.</p>
<h3>Antes de aprovechar una promo</h3>
<ul>
<li>Fijate si vas a usar todo antes de que venza.</li>
<li>Compará con el precio por kilo o por litro de otras marcas: a veces una marca sin promo sigue siendo más barata.</li>
<li>Si la promo se aplica en el total, llevar una unidad impar (por ejemplo, 3 en un 2x1) hace que la última no tenga descuento.</li>
</ul>
</div>
''', faq=[
 ('¿Qué conviene más, 2x1 o segunda unidad al 70 %?', 'El 2x1, que equivale a un 50 % de descuento. La segunda unidad al 70 % equivale a un 35 % si llevás dos.'),
 ('¿Cuánto es el descuento de un 3x2?', 'Un 33 %: pagás 2 de cada 3 unidades.'),
], script='''
conectar(() => {
  const sel = $('#promo').value; document.querySelectorAll('[data-modo]').forEach(e => e.hidden = e.dataset.modo !== sel);
  const precio = val('precio'), cant = Math.max(1, Math.round(val('cant')));
  let pagas;
  if (sel === '2x1' || sel === '3x2' || sel === '4x3') { const n = +sel[0], m = +sel[2]; pagas = Math.floor(cant / n) * m * precio + (cant % n) * precio; }
  else if (sel === 'segunda') { const d = val('d2') / 100; pagas = Math.floor(cant / 2) * precio * (2 - d) + (cant % 2) * precio; }
  else pagas = cant * precio * (1 - val('dp') / 100);
  const lista = cant * precio, ahorro = lista - pagas;
  $('#res').innerHTML = `<div class="label">Pagás</div><div class="big">${$$(pagas)}</div>` + filas([
    ['Sin promoción', $$(lista)],
    ['Ahorrás', $$(ahorro)],
    ['Descuento real', lista ? pct(ahorro / lista * 100) : '—', 'total'],
    ['Precio por unidad', $$(pagas / cant)],
  ]);
});
''')

# ---------- GUÍA: ALTA EN EL MONOTRIBUTO ----------
page('guias/como-darse-de-alta-en-el-monotributo', 'Cómo darse de alta en el monotributo paso a paso',
 'Guía para inscribirte en el monotributo en ARCA: qué necesitás, cómo elegir la categoría, cómo facturar y qué obligaciones tenés todos los meses.',
 nombre='Alta en el monotributo', articulo=True, relacionadas=['monotributo', 'precio-de-venta', 'sueldo-por-hora'], body='''
<h1>Cómo darse de alta en el monotributo</h1>
<p class="lead">Si empezás a trabajar por tu cuenta o a vender, el monotributo es la forma más simple de estar en regla. Te contamos los pasos.</p>
<h2>¿Qué es el monotributo?</h2>
<p>Es un régimen simplificado para personas con ingresos chicos o medianos. Pagás <strong>una sola cuota mensual</strong> que incluye el impuesto, el aporte jubilatorio y la obra social, y podés emitir facturas.</p>
<h2>Qué necesitás</h2>
<ul>
<li><strong>CUIT</strong> (si no tenés, se tramita en ARCA).</li>
<li><strong>Clave fiscal</strong> nivel 3 o superior. Se saca desde la app Mi ARCA con el DNI y una selfie.</li>
<li>Un <strong>domicilio fiscal</strong> y los datos de tu actividad.</li>
<li>Una estimación de cuánto vas a facturar por año.</li>
</ul>
<h2>Paso a paso</h2>
<ol>
<li>Entrá a la web de ARCA con tu clave fiscal y buscá el <strong>Portal Monotributo</strong>.</li>
<li>Elegí <strong>adherirte</strong> y completá tus datos: actividad, domicilio y obra social.</li>
<li>Elegí la <strong>categoría</strong> según lo que estimás facturar en un año. Si recién empezás, se calcula proporcionalmente. Podés estimarla con la <a href="../../monotributo/">calculadora de monotributo</a>.</li>
<li>Confirmá. Vas a obtener la credencial y el código para pagar la cuota.</li>
<li>Para <strong>facturar</strong>, habilitá un punto de venta de factura electrónica en ARCA ("Comprobantes en línea" o la app).</li>
</ol>
<h2>Qué tenés que hacer todos los meses</h2>
<ul>
<li><strong>Pagar la cuota</strong>, que en general vence el día 20. Conviene adherir el débito automático.</li>
<li><strong>Emitir factura</strong> por cada venta o servicio.</li>
<li><strong>Recategorizarte</strong> dos veces por año, en enero y julio. Mirá la <a href="../recategorizacion-monotributo/">guía de recategorización</a>.</li>
</ul>
<h2>Además: Ingresos Brutos</h2>
<p>El monotributo es un impuesto nacional. En muchas provincias también tenés que inscribirte en <strong>Ingresos Brutos</strong>; algunas tienen un régimen simplificado unificado con el monotributo. Consultá en el organismo de tu provincia.</p>
<p class="note">Guía orientativa. Para tu caso puntual, consultá con un contador.</p>
''', faq=[
 ('¿Puedo estar en el monotributo y en relación de dependencia?', 'Sí. En ese caso, en general no pagás el aporte jubilatorio ni la obra social del monotributo (porque ya los pagás en tu trabajo), solo el impuesto integrado.'),
 ('¿Cuánto cuesta el monotributo?', 'Depende de la categoría. Podés ver la cuota de cada una en la calculadora de monotributo, con los valores vigentes.'),
])


# ---------- CONTACTO ----------
page('contacto', 'Contacto', 'Escribinos para consultas, sugerencias de calculadoras nuevas o para avisarnos de un error en Cuentas Claras.', nombre='Contacto', body='''
<h1>Contacto</h1>
<div class="article">
<p>¿Encontraste un error en una calculadora, querés proponer una nueva o tenés alguna consulta sobre el sitio? Escribinos.</p>
<div class="card" style="margin:20px 0">
<p style="margin:0 0 6px"><strong>Mail</strong></p>
<p style="margin:0"><a href="mailto:matiasj.carattoli@gmail.com">matiasj.carattoli@gmail.com</a></p>
</div>
<h2>Antes de escribir</h2>
<ul>
<li>Si encontraste un error, contanos <strong>en qué calculadora</strong> y <strong>qué datos cargaste</strong>, así lo podemos revisar rápido.</li>
<li>No podemos dar asesoramiento legal, contable ni financiero sobre casos particulares. Para eso, consultá con un profesional.</li>
<li>Nunca te vamos a pedir datos personales, claves ni datos de tarjetas.</li>
</ul>
<p>Respondemos en general dentro de los 2 o 3 días hábiles.</p>
<p>Conocé más sobre el sitio en <a href="../acerca/">Acerca de</a>.</p>
</div>
''')

#!/usr/bin/env python3
"""Build segmentation.html with embedded JSON data."""
import json

with open('/home/user/Arcadian-Outfitters-Data-Analysis/dashboard_data.json') as f:
    raw_json = f.read()

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arcadian Outfitters - Customer Segmentation Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
<style>
:root {
  --primary: #1a1a2e;
  --primary-light: #16213e;
  --accent: #e94560;
  --bg: #f4f6f9;
  --card: #ffffff;
  --text: #333;
  --text-light: #666;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --radius: 10px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #fff; padding: 18px 32px; display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.header h1 { font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }
.header .subtitle { font-size: 13px; opacity: 0.7; margin-top: 2px; }
.tabs {
  display: flex; background: var(--primary-light); padding: 0 24px; gap: 0;
  overflow-x: auto; border-bottom: 2px solid #0f3460;
}
.tab {
  padding: 12px 22px; color: rgba(255,255,255,0.6); cursor: pointer;
  font-size: 13px; font-weight: 500; border: none; background: none;
  white-space: nowrap; transition: all 0.2s; position: relative;
}
.tab:hover { color: rgba(255,255,255,0.9); background: rgba(255,255,255,0.05); }
.tab.active {
  color: #fff; background: rgba(255,255,255,0.1);
}
.tab.active::after {
  content: ''; position: absolute; bottom: -2px; left: 0; right: 0;
  height: 3px; background: var(--accent); border-radius: 3px 3px 0 0;
}
.content { padding: 24px; max-width: 1400px; margin: 0 auto; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.grid { display: grid; gap: 20px; }
.grid-2 { grid-template-columns: 1fr 1fr; }
.grid-3 { grid-template-columns: 1fr 1fr 1fr; }
.grid-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.grid-6 { grid-template-columns: repeat(6, 1fr); }
@media (max-width: 1100px) { .grid-4, .grid-6 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 768px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }
.card {
  background: var(--card); border-radius: var(--radius); padding: 20px;
  box-shadow: var(--shadow); border: 1px solid rgba(0,0,0,0.04);
}
.card h3 { font-size: 14px; color: var(--text-light); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-card {
  background: var(--card); border-radius: var(--radius); padding: 18px 20px;
  box-shadow: var(--shadow); text-align: center; border: 1px solid rgba(0,0,0,0.04);
}
.kpi-card .kpi-value { font-size: 28px; font-weight: 700; color: var(--primary); }
.kpi-card .kpi-label { font-size: 11px; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { background: #f8f9fa; padding: 10px 12px; text-align: left; font-weight: 600; color: var(--text-light); border-bottom: 2px solid #e9ecef; font-size: 11px; text-transform: uppercase; letter-spacing: 0.3px; }
td { padding: 9px 12px; border-bottom: 1px solid #f0f0f0; }
tr:hover { background: #fafbfc; }
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; color: #fff;
}
.seg-badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; color: #fff; font-weight: 600; display: inline-block; }
.search-box {
  width: 100%; padding: 10px 16px; border: 2px solid #e0e0e0; border-radius: 8px;
  font-size: 14px; outline: none; transition: border-color 0.2s;
}
.search-box:focus { border-color: var(--accent); }
.season-toggle {
  display: inline-flex; border-radius: 25px; overflow: hidden; border: 2px solid #e0e0e0;
  margin: 8px 0;
}
.season-btn {
  padding: 8px 20px; border: none; cursor: pointer; font-size: 13px; font-weight: 600;
  transition: all 0.2s; background: #fff; color: var(--text-light);
}
.season-btn.active-high { background: #FF6F00; color: #fff; }
.season-btn.active-low { background: #1565C0; color: #fff; }
.season-btn:hover:not(.active-high):not(.active-low) { background: #f5f5f5; }
select {
  padding: 8px 14px; border: 2px solid #e0e0e0; border-radius: 8px;
  font-size: 13px; outline: none; background: #fff; cursor: pointer;
}
select:focus { border-color: var(--accent); }
.filter-row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 16px; }
.table-wrap { overflow-x: auto; max-height: 500px; overflow-y: auto; }
.table-wrap table th { position: sticky; top: 0; z-index: 2; }
.detail-card {
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  color: #fff; border-radius: var(--radius); padding: 24px; margin-bottom: 20px;
}
.detail-card h2 { font-size: 20px; margin-bottom: 4px; }
.detail-card .meta { font-size: 13px; opacity: 0.7; }
.detail-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-top: 16px; }
.detail-stat { text-align: center; }
.detail-stat .val { font-size: 22px; font-weight: 700; }
.detail-stat .lbl { font-size: 11px; opacity: 0.7; text-transform: uppercase; }
.season-card {
  border-radius: 8px; padding: 16px; margin-top: 12px;
}
.season-high { background: rgba(255,111,0,0.1); border: 1px solid rgba(255,111,0,0.3); }
.season-low { background: rgba(21,101,194,0.1); border: 1px solid rgba(21,101,194,0.3); }
.season-card h4 { font-size: 13px; margin-bottom: 8px; }
.econ-box {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9); border-radius: var(--radius);
  padding: 24px; text-align: center; margin-bottom: 20px;
}
.econ-box .big { font-size: 36px; font-weight: 700; color: #2e7d32; }
.econ-box .sub { font-size: 14px; color: #555; margin-top: 4px; }
.math-row {
  display: flex; align-items: center; justify-content: center; gap: 20px;
  flex-wrap: wrap; margin: 20px 0;
}
.math-item { text-align: center; }
.math-item .num { font-size: 24px; font-weight: 700; }
.math-item .lbl { font-size: 12px; color: var(--text-light); }
.math-op { font-size: 28px; font-weight: 700; color: var(--text-light); }
.hidden { display: none; }
.click-row { cursor: pointer; }
.click-row:hover { background: #f0f4ff !important; }
.back-btn {
  display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px;
  background: var(--primary); color: #fff; border: none; border-radius: 8px;
  cursor: pointer; font-size: 13px; margin-bottom: 16px;
}
.back-btn:hover { opacity: 0.9; }
.chart-container { min-height: 350px; }
.seg-def { margin-bottom: 12px; padding: 12px 16px; border-radius: 8px; border-left: 4px solid; }
.seg-def h4 { font-size: 14px; margin-bottom: 4px; }
.seg-def p { font-size: 12px; color: var(--text-light); }
.full-width { grid-column: 1 / -1; }
.cadence-badge {
  display: inline-block; padding: 3px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; color: #fff;
}
.number { font-variant-numeric: tabular-nums; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Arcadian Outfitters</h1>
    <div class="subtitle">Customer Segmentation Dashboard</div>
  </div>
  <div style="text-align:right; font-size: 12px; opacity: 0.6;">
    Data through Feb 2026
  </div>
</div>

<div class="tabs" id="tabBar">
  <button class="tab active" data-tab="overview">Overview</button>
  <button class="tab" data-tab="cadence">Visit Cadence</button>
  <button class="tab" data-tab="economics">Visit Economics</button>
  <button class="tab" data-tab="depletion">Depletion Model</button>
  <button class="tab" data-tab="lookup">Customer Lookup</button>
  <button class="tab" data-tab="workload">Rep Workload</button>
  <button class="tab" data-tab="seasonal">Seasonal Trends</button>
</div>

<div class="content">

<!-- ===================== TAB 1: OVERVIEW ===================== -->
<div class="tab-panel active" id="panel-overview">
  <div class="grid grid-6" id="kpi-cards"></div>
  <div class="grid grid-2" style="margin-top:20px;">
    <div class="card"><h3>Customers by Segment</h3><div id="chart-seg-bar" class="chart-container"></div></div>
    <div class="card"><h3>Revenue Share by Segment</h3><div id="chart-rev-pie" class="chart-container"></div></div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Visit Cadence Distribution: High Season vs Low Season</h3>
    <div id="chart-cadence-grouped" class="chart-container"></div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Segment Summary</h3>
    <div class="table-wrap" id="seg-summary-table"></div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Segment Definitions</h3>
    <div id="seg-definitions"></div>
  </div>
</div>

<!-- ===================== TAB 2: VISIT CADENCE ===================== -->
<div class="tab-panel" id="panel-cadence">
  <div class="filter-row">
    <div class="season-toggle" id="cadence-season-toggle">
      <button class="season-btn active-high" data-season="high" onclick="setCadenceSeason('high')">High Season (Apr-Oct)</button>
      <button class="season-btn" data-season="low" onclick="setCadenceSeason('low')">Low Season (Nov-Mar)</button>
    </div>
    <select id="cadence-band-filter" onchange="filterCadenceTable()">
      <option value="all">All Cadence Bands</option>
    </select>
    <select id="cadence-seg-filter" onchange="filterCadenceTable()">
      <option value="all">All Segments</option>
    </select>
    <input type="text" class="search-box" id="cadence-search" placeholder="Search customers..." oninput="filterCadenceTable()" style="max-width:280px;">
  </div>
  <div class="card">
    <div class="table-wrap" style="max-height:450px;" id="cadence-table-wrap"></div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Visit Frequency vs Avg Order Value</h3>
    <div id="chart-cadence-scatter" class="chart-container"></div>
  </div>
</div>

<!-- ===================== TAB 3: VISIT ECONOMICS ===================== -->
<div class="tab-panel" id="panel-economics">
  <div class="econ-box">
    <div class="big" id="econ-profit"></div>
    <div class="sub">Profit per visit (at 75% trigger / 52 hats sold)</div>
  </div>
  <div class="card" style="margin-bottom:20px;">
    <h3>The Math</h3>
    <div class="math-row" id="econ-math"></div>
  </div>
  <div class="card" style="margin-bottom:20px;">
    <h3>Per-Segment Profitability</h3>
    <div class="table-wrap" id="econ-seg-table"></div>
  </div>
  <div class="card">
    <h3>Annual Profit Projection by Segment</h3>
    <div id="chart-econ-annual" class="chart-container"></div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Key Insight</h3>
    <p style="font-size:14px; line-height:1.7; color:#555;">
      Even at the conservative 75% trigger point (52 hats sold per visit), each service visit generates approximately
      <strong style="color:#2e7d32;">$480 in profit</strong> after accounting for the $45 visit cost and 15% commission.
      The display model makes every visit profitable because the minimum restock quantity (52 hats at $11.87 each)
      yields $617 in revenue before costs. Higher-velocity accounts simply require more frequent visits,
      compounding the profit opportunity. The key lever is visit frequency, not per-visit margin.
    </p>
  </div>
</div>

<!-- ===================== TAB 4: DEPLETION MODEL ===================== -->
<div class="tab-panel" id="panel-depletion">
  <div class="grid grid-2">
    <div class="card">
      <h3>Display Depletion - High Season (Apr-Oct)</h3>
      <div id="chart-depletion-high" class="chart-container" style="min-height:400px;"></div>
    </div>
    <div class="card">
      <h3>Display Depletion - Low Season (Nov-Mar)</h3>
      <div id="chart-depletion-low" class="chart-container" style="min-height:400px;"></div>
    </div>
  </div>
  <div class="card" style="margin-top:20px;">
    <h3>Velocity Comparison by Season</h3>
    <div class="table-wrap" id="depletion-table"></div>
  </div>
</div>

<!-- ===================== TAB 5: CUSTOMER LOOKUP ===================== -->
<div class="tab-panel" id="panel-lookup">
  <div id="lookup-list">
    <div class="filter-row">
      <input type="text" class="search-box" id="lookup-search" placeholder="Search by customer name, rep, or segment..." oninput="filterLookup()" style="max-width:400px;">
      <select id="lookup-seg-filter" onchange="filterLookup()">
        <option value="all">All Segments</option>
      </select>
      <select id="lookup-rep-filter" onchange="filterLookup()">
        <option value="all">All Reps</option>
      </select>
    </div>
    <div class="card">
      <div class="table-wrap" style="max-height:550px;" id="lookup-table-wrap"></div>
    </div>
  </div>
  <div id="lookup-detail" class="hidden"></div>
</div>

<!-- ===================== TAB 6: REP WORKLOAD ===================== -->
<div class="tab-panel" id="panel-workload">
  <div class="card" style="margin-bottom:20px;">
    <h3>Rep Summary</h3>
    <div class="table-wrap" id="rep-table-wrap"></div>
  </div>
  <div class="card">
    <h3>Segment Distribution by Rep</h3>
    <div id="chart-rep-stacked" class="chart-container" style="min-height:450px;"></div>
  </div>
</div>

<!-- ===================== TAB 7: SEASONAL TRENDS ===================== -->
<div class="tab-panel" id="panel-seasonal">
  <div class="card" style="margin-bottom:20px;">
    <h3>Monthly Revenue by Segment</h3>
    <div id="chart-monthly-seg" class="chart-container" style="min-height:380px;"></div>
  </div>
  <div class="card" style="margin-bottom:20px;">
    <h3>Monthly Revenue with Seasonal Shading</h3>
    <div id="chart-monthly-seasonal" class="chart-container" style="min-height:380px;"></div>
  </div>
  <div class="grid grid-2" style="margin-top:0;">
    <div class="card">
      <h3>Orders by Month</h3>
      <div id="chart-orders-month" class="chart-container"></div>
    </div>
    <div class="card">
      <h3>Orders by Day of Week</h3>
      <div id="chart-orders-dow" class="chart-container"></div>
    </div>
  </div>
</div>

</div><!-- /content -->

<script>
// ==================== EMBEDDED DATA ====================
const DATA = __JSON_DATA_PLACEHOLDER__;

const C = DATA.constants;
const segColors = DATA.seg_colors;
const cadColors = DATA.cadence_colors;
const cadOrder = DATA.cadence_order;
const segments = Object.keys(segColors);

// ==================== UTILITIES ====================
function fmt(n, d=0) {
  if (n == null || isNaN(n)) return '-';
  return Number(n).toLocaleString('en-US', {minimumFractionDigits:d, maximumFractionDigits:d});
}
function fmtD(n) { return '$' + fmt(n); }
function fmtD2(n) { return '$' + fmt(n, 2); }
function fmtPct(n) { return fmt(n,1) + '%'; }
function segBadge(seg) {
  const c = segColors[seg] || '#888';
  return '<span class="seg-badge" style="background:'+c+'">'+seg+'</span>';
}
function cadBadge(cad) {
  const c = cadColors[cad] || '#888';
  return '<span class="cadence-badge" style="background:'+c+'">'+cad+'</span>';
}

// ==================== TAB NAVIGATION ====================
document.querySelectorAll('.tab').forEach(t => {
  t.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('panel-' + t.dataset.tab).classList.add('active');
    // Resize plotly charts in the active tab
    setTimeout(() => {
      const panel = document.getElementById('panel-' + t.dataset.tab);
      panel.querySelectorAll('.js-plotly-plot').forEach(p => Plotly.Plots.resize(p));
    }, 50);
  });
});

// ==================== TAB 1: OVERVIEW ====================
function renderOverview() {
  const repeatRate = (C.repeat_customers / C.total_customers * 100).toFixed(1);
  const kpis = [
    {v: fmt(C.total_customers), l: 'Total Customers'},
    {v: fmtD(C.total_revenue), l: 'Total Revenue'},
    {v: fmt(C.total_hats), l: 'Total Hats Sold'},
    {v: repeatRate + '%', l: 'Repeat Rate'},
    {v: fmtD2(C.profit_per_visit), l: 'Profit per Visit'},
    {v: C.seasonal_ratio + 'x', l: 'Seasonal Ratio (H/L)'},
  ];
  document.getElementById('kpi-cards').innerHTML = kpis.map(k =>
    '<div class="kpi-card"><div class="kpi-value">'+k.v+'</div><div class="kpi-label">'+k.l+'</div></div>'
  ).join('');

  // Segment bar chart
  const ss = DATA.seg_summary;
  Plotly.newPlot('chart-seg-bar', [{
    x: ss.map(s=>s.Segment), y: ss.map(s=>s.Count),
    type: 'bar', marker: {color: ss.map(s=>segColors[s.Segment])},
    text: ss.map(s=>s.Count), textposition: 'outside',
    hovertemplate: '%{x}<br>%{y} customers<extra></extra>'
  }], {
    margin:{t:20,b:80,l:50,r:20}, xaxis:{tickangle:-25, tickfont:{size:11}},
    yaxis:{title:'Customers'}, plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Revenue pie
  Plotly.newPlot('chart-rev-pie', [{
    labels: ss.map(s=>s.Segment), values: ss.map(s=>s.TotalRev),
    type: 'pie', marker: {colors: ss.map(s=>segColors[s.Segment])},
    textinfo: 'label+percent', textposition: 'outside',
    hovertemplate: '%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>'
  }], {
    margin:{t:20,b:20,l:20,r:20}, showlegend:false,
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Grouped bar: cadence high vs low
  const highData = cadOrder.map(b => DATA.cadence_high[b] || 0);
  const lowData = cadOrder.map(b => DATA.cadence_low[b] || 0);
  Plotly.newPlot('chart-cadence-grouped', [
    {x: cadOrder, y: highData, name: 'High Season', type:'bar', marker:{color:'#FF6F00'},
     text: highData, textposition:'outside', hovertemplate:'%{x}<br>High: %{y}<extra></extra>'},
    {x: cadOrder, y: lowData, name: 'Low Season', type:'bar', marker:{color:'#1565C0'},
     text: lowData, textposition:'outside', hovertemplate:'%{x}<br>Low: %{y}<extra></extra>'}
  ], {
    barmode:'group', margin:{t:20,b:80,l:50,r:20},
    xaxis:{tickangle:-25, tickfont:{size:11}}, yaxis:{title:'Customers'},
    legend:{orientation:'h', y:1.1, x:0.5, xanchor:'center'},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Segment summary table
  let html = '<table><thead><tr>';
  html += '<th>Segment</th><th>Count</th><th>Total Revenue</th><th>Avg Revenue</th>';
  html += '<th>Avg Orders</th><th>Avg Order Value</th><th>Avg Hats/Order</th>';
  html += '<th>High Vel (hats/day)</th><th>Low Vel</th>';
  html += '<th>High Visit (days)</th><th>Low Visit</th>';
  html += '<th>Visits/Year</th><th>Avg Annual Profit</th><th>Rev Share</th>';
  html += '</tr></thead><tbody>';
  ss.forEach(s => {
    html += '<tr>';
    html += '<td>'+segBadge(s.Segment)+'</td>';
    html += '<td class="number">'+s.Count+'</td>';
    html += '<td class="number">'+fmtD(s.TotalRev)+'</td>';
    html += '<td class="number">'+fmtD(s.AvgRev)+'</td>';
    html += '<td class="number">'+fmt(s.AvgOrd,1)+'</td>';
    html += '<td class="number">'+fmtD2(s.AvgOV)+'</td>';
    html += '<td class="number">'+fmt(s.AvgHPO,1)+'</td>';
    html += '<td class="number">'+fmt(s.HighVel,2)+'</td>';
    html += '<td class="number">'+fmt(s.LowVel,2)+'</td>';
    html += '<td class="number">'+fmt(s.HighVisit,0)+'</td>';
    html += '<td class="number">'+fmt(s.LowVisit,0)+'</td>';
    html += '<td class="number">'+fmt(s.AvgVpY,1)+'</td>';
    html += '<td class="number">'+fmtD(s.AvgAP)+'</td>';
    html += '<td class="number">'+fmtPct(s.RevShare)+'</td>';
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('seg-summary-table').innerHTML = html;

  // Segment definitions
  const defs = [
    {seg:'A - High Velocity', desc:'Top-tier accounts with extremely high hat velocity. These stores deplete displays rapidly and require the most frequent visits.', hv:'Every 1-2 days', lv:'Every 1-2 days'},
    {seg:'B - Steady Performers', desc:'Reliable repeat customers with consistent ordering patterns. The backbone of recurring revenue.', hv:'Every ~26 days', lv:'Every ~35 days'},
    {seg:'C - Moderate Movers', desc:'Mid-range accounts with moderate velocity. Good potential for growth with the right attention.', hv:'Every ~69 days', lv:'Every ~93 days'},
    {seg:'D - Low & Slow', desc:'Lower velocity accounts that order less frequently. Still profitable per visit but require less frequent service.', hv:'Every ~50 days', lv:'Every ~62 days'},
    {seg:'E - New / One-Time', desc:'Recently acquired accounts or one-time buyers. Opportunity to convert into repeat customers.', hv:'Varies', lv:'Varies'},
  ];
  document.getElementById('seg-definitions').innerHTML = defs.map(d => {
    const c = segColors[d.seg] || '#888';
    return '<div class="seg-def" style="border-color:'+c+';background:'+c+'11;">' +
      '<h4 style="color:'+c+'">'+d.seg+'</h4>' +
      '<p>'+d.desc+'</p>' +
      '<p style="margin-top:4px;"><strong>High Season:</strong> '+d.hv+' &nbsp; | &nbsp; <strong>Low Season:</strong> '+d.lv+'</p>' +
      '</div>';
  }).join('');
}

// ==================== TAB 2: VISIT CADENCE ====================
let cadenceSeason = 'high';

function setCadenceSeason(s) {
  cadenceSeason = s;
  document.querySelectorAll('#cadence-season-toggle .season-btn').forEach(b => {
    b.classList.remove('active-high', 'active-low');
    if (b.dataset.season === s) b.classList.add(s === 'high' ? 'active-high' : 'active-low');
  });
  filterCadenceTable();
}

function initCadence() {
  // Populate filters
  const bandSel = document.getElementById('cadence-band-filter');
  cadOrder.forEach(b => { const o = document.createElement('option'); o.value=b; o.text=b; bandSel.add(o); });
  const segSel = document.getElementById('cadence-seg-filter');
  segments.forEach(s => { const o = document.createElement('option'); o.value=s; o.text=s; segSel.add(o); });
  filterCadenceTable();
}

function filterCadenceTable() {
  const band = document.getElementById('cadence-band-filter').value;
  const seg = document.getElementById('cadence-seg-filter').value;
  const q = document.getElementById('cadence-search').value.toLowerCase();
  const cadKey = cadenceSeason === 'high' ? 'HighCad' : 'LowCad';
  const visitKey = cadenceSeason === 'high' ? 'HighVisit' : 'LowVisit';
  const velKey = cadenceSeason === 'high' ? 'HighVel' : 'LowVel';
  const vpsKey = cadenceSeason === 'high' ? 'HighVpS' : 'LowVpS';

  let rows = DATA.customers.filter(c => {
    if (band !== 'all' && c[cadKey] !== band) return false;
    if (seg !== 'all' && c.Segment !== seg) return false;
    if (q && !c.Customer.toLowerCase().includes(q) && !(c.Primary_Rep||'').toLowerCase().includes(q)) return false;
    return true;
  });
  // Sort by visit frequency (ascending = most frequent first)
  rows.sort((a,b) => (a[visitKey]||9999) - (b[visitKey]||9999));

  let html = '<table><thead><tr>';
  html += '<th>Customer</th><th>Segment</th><th>Rep</th>';
  html += '<th>Visit Every (days)</th><th>Visits/Season</th>';
  html += '<th>Hats/Day</th><th>Avg Order</th><th>Net Revenue</th><th>Cadence</th>';
  html += '</tr></thead><tbody>';
  rows.slice(0, 200).forEach(c => {
    html += '<tr>';
    html += '<td>'+c.Customer+'</td>';
    html += '<td>'+segBadge(c.Segment)+'</td>';
    html += '<td>'+(c.Primary_Rep||'-')+'</td>';
    html += '<td class="number">'+fmt(c[visitKey],1)+'</td>';
    html += '<td class="number">'+fmt(c[vpsKey],1)+'</td>';
    html += '<td class="number">'+fmt(c[velKey],2)+'</td>';
    html += '<td class="number">'+fmtD2(c.AvgOV)+'</td>';
    html += '<td class="number">'+fmtD(c.NetRev)+'</td>';
    html += '<td>'+cadBadge(c[cadKey] || 'N/A')+'</td>';
    html += '</tr>';
  });
  if (rows.length > 200) html += '<tr><td colspan="9" style="text-align:center;color:#999;">Showing 200 of '+rows.length+' results</td></tr>';
  html += '</tbody></table>';
  document.getElementById('cadence-table-wrap').innerHTML = html;

  // Scatter plot
  renderCadenceScatter();
}

function renderCadenceScatter() {
  const visitKey = cadenceSeason === 'high' ? 'HighVisit' : 'LowVisit';
  const traces = [];
  segments.forEach(seg => {
    const pts = DATA.scatter.filter(s => s.Segment === seg && s[visitKey] > 0 && s.AvgOV > 0 && s.NetRev > 0);
    if (!pts.length) return;
    const maxRev = Math.max(...pts.map(p=>p.NetRev));
    traces.push({
      x: pts.map(p => p[visitKey]),
      y: pts.map(p => p.AvgOV),
      text: pts.map(p => p.Customer),
      mode: 'markers',
      name: seg,
      marker: {
        color: segColors[seg],
        size: pts.map(p => Math.max(6, Math.sqrt(p.NetRev / maxRev) * 40)),
        opacity: 0.7
      },
      hovertemplate: '%{text}<br>Visit every %{x:.0f} days<br>Avg order: $%{y:,.0f}<br><extra>'+seg+'</extra>'
    });
  });
  Plotly.newPlot('chart-cadence-scatter', traces, {
    xaxis: {title: 'Visit Frequency (days)', type:'log'},
    yaxis: {title: 'Avg Order Value ($)', type:'log'},
    margin: {t:20, b:60, l:70, r:20},
    legend: {orientation:'h', y:-0.2},
    plot_bgcolor: 'rgba(0,0,0,0)', paper_bgcolor: 'rgba(0,0,0,0)'
  }, {responsive: true});
}

// ==================== TAB 3: VISIT ECONOMICS ====================
function renderEconomics() {
  document.getElementById('econ-profit').textContent = fmtD2(C.profit_per_visit);

  const rev = C.revenue_per_visit;
  const comm = rev * C.commission_rate;
  const cost = C.visit_cost;
  const profit = C.profit_per_visit;

  document.getElementById('econ-math').innerHTML =
    '<div class="math-item"><div class="num" style="color:#1565C0;">'+fmtD2(rev)+'</div><div class="lbl">Revenue<br>(52 hats x $11.87)</div></div>' +
    '<div class="math-op">-</div>' +
    '<div class="math-item"><div class="num" style="color:#E65100;">'+fmtD2(comm)+'</div><div class="lbl">Commission<br>(15%)</div></div>' +
    '<div class="math-op">-</div>' +
    '<div class="math-item"><div class="num" style="color:#E65100;">'+fmtD2(cost)+'</div><div class="lbl">Visit Cost</div></div>' +
    '<div class="math-op">=</div>' +
    '<div class="math-item"><div class="num" style="color:#2e7d32;">'+fmtD2(profit)+'</div><div class="lbl">Profit per Visit</div></div>';

  // Per-segment table
  const ss = DATA.seg_summary;
  let html = '<table><thead><tr>';
  html += '<th>Segment</th><th>Customers</th><th>Avg Visits/Year</th>';
  html += '<th>Profit/Visit</th><th>Avg Annual Profit/Customer</th>';
  html += '<th>Total Segment Annual Profit</th>';
  html += '</tr></thead><tbody>';
  ss.forEach(s => {
    const totalAP = s.AvgAP * s.Count;
    html += '<tr>';
    html += '<td>'+segBadge(s.Segment)+'</td>';
    html += '<td class="number">'+s.Count+'</td>';
    html += '<td class="number">'+fmt(s.AvgVpY,1)+'</td>';
    html += '<td class="number">'+fmtD2(C.profit_per_visit)+'</td>';
    html += '<td class="number">'+fmtD(s.AvgAP)+'</td>';
    html += '<td class="number" style="font-weight:700;">'+fmtD(totalAP)+'</td>';
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('econ-seg-table').innerHTML = html;

  // Annual profit bar
  Plotly.newPlot('chart-econ-annual', [{
    x: ss.map(s=>s.Segment),
    y: ss.map(s=>s.AvgAP * s.Count),
    type: 'bar',
    marker: {color: ss.map(s=>segColors[s.Segment])},
    text: ss.map(s=>fmtD(s.AvgAP * s.Count)),
    textposition: 'outside',
    hovertemplate: '%{x}<br>$%{y:,.0f}<extra></extra>'
  }], {
    margin:{t:20,b:80,l:80,r:20},
    xaxis:{tickangle:-25, tickfont:{size:11}},
    yaxis:{title:'Annual Profit ($)', tickformat:'$,.0f'},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});
}

// ==================== TAB 4: DEPLETION MODEL ====================
function renderDepletion() {
  const fullHats = C.full_display_hats; // 208
  const trigger = fullHats * (C.visit_trigger_pct / 100); // 75% = 156
  const floor = C.hard_floor_hats; // 104

  function plotDepletion(divId, season) {
    const traces = [];
    segments.forEach(seg => {
      const key = seg + '|' + season;
      const vel = DATA.depletion[key];
      if (!vel || vel <= 0) return;
      const daysToEmpty = Math.ceil(fullHats / vel);
      const maxDays = Math.min(daysToEmpty, 365);
      const xs = [], ys = [];
      for (let d = 0; d <= maxDays; d++) {
        xs.push(d);
        ys.push(Math.max(0, fullHats - vel * d));
      }
      traces.push({
        x: xs, y: ys, name: seg, mode: 'lines',
        line: {color: segColors[seg], width: 2.5},
        hovertemplate: seg + '<br>Day %{x}<br>%{y:.0f} hats remaining<extra></extra>'
      });
    });

    // Add threshold shapes
    const layout = {
      margin:{t:10,b:50,l:60,r:20},
      xaxis:{title:'Days', range:[0, 200]},
      yaxis:{title:'Hats Remaining', range:[0, fullHats + 10]},
      shapes: [
        {type:'rect', x0:0, x1:200, y0:trigger, y1:fullHats, fillcolor:'rgba(255,152,0,0.08)', line:{width:0}},
        {type:'line', x0:0, x1:200, y0:trigger, y1:trigger, line:{color:'#FF9800', width:2, dash:'dash'}},
        {type:'rect', x0:0, x1:200, y0:floor, y1:trigger, fillcolor:'rgba(255,152,0,0.15)', line:{width:0}},
        {type:'line', x0:0, x1:200, y0:floor, y1:floor, line:{color:'#D32F2F', width:2, dash:'dash'}},
      ],
      annotations: [
        {x:195, y:trigger+5, text:'75% Full (Visit Trigger)', showarrow:false, font:{size:10, color:'#FF9800'}, xanchor:'right'},
        {x:195, y:floor+5, text:'50% Full (Hard Floor)', showarrow:false, font:{size:10, color:'#D32F2F'}, xanchor:'right'},
      ],
      legend:{orientation:'h', y:-0.18},
      plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
    };
    Plotly.newPlot(divId, traces, layout, {responsive:true});
  }

  plotDepletion('chart-depletion-high', 'High');
  plotDepletion('chart-depletion-low', 'Low');

  // Velocity table
  let html = '<table><thead><tr>';
  html += '<th>Segment</th><th>High Season Velocity (hats/day)</th><th>Low Season Velocity</th>';
  html += '<th>Days to Trigger (High)</th><th>Days to Trigger (Low)</th>';
  html += '<th>Days to Floor (High)</th><th>Days to Floor (Low)</th>';
  html += '</tr></thead><tbody>';
  segments.forEach(seg => {
    const hv = DATA.depletion[seg+'|High'] || 0;
    const lv = DATA.depletion[seg+'|Low'] || 0;
    const trigHats = fullHats - trigger; // hats to sell before trigger = 52
    const floorHats = fullHats - floor; // hats to sell before floor = 104
    html += '<tr>';
    html += '<td>'+segBadge(seg)+'</td>';
    html += '<td class="number">'+fmt(hv,2)+'</td>';
    html += '<td class="number">'+fmt(lv,2)+'</td>';
    html += '<td class="number">'+(hv>0? fmt(trigHats/hv,1) : '-')+'</td>';
    html += '<td class="number">'+(lv>0? fmt(trigHats/lv,1) : '-')+'</td>';
    html += '<td class="number">'+(hv>0? fmt(floorHats/hv,1) : '-')+'</td>';
    html += '<td class="number">'+(lv>0? fmt(floorHats/lv,1) : '-')+'</td>';
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('depletion-table').innerHTML = html;
}

// ==================== TAB 5: CUSTOMER LOOKUP ====================
function initLookup() {
  const segSel = document.getElementById('lookup-seg-filter');
  segments.forEach(s => { const o = document.createElement('option'); o.value=s; o.text=s; segSel.add(o); });
  const repSel = document.getElementById('lookup-rep-filter');
  const reps = [...new Set(DATA.customers.map(c=>c.Primary_Rep||'Unassigned'))].sort();
  reps.forEach(r => { const o = document.createElement('option'); o.value=r; o.text=r; repSel.add(o); });
  filterLookup();
}

function filterLookup() {
  const q = document.getElementById('lookup-search').value.toLowerCase();
  const seg = document.getElementById('lookup-seg-filter').value;
  const rep = document.getElementById('lookup-rep-filter').value;

  let rows = DATA.customers.filter(c => {
    if (seg !== 'all' && c.Segment !== seg) return false;
    if (rep !== 'all' && (c.Primary_Rep||'Unassigned') !== rep) return false;
    if (q && !c.Customer.toLowerCase().includes(q) && !(c.Primary_Rep||'').toLowerCase().includes(q) && !c.Segment.toLowerCase().includes(q)) return false;
    return true;
  });
  rows.sort((a,b) => b.NetRev - a.NetRev);

  let html = '<table><thead><tr>';
  html += '<th>Customer</th><th>Segment</th><th>Rep</th><th>Revenue</th><th>Orders</th><th>Hats</th><th>Avg Order</th>';
  html += '</tr></thead><tbody>';
  rows.slice(0,200).forEach(c => {
    html += '<tr class="click-row" onclick="showCustomerDetail(\''+c.Customer.replace(/'/g,"\\'").replace(/"/g,"&quot;")+'\')">';
    html += '<td style="color:#1565C0;font-weight:500;">'+c.Customer+'</td>';
    html += '<td>'+segBadge(c.Segment)+'</td>';
    html += '<td>'+(c.Primary_Rep||'-')+'</td>';
    html += '<td class="number">'+fmtD(c.NetRev)+'</td>';
    html += '<td class="number">'+c.Orders+'</td>';
    html += '<td class="number">'+fmt(c.TotalHats)+'</td>';
    html += '<td class="number">'+fmtD2(c.AvgOV)+'</td>';
    html += '</tr>';
  });
  if (rows.length > 200) html += '<tr><td colspan="7" style="text-align:center;color:#999;">Showing 200 of '+rows.length+' results</td></tr>';
  html += '</tbody></table>';
  document.getElementById('lookup-table-wrap').innerHTML = html;
}

function showCustomerDetail(name) {
  const c = DATA.customers.find(x => x.Customer === name);
  if (!c) return;
  document.getElementById('lookup-list').classList.add('hidden');
  const detail = document.getElementById('lookup-detail');
  detail.classList.remove('hidden');

  const invoices = DATA.invoice_history.filter(i => i.Customer === name);

  let html = '<button class="back-btn" onclick="hideCustomerDetail()">&#8592; Back to list</button>';
  html += '<div class="detail-card">';
  html += '<h2>'+c.Customer+'</h2>';
  html += '<div class="meta">'+segBadge(c.Segment)+' &nbsp; Rep: '+(c.Primary_Rep||'Unassigned')+'</div>';
  html += '<div class="detail-grid">';
  html += '<div class="detail-stat"><div class="val">'+fmtD(c.NetRev)+'</div><div class="lbl">Net Revenue</div></div>';
  html += '<div class="detail-stat"><div class="val">'+c.Orders+'</div><div class="lbl">Orders</div></div>';
  html += '<div class="detail-stat"><div class="val">'+fmt(c.TotalHats)+'</div><div class="lbl">Total Hats</div></div>';
  html += '<div class="detail-stat"><div class="val">'+fmtD2(c.AvgOV)+'</div><div class="lbl">Avg Order Value</div></div>';
  html += '<div class="detail-stat"><div class="val">'+fmt(c.AvgHPO,1)+'</div><div class="lbl">Avg Hats/Order</div></div>';
  html += '<div class="detail-stat"><div class="val">'+fmtD(c.AnnProfit)+'</div><div class="lbl">Annual Profit Est.</div></div>';
  html += '</div></div>';

  // Season cards
  html += '<div class="grid grid-2">';
  html += '<div class="card season-card season-high">';
  html += '<h4 style="color:#E65100;">High Season (Apr-Oct)</h4>';
  html += '<p><strong>Velocity:</strong> '+fmt(c.HighVel,2)+' hats/day</p>';
  html += '<p><strong>Visit Every:</strong> '+fmt(c.HighVisit,1)+' days</p>';
  html += '<p><strong>Cadence:</strong> '+cadBadge(c.HighCad||'N/A')+'</p>';
  html += '<p><strong>Visits/Season:</strong> '+fmt(c.HighVpS,1)+'</p>';
  html += '</div>';
  html += '<div class="card season-card season-low">';
  html += '<h4 style="color:#0D47A1;">Low Season (Nov-Mar)</h4>';
  html += '<p><strong>Velocity:</strong> '+fmt(c.LowVel,2)+' hats/day</p>';
  html += '<p><strong>Visit Every:</strong> '+fmt(c.LowVisit,1)+' days</p>';
  html += '<p><strong>Cadence:</strong> '+cadBadge(c.LowCad||'N/A')+'</p>';
  html += '<p><strong>Visits/Season:</strong> '+fmt(c.LowVpS,1)+'</p>';
  html += '</div></div>';

  // Order history
  if (invoices.length) {
    html += '<div class="card" style="margin-top:20px;">';
    html += '<h3>Order History</h3>';
    html += '<div class="table-wrap"><table><thead><tr>';
    html += '<th>Date</th><th>Document</th><th>Revenue</th><th>Hats</th><th>Lines</th><th>Season</th>';
    html += '</tr></thead><tbody>';
    invoices.forEach(inv => {
      const seasonColor = inv.Season === 'High' ? '#FF6F00' : '#1565C0';
      html += '<tr>';
      html += '<td>'+inv.Date_str+'</td>';
      html += '<td>'+inv.Doc+'</td>';
      html += '<td class="number">'+fmtD(inv.Rev)+'</td>';
      html += '<td class="number">'+fmt(inv.Hats)+'</td>';
      html += '<td class="number">'+inv.Lines+'</td>';
      html += '<td><span style="color:'+seasonColor+';font-weight:600;">'+inv.Season+'</span></td>';
      html += '</tr>';
    });
    html += '</tbody></table></div></div>';
  }
  detail.innerHTML = html;
}

function hideCustomerDetail() {
  document.getElementById('lookup-detail').classList.add('hidden');
  document.getElementById('lookup-list').classList.remove('hidden');
}

// ==================== TAB 6: REP WORKLOAD ====================
function renderRepWorkload() {
  const rs = DATA.rep_summary.slice().sort((a,b) => b.Revenue - a.Revenue);

  let html = '<table><thead><tr>';
  html += '<th>Rep</th><th>Customers</th><th>Revenue</th>';
  html += '<th>Est Visits/Month</th><th>Est Visits/Year</th>';
  html += '<th>Annual Profit</th>';
  html += '<th>High Vel</th><th>Steady</th><th>Moderate</th><th>Low&Slow</th><th>New</th>';
  html += '</tr></thead><tbody>';
  rs.forEach(r => {
    html += '<tr>';
    html += '<td style="font-weight:500;">'+r.Primary_Rep+'</td>';
    html += '<td class="number">'+r.Customers+'</td>';
    html += '<td class="number">'+fmtD(r.Revenue)+'</td>';
    html += '<td class="number">'+fmt(r.VpM,0)+'</td>';
    html += '<td class="number">'+fmt(r.TotalVisits,0)+'</td>';
    html += '<td class="number" style="font-weight:700;">'+fmtD(r.AnnProfit)+'</td>';
    html += '<td class="number">'+r.HighVel+'</td>';
    html += '<td class="number">'+r.Steady+'</td>';
    html += '<td class="number">'+r.Moderate+'</td>';
    html += '<td class="number">'+r.LowSlow+'</td>';
    html += '<td class="number">'+r.New+'</td>';
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('rep-table-wrap').innerHTML = html;

  // Stacked bar
  const repsForChart = rs.filter(r => r.Primary_Rep !== 'Unassigned').slice(0, 15);
  const segKeys = ['A - High Velocity','B - Steady Performers','C - Moderate Movers','D - Low & Slow','E - New / One-Time'];
  const fieldMap = {'A - High Velocity':'HighVel','B - Steady Performers':'Steady','C - Moderate Movers':'Moderate','D - Low & Slow':'LowSlow','E - New / One-Time':'New'};
  const traces = segKeys.map(seg => ({
    x: repsForChart.map(r => r.Primary_Rep),
    y: repsForChart.map(r => r[fieldMap[seg]] || 0),
    name: seg, type: 'bar',
    marker: {color: segColors[seg]},
    hovertemplate: '%{x}<br>'+seg+': %{y}<extra></extra>'
  }));
  Plotly.newPlot('chart-rep-stacked', traces, {
    barmode: 'stack',
    margin:{t:20,b:100,l:50,r:20},
    xaxis:{tickangle:-35, tickfont:{size:11}},
    yaxis:{title:'Customers'},
    legend:{orientation:'h', y:1.12, x:0.5, xanchor:'center', font:{size:10}},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});
}

// ==================== TAB 7: SEASONAL TRENDS ====================
function renderSeasonalTrends() {
  // Monthly revenue by segment
  const mt = DATA.monthly_trends;
  const months = [...new Set(mt.map(m=>m.Month_str))].sort();
  const segTraces = segments.map(seg => {
    const segData = mt.filter(m=>m.Segment===seg);
    const monthMap = {};
    segData.forEach(m => monthMap[m.Month_str] = m.Revenue);
    return {
      x: months, y: months.map(m => monthMap[m] || 0),
      name: seg, type: 'scatter', mode: 'lines+markers',
      line: {color: segColors[seg], width: 2},
      marker: {size: 5},
      hovertemplate: seg+'<br>%{x}<br>$%{y:,.0f}<extra></extra>'
    };
  });
  Plotly.newPlot('chart-monthly-seg', segTraces, {
    margin:{t:20,b:60,l:80,r:20},
    xaxis:{tickangle:-45, tickfont:{size:11}},
    yaxis:{title:'Revenue ($)', tickformat:'$,.0f'},
    legend:{orientation:'h', y:1.12, x:0.5, xanchor:'center', font:{size:10}},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Monthly revenue with seasonal shading
  const ms = DATA.monthly_seasonal;
  const allMonths = [...new Set(ms.map(m=>m.Month_str))].sort();

  // Build seasonal shapes
  const shapes = [];
  allMonths.forEach((m, i) => {
    const rec = ms.find(r => r.Month_str === m);
    const isHigh = rec && rec.Season.includes('High');
    shapes.push({
      type: 'rect', xref: 'x', yref: 'paper',
      x0: i - 0.5, x1: i + 0.5, y0: 0, y1: 1,
      fillcolor: isHigh ? 'rgba(255,111,0,0.07)' : 'rgba(21,101,194,0.07)',
      line: {width: 0}
    });
  });

  // Aggregate revenue per month
  const monthRev = {};
  ms.forEach(m => { monthRev[m.Month_str] = (monthRev[m.Month_str]||0) + m.Revenue; });

  Plotly.newPlot('chart-monthly-seasonal', [{
    x: allMonths, y: allMonths.map(m=>monthRev[m]||0),
    type: 'bar',
    marker: {color: allMonths.map(m => {
      const rec = ms.find(r=>r.Month_str===m);
      return rec && rec.Season.includes('High') ? '#FF6F00' : '#1565C0';
    })},
    hovertemplate: '%{x}<br>$%{y:,.0f}<extra></extra>'
  }], {
    shapes: shapes,
    margin:{t:20,b:60,l:80,r:20},
    xaxis:{tickangle:-45, tickfont:{size:11}},
    yaxis:{title:'Revenue ($)', tickformat:'$,.0f'},
    annotations: [
      {x:0.15, y:1.05, xref:'paper', yref:'paper', text:'High Season', font:{color:'#FF6F00', size:12, weight:700}, showarrow:false},
      {x:0.85, y:1.05, xref:'paper', yref:'paper', text:'Low Season', font:{color:'#1565C0', size:12, weight:700}, showarrow:false}
    ],
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Orders by month
  const mp = DATA.monthly_pattern;
  const monthNames = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const monthNums = Object.keys(mp).map(Number).sort((a,b)=>a-b);
  const monthLabels = monthNums.map(n => monthNames[n]||n);
  const monthColors = monthNums.map(n => (n>=4 && n<=10) ? '#FF6F00' : '#1565C0');

  // Shapes for orders by month
  const ordShapes = monthNums.map((n, i) => ({
    type:'rect', xref:'x', yref:'paper',
    x0: i-0.5, x1: i+0.5, y0:0, y1:1,
    fillcolor: (n>=4 && n<=10) ? 'rgba(255,111,0,0.07)' : 'rgba(21,101,194,0.07)',
    line:{width:0}
  }));

  Plotly.newPlot('chart-orders-month', [{
    x: monthLabels, y: monthNums.map(n=>mp[String(n)]),
    type:'bar', marker:{color: monthColors},
    hovertemplate:'%{x}: %{y} orders<extra></extra>'
  }], {
    shapes: ordShapes,
    margin:{t:20,b:40,l:50,r:20},
    yaxis:{title:'Orders'},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});

  // Orders by day of week
  const dp = DATA.dow_pattern;
  const dowNames = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const dowNums = [0,1,2,3,4,5,6];
  Plotly.newPlot('chart-orders-dow', [{
    x: dowNames, y: dowNums.map(n=>dp[String(n)]||0),
    type:'bar', marker:{color:'#5C6BC0'},
    hovertemplate:'%{x}: %{y} orders<extra></extra>'
  }], {
    margin:{t:20,b:40,l:50,r:20},
    yaxis:{title:'Orders'},
    plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)'
  }, {responsive:true});
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', function() {
  renderOverview();
  initCadence();
  renderEconomics();
  renderDepletion();
  initLookup();
  renderRepWorkload();
  renderSeasonalTrends();
});
</script>
</body>
</html>'''

# Insert JSON data
html_output = HTML_TEMPLATE.replace('__JSON_DATA_PLACEHOLDER__', raw_json)

with open('/home/user/Arcadian-Outfitters-Data-Analysis/segmentation.html', 'w') as f:
    f.write(html_output)

print(f"Written segmentation.html: {len(html_output):,} bytes")

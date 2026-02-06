import { useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from 'recharts';
import { sampleData } from './data/sampleData';

const tierColors = {
  Strategic: '#7f1d1d',
  Core: '#1d4ed8',
  Growth: '#0f766e',
  'Long-tail': '#6b7280',
};

const money = (v) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v || 0);

const monthLabel = (m) => {
  const [y, mo] = m.split('-');
  return new Date(Number(y), Number(mo) - 1, 1).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
};

export default function App() {
  const [tierFilter, setTierFilter] = useState('All');
  const [search, setSearch] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(sampleData.customers[0]?.customer || '');

  const filteredCustomers = useMemo(() => {
    return sampleData.customers
      .filter((c) => (tierFilter === 'All' ? true : c.tier === tierFilter))
      .filter((c) => c.customer.toLowerCase().includes(search.toLowerCase()))
      .sort((a, b) => b.avgMonthlySales - a.avgMonthlySales);
  }, [tierFilter, search]);

  const tierSummary = useMemo(() => {
    const groups = ['Strategic', 'Core', 'Growth', 'Long-tail'];
    return groups.map((tier) => {
      const subset = sampleData.customers.filter((c) => c.tier === tier);
      return {
        tier,
        count: subset.length,
        avgMonthlySales: subset.reduce((sum, c) => sum + c.avgMonthlySales, 0),
      };
    });
  }, []);

  const topVisitList = useMemo(
    () => [...sampleData.customers].sort((a, b) => b.avgMonthlySales - a.avgMonthlySales).slice(0, 12),
    [],
  );

  const scatterData = useMemo(() => {
    return filteredCustomers.map((c) => ({
      x: c.activeMonths,
      y: c.avgMonthlySales,
      z: Math.abs(c.totalSales),
      name: c.customer,
      tier: c.tier,
      visitFrequency: c.visitFrequency,
    }));
  }, [filteredCustomers]);

  const selectedTrend = useMemo(() => {
    const trend = sampleData.monthlyByCustomer[selectedCustomer] || {};
    return sampleData.months.map((month) => ({ month, sales: trend[month] || 0 }));
  }, [selectedCustomer]);

  const cardStyle = {
    background: '#fff',
    border: '1px solid #e5e7eb',
    borderRadius: 10,
    padding: 16,
  };

  return (
    <div style={{ fontFamily: 'Inter, Arial, sans-serif', background: '#f8fafc', minHeight: '100vh', color: '#0f172a' }}>
      <header style={{ padding: '20px 24px', borderBottom: '1px solid #e2e8f0', background: '#fff' }}>
        <h1 style={{ margin: 0, fontSize: 24 }}>Customer Visit Prioritization Dashboard</h1>
        <p style={{ margin: '6px 0 0', color: '#475569', fontSize: 14 }}>
          Data model combines all provided files and groups customers by average monthly sales volume.
        </p>
      </header>

      <main style={{ padding: 24, display: 'grid', gap: 16 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', gap: 12 }}>
          <div style={cardStyle}><strong>Total Customers</strong><div style={{ fontSize: 28 }}>{sampleData.customers.length}</div></div>
          <div style={cardStyle}><strong>Tracked Months</strong><div style={{ fontSize: 28 }}>{sampleData.months.length}</div></div>
          <div style={cardStyle}><strong>Highest Priority</strong><div style={{ fontSize: 20 }}>Weekly</div><div style={{ color: '#64748b' }}>Strategic accounts</div></div>
          <div style={cardStyle}><strong>Sources Ingested</strong><div style={{ fontSize: 12, marginTop: 8 }}>{Object.entries(sampleData.sourceCounts).map(([k, v]) => <div key={k}>{k}: {v.toLocaleString()} rows</div>)}</div></div>
        </div>

        <div style={{ ...cardStyle, display: 'grid', gridTemplateColumns: '220px 1fr', gap: 12 }}>
          <div>
            <label>Tier Filter</label>
            <select value={tierFilter} onChange={(e) => setTierFilter(e.target.value)} style={{ width: '100%', marginTop: 6, padding: 8 }}>
              <option>All</option>
              <option>Strategic</option>
              <option>Core</option>
              <option>Growth</option>
              <option>Long-tail</option>
            </select>
          </div>
          <div>
            <label>Find Customer</label>
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by customer name" style={{ width: '100%', marginTop: 6, padding: 8 }} />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Tier Composition (count of customers)</h3>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={tierSummary} dataKey="count" nameKey="tier" outerRadius={95} label>
                  {tierSummary.map((entry) => (
                    <Cell key={entry.tier} fill={tierColors[entry.tier]} />
                  ))}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Top Accounts by Average Monthly Sales</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={topVisitList} layout="vertical" margin={{ left: 30 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" tickFormatter={money} />
                <YAxis dataKey="customer" type="category" width={130} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v) => money(v)} />
                <Bar dataKey="avgMonthlySales">
                  {topVisitList.map((row) => <Cell key={row.customer} fill={tierColors[row.tier]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div style={cardStyle}>
          <h3 style={{ marginTop: 0 }}>Interactive Customer Volume Model</h3>
          <p style={{ color: '#64748b', marginTop: -4 }}>Bubble size = total sales, Y-axis = average monthly sales, X-axis = active months.</p>
          <ResponsiveContainer width="100%" height={360}>
            <ScatterChart margin={{ top: 20, right: 20, left: 10, bottom: 10 }}>
              <CartesianGrid />
              <XAxis type="number" dataKey="x" name="Active Months" />
              <YAxis type="number" dataKey="y" name="Avg Monthly Sales" tickFormatter={money} width={120} />
              <ZAxis type="number" dataKey="z" range={[70, 600]} />
              <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                formatter={(v, n) => (n === 'y' || n === 'z' ? money(v) : v)}
                labelFormatter={(_, payload) => payload?.[0]?.payload?.name || ''}
              />
              <Scatter data={scatterData}>
                {scatterData.map((row) => <Cell key={row.name} fill={tierColors[row.tier]} />)}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Monthly Revenue Trend by Tier</h3>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={sampleData.tierMonthlyTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" tickFormatter={monthLabel} />
                <YAxis tickFormatter={money} />
                <Tooltip formatter={(v) => money(v)} labelFormatter={monthLabel} />
                {['Strategic', 'Core', 'Growth', 'Long-tail'].map((tier) => (
                  <Line key={tier} type="monotone" dataKey={tier} stroke={tierColors[tier]} strokeWidth={2} dot={false} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Selected Customer Monthly Pattern</h3>
            <select style={{ width: '100%', padding: 8, marginBottom: 10 }} value={selectedCustomer} onChange={(e) => setSelectedCustomer(e.target.value)}>
              {filteredCustomers.map((c) => <option key={c.customer}>{c.customer}</option>)}
            </select>
            <ResponsiveContainer width="100%" height={235}>
              <LineChart data={selectedTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" tickFormatter={monthLabel} />
                <YAxis tickFormatter={money} />
                <Tooltip formatter={(v) => money(v)} labelFormatter={monthLabel} />
                <Line dataKey="sales" stroke="#0f172a" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div style={cardStyle}>
          <h3 style={{ marginTop: 0 }}>Recommended Visit Cadence by Customer</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
              <thead>
                <tr style={{ background: '#f1f5f9' }}>
                  <th style={{ textAlign: 'left', padding: 8 }}>Customer</th>
                  <th style={{ textAlign: 'left', padding: 8 }}>Tier</th>
                  <th style={{ textAlign: 'right', padding: 8 }}>Avg Monthly</th>
                  <th style={{ textAlign: 'right', padding: 8 }}>Total Sales</th>
                  <th style={{ textAlign: 'right', padding: 8 }}>Active Months</th>
                  <th style={{ textAlign: 'left', padding: 8 }}>Visit Frequency</th>
                </tr>
              </thead>
              <tbody>
                {filteredCustomers.map((c) => (
                  <tr key={c.customer} style={{ borderBottom: '1px solid #e2e8f0' }}>
                    <td style={{ padding: 8 }}>{c.customer}</td>
                    <td style={{ padding: 8, color: tierColors[c.tier], fontWeight: 600 }}>{c.tier}</td>
                    <td style={{ padding: 8, textAlign: 'right' }}>{money(c.avgMonthlySales)}</td>
                    <td style={{ padding: 8, textAlign: 'right' }}>{money(c.totalSales)}</td>
                    <td style={{ padding: 8, textAlign: 'right' }}>{c.activeMonths}</td>
                    <td style={{ padding: 8 }}>{c.visitFrequency}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

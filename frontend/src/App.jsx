import React from "react";
import { useEffect, useState } from "react";
import { Activity, AlertTriangle, ShieldCheck, FileText, RefreshCw, Send, Gauge } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

const API = "http://127.0.0.1:8000";
const demo = "Worker entered a confined space without gas test before maintenance.";

export default function App() {
  const [text, setText] = useState(demo);
  const [site, setSite] = useState("Demo Site A");
  const [activity, setActivity] = useState("Maintenance");
  const [type, setType] = useState("Near Miss");
  const [result, setResult] = useState(null);
  const [reports, setReports] = useState([]);
  const [summary, setSummary] = useState({ total_reports: 0, sif_potential: 0, non_sif_potential: 0, average_severity_score: 0 });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      const [s, r] = await Promise.all([
        fetch(`${API}/summary`).then(x => { if (!x.ok) throw new Error("API unavailable"); return x.json(); }),
        fetch(`${API}/reports?limit=20`).then(x => x.json())
      ]);
      setSummary(s);
      setReports(r);
      setError("");
    } catch {
      setError("Cannot reach the backend. Start FastAPI at http://127.0.0.1:8000 and refresh.");
    }
  }

  useEffect(() => { refresh(); }, []);

  async function analyze(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ report_text: text, site, activity, report_type: type })
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail?.[0]?.msg || body.detail || "Could not analyze report");
      setResult(body);
      await refresh();
    } catch (err) {
      setError(err.message || "Unable to analyze report.");
    } finally {
      setBusy(false);
    }
  }

  const chartData = [
    { name: "SIF potential", count: summary.sif_potential },
    { name: "Other reports", count: summary.non_sif_potential }
  ];

  return <div className="app-shell">
    <header className="topbar">
      <div className="brand-mark"><ShieldCheck size={26}/></div>
      <div className="brand"><strong>SIFSense</strong><span>Safety intelligence for proactive HSE review</span></div>
      <div className="team-pill">INFRON · DEMO</div>
    </header>

    <main className="main">
      <section className="hero">
        <div>
          <div className="eyebrow"><Activity size={15}/> SURAKSHIT BHARAT</div>
          <h1>See the signal.<br/><span>Prevent the incident.</span></h1>
          <p>Analyze safety observations and surface possible serious injury and fatality precursors for human review.</p>
        </div>
        <div className="hero-icon"><ShieldCheck size={74}/><span>HSE TRIAGE</span></div>
      </section>

      {error && <div className="error-banner"><AlertTriangle size={18}/>{error}</div>}

      <section className="stats-grid">
        <Stat icon={<FileText/>} label="Reports analyzed" value={summary.total_reports}/>
        <Stat icon={<AlertTriangle/>} label="SIF-potential flags" value={summary.sif_potential}/>
        <Stat icon={<ShieldCheck/>} label="Other reports" value={summary.non_sif_potential}/>
        <Stat icon={<Gauge/>} label="Average heuristic score" value={summary.average_severity_score}/>
      </section>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading"><div><span className="step">01</span><h2>Analyze a safety report</h2></div><span className="live-tag">LOCAL DEMO</span></div>
          <p className="muted">Use synthetic or non-confidential text. The result is a triage aid, not a safety decision.</p>
          <form onSubmit={analyze}>
            <label>Report description<textarea value={text} onChange={e => setText(e.target.value)} minLength={5} maxLength={10000} required placeholder="Describe the unsafe act, unsafe condition, or near miss..."/></label>
            <div className="form-row">
              <label>Site<input value={site} onChange={e => setSite(e.target.value)} maxLength={200}/></label>
              <label>Activity<input value={activity} onChange={e => setActivity(e.target.value)} maxLength={200}/></label>
            </div>
            <label>Report type<select value={type} onChange={e => setType(e.target.value)}>
              <option>Near Miss</option><option>Unsafe Act</option><option>Unsafe Condition</option><option>Incident</option><option>Observation</option>
            </select></label>
            <div className="form-actions">
              <button className="secondary" type="button" onClick={() => {setText(demo); setResult(null);}}>Load example</button>
              <button className="primary" disabled={busy || text.trim().length < 5}>{busy ? <RefreshCw className="spin" size={17}/> : <Send size={17}/>} {busy ? "Analyzing..." : "Analyze report"}</button>
            </div>
          </form>
        </section>

        <section className="panel result-panel">
          <div className="panel-heading"><div><span className="step">02</span><h2>Analysis result</h2></div></div>
          {!result ? <div className="empty-state"><div className="empty-icon"><Activity size={30}/></div><h3>Ready for review</h3><p>Submit a report to see its triage label, heuristic score, matched evidence and rule hints.</p></div> :
            <div className="result-body">
              <div className={`classification ${result.classification === "SIF-Potential" ? "high" : "low"}`}>
                {result.classification === "SIF-Potential" ? <AlertTriangle/> : <ShieldCheck/>}
                <div><small>TRIAGE CLASSIFICATION</small><strong>{result.classification}</strong></div>
                <div className="score"><b>{result.severity_score}</b><small>/100</small></div>
              </div>
              <div className="score-track"><span style={{width: `${result.severity_score}%`}}/></div>
              <h3>Matched precursor evidence <span className="count">{result.evidence.length}</span></h3>
              {result.evidence.length ? <div className="evidence-list">{result.evidence.map((item, i) =>
                <div className="evidence-item" key={`${item.phrase}-${i}`}><div><strong>{item.phrase}</strong><span>{item.category}</span></div><b>+{item.severity_weight}</b></div>
              )}</div> : <p className="muted small">No configured phrase matched. This does not prove that the report is risk-free.</p>}
              <h3>Life-Saving Rule hints</h3>
              <div className="rule-tags">{result.life_saving_rules.length ? result.life_saving_rules.map(rule => <span key={rule}>{rule}</span>) : <span>No rule hint identified</span>}</div>
              <div className="recommendation"><strong>Suggested next step</strong><p>{result.recommendation}</p></div>
              <p className="disclaimer">{result.disclaimer}</p>
            </div>
          }
        </section>
      </div>

      <section className="bottom-grid">
        <section className="panel">
          <div className="panel-heading"><div><span className="step">03</span><h2>Report overview</h2></div><button className="icon-button" onClick={refresh} title="Refresh"><RefreshCw size={16}/></button></div>
          <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{top: 8, right: 8, left: -18, bottom: 4}}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e6edf2"/>
              <XAxis dataKey="name" tick={{fontSize: 11, fill: "#65758b"}} axisLine={false} tickLine={false}/>
              <YAxis allowDecimals={false} tick={{fontSize: 11, fill: "#65758b"}} axisLine={false} tickLine={false}/>
              <Tooltip/>
              <Bar dataKey="count" fill="#16a085" radius={[6,6,0,0]} maxBarSize={54}/>
            </BarChart>
          </ResponsiveContainer></div>
        </section>
        <section className="panel">
          <div className="panel-heading"><div><span className="step">04</span><h2>Recent reports</h2></div><span className="count">{reports.length}</span></div>
          {reports.length === 0 ? <p className="muted">No reports saved yet. Analyze a sample report to get started.</p> :
            <div className="recent-list">{reports.slice(0, 6).map(r => <div className="recent-item" key={r.id}>
              <div className={`mini-dot ${r.classification === "SIF-Potential" ? "red" : "green"}`}/>
              <div className="recent-copy"><strong>{r.site}</strong><span>{r.report_text}</span></div>
              <b className="recent-score">{r.severity_score}</b>
            </div>)}</div>}
        </section>
      </section>
      <footer><span>SIFSense · INFRON</span><span>Prototype for demonstration · Human HSE review required</span></footer>
    </main>
  </div>;
}

function Stat({icon, label, value}) {
  return <div className="stat-card"><div className="stat-icon">{icon}</div><div><span>{label}</span><strong>{value}</strong></div></div>;
}

import { useEffect, useState } from "react";
import { fetchDashboard, triggerTask } from "./api";
import type { DashboardResponse } from "./types";

const EMPTY_STATE: DashboardResponse = {
  metrics: [],
  pipeline: [],
  products: [],
  activity: [],
  exceptions: [],
};

export default function App() {
  const [dashboard, setDashboard] = useState<DashboardResponse>(EMPTY_STATE);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTask, setActiveTask] = useState<string | null>(null);

  async function loadDashboard() {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchDashboard();
      setDashboard(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function handleTrigger(task: "trend-radar" | "price-engine" | "douyin-intel" | "analytics-brain") {
    try {
      setActiveTask(task);
      await triggerTask(task);
      await loadDashboard();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Trigger failed");
    } finally {
      setActiveTask(null);
    }
  }

  return (
    <div className="shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />
      <header className="hero">
        <div>
          <p className="eyebrow">AutoDrop Command Center</p>
          <h1>Run 500 product experiments a week from one screen.</h1>
          <p className="subcopy">
            Trend radar, Chinese factory intelligence, AI influencer content, pricing, routing, and
            exception handling in one autonomous control room.
          </p>
        </div>
        <div className="hero-actions">
          <button onClick={() => handleTrigger("trend-radar")} disabled={activeTask !== null}>
            {activeTask === "trend-radar" ? "Running..." : "Run Trend Radar"}
          </button>
          <button onClick={() => handleTrigger("douyin-intel")} disabled={activeTask !== null} className="secondary">
            {activeTask === "douyin-intel" ? "Scanning..." : "Scan Douyin Intel"}
          </button>
          <button onClick={() => handleTrigger("analytics-brain")} disabled={activeTask !== null} className="ghost">
            {activeTask === "analytics-brain" ? "Analyzing..." : "Nightly Analytics"}
          </button>
        </div>
      </header>

      {error ? <div className="banner error">{error}</div> : null}
      {loading ? <div className="banner">Loading AutoDrop systems...</div> : null}

      <section className="metrics-grid">
        {dashboard.metrics.map((metric) => (
          <article className={`metric-card tone-${metric.tone}`} key={metric.title}>
            <span>{metric.title}</span>
            <strong>{metric.value}</strong>
            <small>{metric.delta}</small>
          </article>
        ))}
      </section>

      <section className="pipeline-card">
        <div className="section-head">
          <div>
            <p className="eyebrow">Autonomy Pipeline</p>
            <h2>Signal to shipment in five automated stages</h2>
          </div>
          <button onClick={() => handleTrigger("price-engine")} disabled={activeTask !== null} className="secondary">
            {activeTask === "price-engine" ? "Repricing..." : "Run Price Engine"}
          </button>
        </div>
        <div className="pipeline-grid">
          {dashboard.pipeline.map((stage) => (
            <article className="pipeline-stage" key={stage.name}>
              <span className="count">{stage.count}</span>
              <h3>{stage.name}</h3>
              <p>{stage.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="content-grid">
        <article className="glass-panel">
          <div className="section-head">
            <div>
              <p className="eyebrow">Live Test Queue</p>
              <h2>Products moving through the robot stack</h2>
            </div>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Source</th>
                  <th>Margin</th>
                  <th>Status</th>
                  <th>Channels</th>
                  <th>Factory hint</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.products.map((product) => (
                  <tr key={product.id}>
                    <td>
                      <strong>{product.product_name}</strong>
                    </td>
                    <td>{product.source}</td>
                    <td>{Math.round(product.margin * 100)}%</td>
                    <td>
                      <span className={`pill status-${product.status}`}>{product.status}</span>
                    </td>
                    <td>{product.channels.join(", ")}</td>
                    <td>
                      {product.factory_hint
                        ? `${product.factory_hint.city} · ${product.factory_hint.category} · ${product.factory_hint.factory_count}`
                        : "None"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <div className="side-stack">
          <article className="glass-panel">
            <div className="section-head">
              <div>
                <p className="eyebrow">Robot Activity</p>
                <h2>What the agents did while you slept</h2>
              </div>
            </div>
            <div className="feed">
              {dashboard.activity.map((item, index) => (
                <div className="feed-item" key={`${item.robot_name}-${index}`}>
                  <div className={`dot dot-${item.status}`} />
                  <div>
                    <strong>{item.robot_name}</strong>
                    <p>{item.message}</p>
                  </div>
                </div>
              ))}
            </div>
          </article>

          <article className="glass-panel">
            <div className="section-head">
              <div>
                <p className="eyebrow">Exceptions</p>
                <h2>10-minute human review queue</h2>
              </div>
            </div>
            <div className="exceptions">
              {dashboard.exceptions.map((item) => (
                <div className="exception-row" key={item.id}>
                  <div>
                    <strong>{item.type}</strong>
                    <p>{item.description}</p>
                  </div>
                  <span className={`pill severity-${item.severity}`}>{item.severity}</span>
                </div>
              ))}
            </div>
          </article>
        </div>
      </section>
    </div>
  );
}


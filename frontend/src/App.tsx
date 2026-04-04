import { useEffect, useMemo, useState } from "react";
import { checkoutProduct, fetchDashboard, fetchStorefront, runDemo, triggerTask } from "./api";
import type { CheckoutResponse, DashboardResponse, StorefrontResponse } from "./types";

const FALLBACK_DASHBOARD: DashboardResponse = {
  metrics: [
    { title: "Revenue", value: "$3,847", delta: "+23% vs yesterday", tone: "good" },
    { title: "Products Testing", value: "512", delta: "47 added today", tone: "warn" },
    { title: "Winners Found", value: "11", delta: "2.1% hit rate", tone: "neutral" },
    { title: "Avg Margin", value: "38%", delta: "-2% this week", tone: "warn" },
  ],
  pipeline: [
    { name: "Trending", count: 247, detail: "TikTok, Instagram, Amazon, Douyin, Google" },
    { name: "Scouting", count: 83, detail: "Supplier match, 1688 checks, margin filter" },
    { name: "Listing", count: 41, detail: "Channel copy, mockups, AI influencer briefs" },
    { name: "Published", count: 489, detail: "Shopify, TikTok Shop, Amazon, Etsy" },
    { name: "Winners", count: 11, detail: "Budget doubled, losers killed, alerts sent" },
  ],
  products: [
    {
      id: 1,
      product_name: "Rechargeable Neck Fan",
      source: "tiktok",
      margin: 0.24,
      status: "winner",
      channels: ["shopify", "tiktok_shop", "instagram"],
      factory_hint: { city: "深圳", category: "electronics", factory_count: 140 },
      created_at: new Date().toISOString(),
    },
  ],
  activity: [
    {
      robot_name: "Trend Radar",
      message: "TikTok and Instagram found a cooling device trend worth shipping today.",
      status: "success",
      created_at: new Date().toISOString(),
    },
  ],
  exceptions: [],
};

const FALLBACK_STOREFRONT: StorefrontResponse = {
  hero_product: {
    id: 1,
    product_name: "Rechargeable Neck Fan",
    source: "tiktok",
    status: "winner",
    price: 34,
    compare_at_price: 49,
    margin: 0.24,
    channels: ["shopify", "instagram", "tiktok_shop"],
    factory_hint: { city: "深圳", category: "electronics", factory_count: 140 },
    badge: "Trending",
    subtitle: "Spotted on TikTok Shop cool devices · Fulfilled by Spocket",
    image_tone: "mint",
  },
  products: [
    {
      id: 1,
      product_name: "Rechargeable Neck Fan",
      source: "tiktok",
      status: "winner",
      price: 34,
      compare_at_price: 49,
      margin: 0.24,
      channels: ["shopify", "instagram", "tiktok_shop"],
      factory_hint: { city: "深圳", category: "electronics", factory_count: 140 },
      badge: "Trending",
      subtitle: "Spotted on TikTok Shop cool devices · Fulfilled by Spocket",
      image_tone: "mint",
    },
  ],
  total_products: 1,
  updated_label: "Preview data loaded",
};

const INFLUENCER_CARDS = [
  { platform: "TikTok", handle: "@nova.ai", title: "Rechargeable Neck Fan test in real heat", stats: "2.3M views · 187K likes · 4.2K comments", theme: "obsidian" },
  { platform: "Instagram", handle: "@lux.styled", title: "Cooling gadget reel for summer commuters", stats: "1.1M views · 94K likes · 2.1K saves", theme: "forest" },
  { platform: "YouTube Shorts", handle: "@vida.finds", title: "Best practical under-$35 buy this week", stats: "840K views · 61K likes · 3.8K comments", theme: "mahogany" },
];

const FACTORY_CARDS = [
  { cityCn: "义乌", city: "Yiwu, Zhejiang", detail: "Small goods, accessories, toys", count: "4,200+ factories verified" },
  { cityCn: "莆田", city: "Putian, Fujian", detail: "Shoes, sneakers, sportswear", count: "1,800+ factories verified" },
  { cityCn: "深圳", city: "Shenzhen, Guangdong", detail: "Electronics, gadgets, cables", count: "6,100+ factories verified" },
  { cityCn: "汕头", city: "Shantou, Guangdong", detail: "Toys, plastics, stationery", count: "2,900+ factories verified" },
];

type ViewMode = "owner" | "storefront";
type TriggerTask = "trend-radar" | "price-engine" | "douyin-intel" | "analytics-brain" | "listing-pipeline" | "ops-loop";

export default function App() {
  const [dashboard, setDashboard] = useState<DashboardResponse>(FALLBACK_DASHBOARD);
  const [storefront, setStorefront] = useState<StorefrontResponse>(FALLBACK_STOREFRONT);
  const [loading, setLoading] = useState(true);
  const [activeTask, setActiveTask] = useState<string | null>(null);
  const [mode, setMode] = useState<ViewMode>("owner");
  const [usingPreviewData, setUsingPreviewData] = useState(false);
  const [checkoutState, setCheckoutState] = useState<CheckoutResponse | null>(null);

  async function loadData() {
    try {
      setLoading(true);
      const [dashboardData, storefrontData] = await Promise.all([fetchDashboard(), fetchStorefront()]);
      setDashboard(dashboardData);
      setStorefront(storefrontData);
      setUsingPreviewData(false);
    } catch {
      setDashboard(FALLBACK_DASHBOARD);
      setStorefront(FALLBACK_STOREFRONT);
      setUsingPreviewData(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleTrigger(task: TriggerTask) {
    try {
      setActiveTask(task);
      await triggerTask(task);
      await loadData();
    } catch {
      setUsingPreviewData(true);
    } finally {
      setActiveTask(null);
    }
  }

  async function handleRunDemo() {
    try {
      setActiveTask("demo-run-all");
      await runDemo();
      await loadData();
    } catch {
      setUsingPreviewData(true);
    } finally {
      setActiveTask(null);
    }
  }

  async function handleCheckout(productId: number) {
    try {
      setActiveTask(`checkout-${productId}`);
      const result = await checkoutProduct(productId);
      setCheckoutState(result);
      await loadData();
      setMode("owner");
    } catch {
      setCheckoutState(null);
    } finally {
      setActiveTask(null);
    }
  }

  const headerMetrics = useMemo(
    () => [
      { label: "revenue today", value: dashboard.metrics[0]?.value ?? "$0", tone: "" },
      { label: "orders", value: String(dashboard.pipeline[3]?.count ?? 0), tone: "" },
      { label: "products live", value: String(storefront.total_products), tone: "gold" },
      { label: "exceptions", value: String(dashboard.exceptions.length), tone: "red" },
    ],
    [dashboard, storefront],
  );

  return (
    <div className={mode === "owner" ? "owner-page" : "storefront-page"}>
      <div className="mode-switch">
        <button className={mode === "owner" ? "mode-pill active" : "mode-pill"} onClick={() => setMode("owner")}>
          Owner UI
        </button>
        <button className={mode === "storefront" ? "mode-pill active" : "mode-pill"} onClick={() => setMode("storefront")}>
          Customer UI
        </button>
      </div>

      {mode === "owner" ? (
        <div className="owner-shell">
          <header className="owner-header">
            <div className="owner-logo">
              <span className="logo-dot" />
              AutoDrop
              <span className="owner-logo-sub">command center</span>
            </div>
            <div className="owner-header-stats">
              {headerMetrics.map((item) => (
                <div key={item.label} className="owner-hstat">
                  <span className="owner-hstat-label">{item.label}</span>
                  <span className={`owner-hstat-value ${item.tone}`}>{item.value}</span>
                </div>
              ))}
            </div>
            <div className="owner-status-pill">
              <span className="status-dot" />
              {usingPreviewData ? "Preview mode active" : "Local demo mode ready"}
            </div>
          </header>

          <div className="owner-body">
            <aside className="owner-sidebar">
              <div className="nav-block">
                <div className="nav-label">Overview</div>
                <div className="nav-item active">Dashboard</div>
                <div className="nav-item">Analytics</div>
              </div>
              <div className="nav-block">
                <div className="nav-label">Robots</div>
                <div className="nav-item">Trend Radar <span className="nav-badge green">ON</span></div>
                <div className="nav-item">Product Scout <span className="nav-badge green">ON</span></div>
                <div className="nav-item">Listing Factory <span className="nav-badge green">ON</span></div>
                <div className="nav-item">Influencer Factory <span className="nav-badge green">ON</span></div>
                <div className="nav-item">Price Engine <span className="nav-badge green">ON</span></div>
                <div className="nav-item">Order Router <span className="nav-badge green">ON</span></div>
                <div className="nav-item">CS Bot <span className="nav-badge green">ON</span></div>
              </div>
              <div className="nav-block">
                <div className="nav-label">Channels</div>
                <div className="nav-item">TikTok Shop</div>
                <div className="nav-item">Shopify</div>
                <div className="nav-item">Instagram</div>
                <div className="nav-item">YouTube</div>
              </div>
            </aside>

            <main className="owner-main">
              {usingPreviewData ? <div className="owner-banner">Backend not reachable, so the app is showing preview data.</div> : null}
              {checkoutState ? (
                <div className="owner-banner success">
                  Sale confirmed: order #{checkoutState.order_id} for {checkoutState.product_name} at $
                  {checkoutState.revenue.toFixed(2)}. Tracking {checkoutState.tracking_number ?? "pending"}.
                </div>
              ) : null}
              {loading ? <div className="owner-banner">Refreshing command center data...</div> : null}

              <section>
                <div className="section-head">
                  <div className="section-title">Demo control room</div>
                  <div className="section-actions">
                    <button onClick={handleRunDemo} disabled={activeTask !== null} className="owner-btn">
                      {activeTask === "demo-run-all" ? "Running..." : "Launch Demo Loop"}
                    </button>
                    <button onClick={() => handleTrigger("trend-radar")} disabled={activeTask !== null} className="owner-btn ghost">
                      {activeTask === "trend-radar" ? "Running..." : "Run Radar"}
                    </button>
                    <button onClick={() => handleTrigger("douyin-intel")} disabled={activeTask !== null} className="owner-btn ghost">
                      {activeTask === "douyin-intel" ? "Scanning..." : "Douyin Intel"}
                    </button>
                  </div>
                </div>
                <div className="metric-grid">
                  {dashboard.metrics.map((metric) => (
                    <article className={`owner-metric-card tone-${metric.tone}`} key={metric.title}>
                      <div className="metric-label">{metric.title}</div>
                      <div className="metric-value">{metric.value}</div>
                      <div className="metric-sub">{metric.delta}</div>
                    </article>
                  ))}
                </div>
              </section>

              <section>
                <div className="section-head">
                  <div className="section-title">Product pipeline</div>
                  <div className="section-actions">
                    <button onClick={() => handleTrigger("listing-pipeline")} disabled={activeTask !== null} className="owner-btn ghost">
                      {activeTask === "listing-pipeline" ? "Publishing..." : "Publish Products"}
                    </button>
                    <button onClick={() => handleTrigger("price-engine")} disabled={activeTask !== null} className="owner-btn ghost">
                      {activeTask === "price-engine" ? "Repricing..." : "Price Engine"}
                    </button>
                    <button onClick={() => handleTrigger("analytics-brain")} disabled={activeTask !== null} className="owner-btn ghost">
                      {activeTask === "analytics-brain" ? "Analyzing..." : "Analytics"}
                    </button>
                  </div>
                </div>
                <div className="pipeline-grid-ops">
                  {dashboard.pipeline.map((stage) => (
                    <div className="pipe-col" key={stage.name}>
                      <div className="pipe-header">
                        <div className="pipe-title">{stage.name}</div>
                        <div className="pipe-count">{stage.count}</div>
                      </div>
                      <div className="pipe-item">
                        <div className="pipe-item-name">{stage.detail}</div>
                        <div className="pipe-item-meta">AutoDrop robot lane</div>
                        <div className="pipe-item-score score-high">active</div>
                      </div>
                      {dashboard.products.slice(0, 2).map((product) => (
                        <div className="pipe-item" key={`${stage.name}-${product.id}`}>
                          <div className="pipe-item-name">{product.product_name}</div>
                          <div className="pipe-item-meta">{product.source} · {Math.round(product.margin * 100)}% margin</div>
                          <div className={`pipe-item-score status-${product.status}`}>{product.status}</div>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              </section>

              <section>
                <div className="section-head">
                  <div className="section-title">Live catalog</div>
                  <div className="section-actions">
                    <button onClick={() => setMode("storefront")} className="owner-btn ghost">Open Storefront</button>
                  </div>
                </div>
                <div className="owner-table-wrap">
                  <div className="owner-table-head">
                    <div>Product</div>
                    <div>Source</div>
                    <div>Margin</div>
                    <div>Status</div>
                    <div>Channels</div>
                    <div>Factory hint</div>
                  </div>
                  {dashboard.products.map((product) => (
                    <div className="owner-table-row" key={product.id}>
                      <div className="owner-cell name">{product.product_name}</div>
                      <div className="owner-cell">{product.source}</div>
                      <div className="owner-cell green">{Math.round(product.margin * 100)}%</div>
                      <div className="owner-cell">
                        <span className={`status-badge badge-${product.status}`}>{product.status}</span>
                      </div>
                      <div className="owner-cell">
                        {product.channels.map((channel) => (
                          <span className="channel-tag" key={channel}>{channel}</span>
                        ))}
                      </div>
                      <div className="owner-cell">
                        {product.factory_hint ? `${product.factory_hint.city} · ${product.factory_hint.category}` : "No factory hint"}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </main>

            <aside className="owner-right">
              <section className="panel-section">
                <div className="panel-title">Robot activity</div>
                {dashboard.activity.map((item, index) => (
                  <div className="activity-item" key={`${item.robot_name}-${index}`}>
                    <div className={`activity-icon ai-${item.status === "warning" ? "gold" : item.status === "running" ? "purple" : "green"}`}>◎</div>
                    <div>
                      <div className="activity-text">
                        <span className="activity-highlight">{item.robot_name}</span> {item.message}
                      </div>
                      <div className="activity-time">{new Date(item.created_at).toLocaleTimeString()}</div>
                    </div>
                  </div>
                ))}
              </section>

              <section className="panel-section">
                <div className="panel-title">Video demo script</div>
                <div className="activity-text">1. Run demo loop. 2. Open storefront. 3. Buy demo product. 4. Switch back and show revenue + routing.</div>
              </section>

              <section className="panel-section">
                <div className="panel-title">Exceptions</div>
                {dashboard.exceptions.length === 0 ? (
                  <div className="activity-text">No blocking exceptions in local demo mode.</div>
                ) : (
                  dashboard.exceptions.map((item) => (
                    <div className={`alert ${item.severity === "high" ? "alert-danger" : "alert-warn"}`} key={item.id}>
                      <div className="alert-icon">{item.severity === "high" ? "!" : "•"}</div>
                      <div className="alert-text">{item.description}</div>
                    </div>
                  ))
                )}
              </section>
            </aside>
          </div>
        </div>
      ) : (
        <div className="store-shell">
          <div className="store-topbar">Free shipping on orders over $35 · Ships from verified factory clusters in China</div>
          <header className="store-header">
            <div className="store-logo">Drifty</div>
            <nav className="store-nav">
              <a>Trending</a>
              <a>Cooling</a>
              <a>Home</a>
              <a>Beauty</a>
              <a>Tech</a>
            </nav>
            <div className="store-actions">
              <button className="icon-bubble">{checkoutState ? "1" : "0"}</button>
              <button className="signin-btn" onClick={() => setMode("owner")}>Back to HQ</button>
            </div>
          </header>

          <section className="store-hero">
            <div className="store-hero-copy">
              <p className="store-kicker">AI-curated · sourced direct from factory</p>
              <h1>{storefront.hero_product?.product_name ?? "Products going viral right now"}</h1>
              <p>{storefront.hero_product?.subtitle ?? "We watch TikTok, Instagram, and Chinese factory districts so you don't have to."}</p>
              <div className="store-cta-row">
                <button className="store-btn primary" onClick={() => storefront.hero_product && handleCheckout(storefront.hero_product.id)}>
                  {activeTask === `checkout-${storefront.hero_product?.id}` ? "Processing..." : "Buy demo product"}
                </button>
                <button className="store-btn">{storefront.updated_label}</button>
              </div>
            </div>
            <div className="store-hero-media">
              <div className="creator-card tall">
                <div className="media-placeholder" />
                <div className="creator-tag">{storefront.hero_product?.badge ?? "Trending"} · ready to sell</div>
              </div>
              <div className="creator-card">
                <div className="media-placeholder" />
                <div className="creator-tag">{storefront.hero_product?.source ?? "tiktok"} · factory direct</div>
              </div>
            </div>
          </section>

          {checkoutState ? (
            <section className="store-section">
              <div className="checkout-banner">
                Order #{checkoutState.order_id} confirmed for {checkoutState.product_name}. Tracking {checkoutState.tracking_number ?? "pending"}.
              </div>
            </section>
          ) : null}

          <section className="source-strip">
            <div className="source-label">Sourced from</div>
            {["TikTok", "Instagram", "Amazon", "TikTok Shop", "抖音", "Temu"].map((item, index) => (
              <span className={`source-pill ${index < 2 ? "active" : ""}`} key={item}>{item}</span>
            ))}
            <span className="source-refresh">Updated every 30 min</span>
          </section>

          <section className="store-section">
            <div className="store-section-head">
              <h2>Trending this week</h2>
              <a>See all {storefront.total_products} products</a>
            </div>
            <div className="product-grid">
              {storefront.products.map((product) => (
                <article className="product-card" key={product.id}>
                  <div className={`product-media ${product.image_tone}`}>
                    <span className="product-tag">{product.badge}</span>
                    <div className="media-placeholder" />
                  </div>
                  <div className="product-body">
                    <div className="product-name">{product.product_name}</div>
                    <div className="product-rating">★★★★★ {product.subtitle}</div>
                    <div className="product-price-row">
                      <div>
                        <strong>${product.price.toFixed(2)}</strong> <span>{product.compare_at_price ? `$${product.compare_at_price.toFixed(2)}` : ""}</span>
                      </div>
                      <button className="add-btn" onClick={() => handleCheckout(product.id)}>
                        {activeTask === `checkout-${product.id}` ? "..." : "+"}
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="store-section">
            <div className="store-section-head">
              <div>
                <p className="store-kicker green">AI influencer content</p>
                <h2>See it in action</h2>
              </div>
              <a>View all content</a>
            </div>
            <div className="influencer-grid">
              {INFLUENCER_CARDS.map((card) => (
                <article className="influencer-card" key={card.handle}>
                  <div className={`influencer-video ${card.theme}`}>
                    <span className="platform-chip">{card.platform.slice(0, 2).toUpperCase()}</span>
                    <div className="play-button">▶</div>
                    <div className="creator-footer">{card.handle}</div>
                  </div>
                  <div className="influencer-body">
                    <div className="store-kicker">{`AI influencer · ${card.platform}`}</div>
                    <h3>{card.title}</h3>
                    <p>{card.stats}</p>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="store-section spotlight">
            <div className="store-section-head">
              <div>
                <p className="store-kicker green">Direct from source</p>
                <h2>Factory district spotlight</h2>
              </div>
            </div>
            <div className="factory-grid">
              {FACTORY_CARDS.map((card) => (
                <article className="factory-card" key={card.city}>
                  <div className="factory-cn">{card.cityCn}</div>
                  <h3>{card.city}</h3>
                  <p>{card.detail}</p>
                  <span>{card.count}</span>
                </article>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

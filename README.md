<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Amazon Price Analytics Pipeline</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg: #0a0a0f;
      --surface: #111118;
      --surface2: #17171f;
      --border: #2a2a3a;
      --accent: #ff6b2b;
      --accent2: #f7c948;
      --accent3: #4ade80;
      --text: #e8e8f0;
      --muted: #6b6b85;
      --mono: 'Space Mono', monospace;
      --sans: 'Syne', sans-serif;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { scroll-behavior: smooth; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      line-height: 1.7;
      overflow-x: hidden;
    }

    /* Animated grid bg */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,107,43,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,107,43,0.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    .page-wrap {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 24px 80px;
      position: relative;
      z-index: 1;
    }

    /* ── HERO ── */
    .hero {
      padding: 80px 0 60px;
      border-bottom: 1px solid var(--border);
      position: relative;
    }

    .hero-tag {
      display: inline-block;
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--accent);
      border: 1px solid var(--accent);
      padding: 4px 12px;
      margin-bottom: 28px;
      animation: fadeUp 0.6s ease both;
    }

    .hero h1 {
      font-size: clamp(2.2rem, 6vw, 3.8rem);
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -1px;
      animation: fadeUp 0.6s 0.1s ease both;
    }

    .hero h1 span {
      color: var(--accent);
      position: relative;
    }

    .hero-sub {
      margin-top: 18px;
      color: var(--muted);
      font-size: 1rem;
      max-width: 560px;
      animation: fadeUp 0.6s 0.2s ease both;
    }

    .hero-meta {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 28px;
      animation: fadeUp 0.6s 0.3s ease both;
    }

    .badge {
      font-family: var(--mono);
      font-size: 11px;
      padding: 5px 12px;
      border-radius: 2px;
      letter-spacing: 1px;
      font-weight: 700;
    }

    .badge-orange { background: rgba(255,107,43,0.15); color: var(--accent); border: 1px solid rgba(255,107,43,0.3); }
    .badge-yellow { background: rgba(247,201,72,0.12); color: var(--accent2); border: 1px solid rgba(247,201,72,0.25); }
    .badge-green  { background: rgba(74,222,128,0.12); color: var(--accent3); border: 1px solid rgba(74,222,128,0.25); }

    /* ── SECTIONS ── */
    section {
      padding: 56px 0 0;
      animation: fadeUp 0.5s ease both;
    }

    .section-label {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .section-label::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    h2 {
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 24px;
    }

    /* ── FEATURE GRID ── */
    .feature-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1px;
      background: var(--border);
      border: 1px solid var(--border);
    }

    .feature-card {
      background: var(--surface);
      padding: 24px;
      transition: background 0.2s;
    }

    .feature-card:hover { background: var(--surface2); }

    .feature-icon {
      font-size: 1.5rem;
      margin-bottom: 10px;
    }

    .feature-card h3 {
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 6px;
      letter-spacing: 0.2px;
    }

    .feature-card p {
      font-size: 0.8rem;
      color: var(--muted);
      font-family: var(--mono);
      line-height: 1.5;
    }

    /* ── PIPELINE ── */
    .pipeline {
      display: flex;
      align-items: stretch;
      gap: 0;
      overflow-x: auto;
      padding-bottom: 8px;
    }

    .pipeline-step {
      flex: 1;
      min-width: 120px;
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 20px 16px;
      position: relative;
      transition: border-color 0.2s, transform 0.2s;
    }

    .pipeline-step:hover {
      border-color: var(--accent);
      transform: translateY(-3px);
      z-index: 2;
    }

    .pipeline-step:not(:last-child)::after {
      content: '→';
      position: absolute;
      right: -14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--accent);
      font-family: var(--mono);
      font-size: 1.1rem;
      z-index: 3;
      background: var(--bg);
      padding: 2px 2px;
    }

    .step-num {
      font-family: var(--mono);
      font-size: 10px;
      color: var(--accent);
      letter-spacing: 2px;
      margin-bottom: 8px;
    }

    .pipeline-step h3 {
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 8px;
    }

    .step-tags {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .step-tag {
      font-family: var(--mono);
      font-size: 9px;
      color: var(--muted);
      padding: 2px 0;
      border-left: 2px solid var(--border);
      padding-left: 8px;
      line-height: 1.4;
    }

    /* ── TECH STACK ── */
    .tech-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 12px;
    }

    .tech-item {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 16px;
      text-align: center;
      transition: border-color 0.2s, background 0.2s;
      cursor: default;
    }

    .tech-item:hover {
      border-color: var(--accent2);
      background: var(--surface2);
    }

    .tech-item .ti {
      font-size: 1.6rem;
      display: block;
      margin-bottom: 6px;
    }

    .tech-item span {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 1px;
    }

    /* ── CODE BLOCK ── */
    .code-block {
      background: #0d0d14;
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      padding: 20px 24px;
      font-family: var(--mono);
      font-size: 12px;
      color: #a0a0c0;
      overflow-x: auto;
      line-height: 1.8;
    }

    .code-block .kw { color: var(--accent); }
    .code-block .str { color: var(--accent2); }
    .code-block .cmt { color: #444460; font-style: italic; }
    .code-block .fn { color: var(--accent3); }

    /* ── FILE STRUCTURE ── */
    .file-tree {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 24px;
      font-family: var(--mono);
      font-size: 12px;
      line-height: 2;
    }

    .ft-dir { color: var(--accent2); font-weight: 700; }
    .ft-file { color: var(--muted); }
    .ft-file.highlight { color: var(--accent3); }
    .ft-indent { padding-left: 20px; display: block; }

    /* ── FUTURE ── */
    .future-list {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .future-item {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 16px 20px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-size: 0.88rem;
      transition: border-color 0.2s;
    }

    .future-item:hover { border-color: var(--accent3); }

    .future-item .fi-icon {
      color: var(--accent3);
      font-size: 1.1rem;
      margin-top: 1px;
    }

    .future-item strong {
      display: block;
      margin-bottom: 3px;
      font-size: 0.85rem;
    }

    .future-item p {
      font-family: var(--mono);
      font-size: 10px;
      color: var(--muted);
    }

    /* ── AUTHOR ── */
    .author-card {
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 32px;
      display: flex;
      align-items: center;
      gap: 24px;
      margin-top: 56px;
    }

    .author-avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      font-weight: 800;
      color: #0a0a0f;
      flex-shrink: 0;
    }

    .author-card h3 {
      font-size: 1.1rem;
      font-weight: 700;
    }

    .author-card p {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      margin-top: 4px;
    }

    /* ── KEYFRAMES ── */
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* ── DIVIDER ── */
    .divider {
      height: 1px;
      background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
      margin: 56px 0 0;
      opacity: 0.3;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 600px) {
      .pipeline { flex-direction: column; }
      .pipeline-step:not(:last-child)::after { content: '↓'; right: 50%; bottom: -16px; top: auto; transform: translateX(50%); }
      .future-list { grid-template-columns: 1fr; }
      .author-card { flex-direction: column; text-align: center; }
    }

    /* ── SCROLL INDICATOR ── */
    .scroll-bar {
      position: fixed;
      top: 0;
      left: 0;
      height: 2px;
      background: var(--accent);
      z-index: 100;
      transition: width 0.1s;
    }
  </style>
</head>
<body>

<div class="scroll-bar" id="scrollBar"></div>

<div class="page-wrap">

  <!-- HERO -->
  <header class="hero">
    <div class="hero-tag">🛒 Project Documentation</div>
    <h1>Amazon Price<br/><span>Analytics Pipeline</span></h1>
    <p class="hero-sub">An end-to-end ETL pipeline that ingests, cleans, enriches, and visualises Amazon product pricing data — with PCA-based anomaly detection built in.</p>
    <div class="hero-meta">
      <span class="badge badge-orange">Python 🐍</span>
      <span class="badge badge-yellow">Scikit-learn</span>
      <span class="badge badge-green">MySQL</span>
      <span class="badge badge-orange">Pandas + NumPy</span>
      <span class="badge badge-yellow">Matplotlib</span>
    </div>
  </header>

  <!-- FEATURES -->
  <section>
    <div class="section-label">01 — Features</div>
    <h2>What It Does</h2>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">📥</div>
        <h3>Multi-file CSV Ingestion</h3>
        <p>Reads multiple CSV datasets with automatic source tracking per file.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🧹</div>
        <h3>Data Cleaning</h3>
        <p>Strips ₹ symbols, handles nulls, removes duplicates, and timestamps ingestion.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <h3>Feature Engineering</h3>
        <p>Derives price change, discount amount, and discount percentage columns.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>PCA Anomaly Detection</h3>
        <p>Reduces dimensions and flags outliers beyond 2× standard deviation.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Rich Visualisations</h3>
        <p>Histograms, scatter plots, bar & pie charts generated via Matplotlib.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🗄️</div>
        <h3>MySQL Integration</h3>
        <p>Auto-creates table and loads processed gold-layer data into the database.</p>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- PIPELINE -->
  <section>
    <div class="section-label">02 — Architecture</div>
    <h2>Pipeline Stages</h2>
    <div class="pipeline">
      <div class="pipeline-step">
        <div class="step-num">STEP 01</div>
        <h3>Extract</h3>
        <div class="step-tags">
          <span class="step-tag">Read CSV files</span>
          <span class="step-tag">source_file tracking</span>
          <span class="step-tag">Multi-dataset merge</span>
        </div>
      </div>
      <div class="pipeline-step">
        <div class="step-num">STEP 02</div>
        <h3>Transform</h3>
        <div class="step-tags">
          <span class="step-tag">Strip ₹ & commas</span>
          <span class="step-tag">Null handling</span>
          <span class="step-tag">Deduplication</span>
          <span class="step-tag">Timestamp</span>
        </div>
      </div>
      <div class="pipeline-step">
        <div class="step-num">STEP 03</div>
        <h3>Gold Layer</h3>
        <div class="step-tags">
          <span class="step-tag">price_change</span>
          <span class="step-tag">discount_percent</span>
          <span class="step-tag">PCA scoring</span>
          <span class="step-tag">Anomaly removal</span>
        </div>
      </div>
      <div class="pipeline-step">
        <div class="step-num">STEP 04</div>
        <h3>Load</h3>
        <div class="step-tags">
          <span class="step-tag">MySQL write</span>
          <span class="step-tag">Auto-create table</span>
          <span class="step-tag">CSV export</span>
        </div>
      </div>
      <div class="pipeline-step">
        <div class="step-num">STEP 05</div>
        <h3>Visualise</h3>
        <div class="step-tags">
          <span class="step-tag">Histogram</span>
          <span class="step-tag">Scatter plot</span>
          <span class="step-tag">Bar & Pie chart</span>
          <span class="step-tag">PCA chart</span>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- PCA LOGIC -->
  <section>
    <div class="section-label">03 — Anomaly Detection</div>
    <h2>PCA Logic</h2>
    <div class="code-block">
<span class="cmt"># Input features fed into PCA</span>
features = [<span class="str">'min_price'</span>, <span class="str">'current_price'</span>, <span class="str">'price_change'</span>]

<span class="cmt"># Standardise → reduce to 1 component → score</span>
scaler  = <span class="fn">StandardScaler</span>()
pca     = <span class="fn">PCA</span>(n_components=<span class="str">1</span>)
X_scaled       = scaler.<span class="fn">fit_transform</span>(df[features])
df[<span class="str">'pca_score'</span>] = pca.<span class="fn">fit_transform</span>(X_scaled)

<span class="cmt"># Remove outliers beyond 2 std deviations</span>
threshold = <span class="str">2</span> * df[<span class="str">'pca_score'</span>].<span class="fn">std</span>()
df_clean  = df[df[<span class="str">'pca_score'</span>].<span class="fn">abs</span>() &lt;= threshold]
    </div>
  </section>

  <div class="divider"></div>

  <!-- TECH STACK -->
  <section>
    <div class="section-label">04 — Tech Stack</div>
    <h2>Tools & Libraries</h2>
    <div class="tech-grid">
      <div class="tech-item"><span class="ti">🐍</span><span>Python</span></div>
      <div class="tech-item"><span class="ti">🐼</span><span>Pandas</span></div>
      <div class="tech-item"><span class="ti">🔢</span><span>NumPy</span></div>
      <div class="tech-item"><span class="ti">🤖</span><span>Scikit-learn</span></div>
      <div class="tech-item"><span class="ti">📊</span><span>Matplotlib</span></div>
      <div class="tech-item"><span class="ti">🗄️</span><span>MySQL</span></div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- FILE STRUCTURE -->
  <section>
    <div class="section-label">05 — Project Structure</div>
    <h2>Directory Layout</h2>
    <div class="file-tree">
      <span class="ft-dir">amazon_pipeline/</span>
      <span class="ft-indent">│</span>
      <span class="ft-indent"><span class="ft-dir">├── data/</span>               <span class="ft-file">← Input CSV files</span></span>
      <span class="ft-indent">│</span>
      <span class="ft-indent"><span class="ft-file highlight">├── Perfect_deals.csv</span>  <span class="ft-file">← Output: filtered deals</span></span>
      <span class="ft-indent"><span class="ft-file highlight">├── pipeline.py</span>        <span class="ft-file">← Main pipeline script</span></span>
      <span class="ft-indent"><span class="ft-file">└── README.md</span></span>
    </div>
  </section>

  <div class="divider"></div>

  <!-- HOW TO RUN -->
  <section>
    <div class="section-label">06 — Quick Start</div>
    <h2>How to Run</h2>
    <div class="code-block">
<span class="cmt"># 1. Install dependencies</span>
pip install pandas numpy matplotlib scikit-learn mysql-connector-python

<span class="cmt"># 2. Launch the pipeline</span>
python pipeline.py
    </div>
  </section>

  <div class="divider"></div>

  <!-- FUTURE -->
  <section>
    <div class="section-label">07 — Roadmap</div>
    <h2>Future Improvements</h2>
    <div class="future-list">
      <div class="future-item">
        <span class="fi-icon">🌲</span>
        <div>
          <strong>Isolation Forest</strong>
          <p>Replace PCA with Isolation Forest for more robust anomaly detection.</p>
        </div>
      </div>
      <div class="future-item">
        <span class="fi-icon">⏰</span>
        <div>
          <strong>Airflow Scheduling</strong>
          <p>Orchestrate and schedule pipeline runs using Apache Airflow DAGs.</p>
        </div>
      </div>
      <div class="future-item">
        <span class="fi-icon">⚡</span>
        <div>
          <strong>Bulk DB Inserts</strong>
          <p>Switch to bulk insert strategy for significantly faster DB loading.</p>
        </div>
      </div>
      <div class="future-item">
        <span class="fi-icon">📱</span>
        <div>
          <strong>Streamlit Dashboard</strong>
          <p>Build an interactive web dashboard for real-time price analytics.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- AUTHOR -->
  <div class="author-card">
    <div class="author-avatar">TT</div>
    <div>
      <h3>Tanishq Tomar</h3>
      <p>Author · Amazon Price Analytics Pipeline</p>
    </div>
  </div>

</div>

<script>
  // Scroll progress bar
  window.addEventListener('scroll', () => {
    const el = document.getElementById('scrollBar');
    const scrolled = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    el.style.width = scrolled + '%';
  });

  // Staggered section reveal on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = '0.05s';
        entry.target.style.animationName = 'fadeUp';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('section, .author-card').forEach(el => {
    el.style.opacity = '0';
    el.style.animationDuration = '0.55s';
    el.style.animationFillMode = 'both';
    observer.observe(el);
  });
</script>
</body>
</html>

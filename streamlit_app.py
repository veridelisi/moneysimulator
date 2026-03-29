import streamlit as st

st.set_page_config(page_title="MoneySimulator", layout="wide", page_icon="💵")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}

        .hero-container {
            background: linear-gradient(135deg, #1e3a5f 0%, #0f2a47 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .hero-subtitle {
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
            font-weight: 300;
        }
        .hero-description {
            font-size: 1.1rem;
            opacity: 0.8;
            max-width: 650px;
            margin: 0 auto;
            line-height: 1.6;
        }
        .project-card {
            background: white;
            border-radius: 20px;
            padding: 0;
            margin: 1.5rem 0;
            box-shadow: 0 12px 40px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            overflow: hidden;
        }
        .card-header {
            padding: 2rem 2rem 1rem 2rem;
            border-radius: 20px 20px 0 0;
            position: relative;
            color: white;
            overflow: hidden;
        }
        .card-header::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255,255,255,0.08);
        }
        .card-content { position: relative; z-index: 2; }
        .card-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }
        .card-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 6px 16px;
            border-radius: 25px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: white;
            margin: 0;
            line-height: 1.3;
        }
        .card-body { padding: 1.5rem 2rem 1rem 2rem; }
        .card-tagline {
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .card-description {
            color: #475569;
            line-height: 1.7;
            font-size: 0.95rem;
        }
        .gradient-fed      { background: linear-gradient(135deg, #1e3a5f 0%, #0f2a47 100%); }
        .gradient-treasury { background: linear-gradient(135deg, #10b981 0%, #047857 100%); }
        .gradient-banks    { background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%); }
        .gradient-karma    { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); }

        .stats-container {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e3a5f;
            display: block;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .category-header {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            margin: 3rem 0 2rem 0;
            border-left: 5px solid #1e3a5f;
            box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        }
        .category-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1e293b;
            margin: 0;
        }
        .category-subtitle {
            font-size: 1rem;
            color: #64748b;
            margin: 0.5rem 0 0 0;
            font-weight: 400;
        }
        .footer {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-top: 4rem;
        }
        .footer a { color: #60a5fa; text-decoration: none; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">💵 MoneySimulator</div>
        <div class="hero-subtitle">Money Operations • Accounting • Flow Analysis</div>
        <div class="hero-description">
            Explore how money moves through the Federal Reserve, Treasury, and banking system.
            Every scenario is independent, step-by-step, and visualized with T-accounts and flow diagrams.
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="stats-container">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div>
                <span class="stat-number">4</span>
                <span class="stat-label">Categories</span>
            </div>
            <div>
                <span class="stat-number">20+</span>
                <span class="stat-label">Scenarios</span>
            </div>
            <div>
                <span class="stat-number">T-Acc</span>
                <span class="stat-label">Accounting</span>
            </div>
            <div>
                <span class="stat-number">Flow</span>
                <span class="stat-label">Visualization</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Card helper ───────────────────────────────────────────────────────────────
def scenario_card(title, tagline, description, icon, gradient_class, badge_text, page_path, btn_key):
    st.markdown(f"""
    <div class="project-card">
        <div class="card-header {gradient_class}">
            <div class="card-content">
                <span class="card-icon">{icon}</span>
                <span class="card-badge">{badge_text}</span>
                <h3 class="card-title">{title}</h3>
            </div>
        </div>
        <div class="card-body">
            <div class="card-tagline">{tagline}</div>
            <div class="card-description">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore →", key=btn_key):
        st.switch_page(page_path)

# ── FED ───────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="category-header">
        <h2 class="category-title">🏛️ Federal Reserve Operations</h2>
        <p class="category-subtitle">Open market operations, QE, repo, and reserve management</p>
    </div>
""", unsafe_allow_html=True)

scenario_card(
    title="Federal Reserve Operations",
    tagline="QE • OMO • Repo • Reserve Management",
    description="Explore how the Fed creates reserves through open market operations, "
                "quantitative easing, and repo facilities. Step-by-step T-account walkthroughs.",
    icon="🏛️",
    gradient_class="gradient-fed",
    badge_text="FED",
    page_path="pages/01_fed.py",
    btn_key="btn_fed",
)

# ── TREASURY ──────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="category-header">
        <h2 class="category-title">💰 Treasury Operations</h2>
        <p class="category-subtitle">Bond issuance, TGA movements, and reserve effects</p>
    </div>
""", unsafe_allow_html=True)

scenario_card(
    title="Treasury Operations",
    tagline="Bond Issuance • TGA • Reserve Impact",
    description="See how Treasury bond issuance drains reserves and how government spending "
                "injects them back. Follow the TGA balance through each transaction.",
    icon="💰",
    gradient_class="gradient-treasury",
    badge_text="Treasury",
    page_path="pages/02_treasury.py",
    btn_key="btn_treasury",
)

# ── BANKS ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="category-header">
        <h2 class="category-title">🏦 Banking System</h2>
        <p class="category-subtitle">Credit creation, reserve transfers, and deposit mechanics</p>
    </div>
""", unsafe_allow_html=True)

scenario_card(
    title="Banking System",
    tagline="Credit Creation • Reserve Transfer • Deposits",
    description="Understand how banks create money through lending, how reserves move "
                "between institutions, and what really happens on both sides of the balance sheet.",
    icon="🏦",
    gradient_class="gradient-banks",
    badge_text="Banks",
    page_path="pages/03_banks.py",
    btn_key="btn_banks",
)

# ── COMBINED ──────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="category-header">
        <h2 class="category-title">🔀 Combined Scenarios</h2>
        <p class="category-subtitle">FED + Treasury + Banks interactions and net effects</p>
    </div>
""", unsafe_allow_html=True)

scenario_card(
    title="Combined Scenarios",
    tagline="FED + Treasury + Banks • Net Reserve Effects",
    description="What happens when QE and bond issuance occur simultaneously? "
                "Explore how the three actors interact and offset each other.",
    icon="⚡",
    gradient_class="gradient-karma",
    badge_text="Combined",
    page_path="pages/04_karma.py",
    btn_key="btn_karma",
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        <h3 style="margin-top: 0;">About MoneySimulator</h3>
        <p style="margin-bottom: 1.5rem;">
            An educational simulation platform visualizing Federal Reserve, Treasury, 
            and banking system operations through accounting entries and flow diagrams.
        </p>
        <div style="border-top: 1px solid #475569; padding-top: 1.5rem; margin-top: 1.5rem;">
            <a href="https://veridelisi.substack.com/">📰 Veri Delisi Substack</a><br>
            <span style="color: #94a3b8;">Created by</span>
            <strong>Engin Yılmaz</strong> •
            <span style="color: #94a3b8;">2025</span>
        </div>
    </div>
""", unsafe_allow_html=True)
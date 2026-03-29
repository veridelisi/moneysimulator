import streamlit as st

st.set_page_config(page_title="MoneySimulator", layout="wide", page_icon="💵")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Syne', 'Segoe UI', sans-serif !important;
}
[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

/* ── Hero ── */
.hero {
    background: #1E1B4B;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.2rem;
}
.hero-title  { font-size: 2.2rem; font-weight: 800; color: white; margin-bottom: 0.4rem; }
.hero-sub    { font-size: 1rem; color: rgba(255,255,255,0.65); font-weight: 400; margin-bottom: 0.8rem; }
.hero-desc   { font-size: 0.88rem; color: rgba(255,255,255,0.5); line-height: 1.6; max-width: 500px; margin: 0 auto; }

/* ── Stat pills ── */
.stat-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.2rem; }
.stat-pill {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.12);
    border-radius: 8px;
    padding: 10px 14px;
    flex: 1; min-width: 100px;
}
.stat-pill-val   { font-size: 1.5rem; font-weight: 700; color: #1a1a1a; }
.stat-pill-label { font-size: 10px; color: #6b6b6b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }

/* ── Section header ── */
.section-head {
    margin: 1.8rem 0 0.8rem 0;
    border-left: 3px solid #1E1B4B;
    padding-left: 12px;
}
.section-title { font-size: 1rem; font-weight: 700; color: #1a1a1a; margin: 0; }
.section-sub   { font-size: 0.78rem; color: #6b6b6b; margin: 2px 0 0 0; }

/* ── Scenario card ── */
.sc-card {
    background: white;
    border: 0.5px solid rgba(0,0,0,0.12);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 8px;
    transition: box-shadow 0.2s;
}
.sc-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.10); }

.sc-card-top {
    padding: 14px 14px 10px 14px;
}
.sc-badge {
    display: inline-block;
    font-size: 9px; font-weight: 700;
    padding: 2px 9px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.6px;
    margin-bottom: 6px;
}
.badge-fed      { background: #E6F1FB; color: #185FA5; }
.badge-treasury { background: #EAF3DE; color: #3B6D11; }
.badge-banks    { background: #FEF3C7; color: #92400E; }
.badge-combined { background: #EDE9FE; color: #5B21B6; }

.sc-icon  { font-size: 1.6rem; display: block; margin-bottom: 4px; }
.sc-title { font-size: 0.95rem; font-weight: 700; color: #1a1a1a; margin: 0 0 4px 0; line-height: 1.3; }
.sc-desc  { font-size: 0.78rem; color: #6b6b6b; line-height: 1.5; margin: 0; }

.sc-card-bottom {
    border-top: 0.5px solid rgba(0,0,0,0.08);
    padding: 0;
}

/* ── Color accents per section ── */
.acc-fed      { border-left: 3px solid #185FA5; }
.acc-treasury { border-left: 3px solid #3B6D11; }
.acc-banks    { border-left: 3px solid #92400E; }
.acc-combined { border-left: 3px solid #5B21B6; }

/* section head accent */
.sh-fed      { border-left-color: #185FA5; }
.sh-treasury { border-left-color: #3B6D11; }
.sh-banks    { border-left-color: #92400E; }
.sh-combined { border-left-color: #5B21B6; }

/* ── Footer ── */
.footer {
    background: #f7f7f5;
    border: 0.5px solid rgba(0,0,0,0.10);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 2rem;
}
.footer-title { font-size: 0.95rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.4rem; }
.footer-desc  { font-size: 0.8rem; color: #6b6b6b; line-height: 1.6; margin-bottom: 0.8rem; }
.footer a     { color: #185FA5; text-decoration: none; font-weight: 700; font-size: 0.85rem; }
.footer-by    { font-size: 0.75rem; color: #a0a0a0; margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">💵 MoneySimulator</div>
    <div class="hero-sub">Money Operations • Accounting • Flow Analysis</div>
    <div class="hero-desc">
        Explore how money moves through the Federal Reserve, Treasury, and banking system.
        Step-by-step T-accounts and flow diagrams.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)
for col, val, label in [
    (s1, "4",     "Categories"),
    (s2, "20+",   "Scenarios"),
    (s3, "T-Acc", "Accounting"),
    (s4, "Flow",  "Visualization"),
]:
    with col:
        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-pill-val">{val}</div>
            <div class="stat-pill-label">{label}</div>
        </div>""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sc_card(col, icon, badge_cls, badge_txt, title, desc, accent_cls, page, btn_key):
    with col:
        st.markdown(f"""
        <div class="sc-card {accent_cls}">
            <div class="sc-card-top">
                <span class="sc-badge {badge_cls}">{badge_txt}</span>
                <span class="sc-icon">{icon}</span>
                <p class="sc-title">{title}</p>
                <p class="sc-desc">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore →", key=btn_key):
            st.switch_page(page)

def section(title, sub, accent_cls):
    st.markdown(f"""
    <div class="section-head {accent_cls}">
        <div class="section-title">{title}</div>
        <div class="section-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def render_rows(rows, badge_cls, accent_cls, page):
    for row in rows:
        cols = st.columns(4, gap="small")
        for i, c in enumerate(row):
            sc_card(cols[i], c["icon"], badge_cls, c["badge"],
                    c["title"], c["desc"], accent_cls, page, c["key"])
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO DATA
# ══════════════════════════════════════════════════════════════════════════════
FED = [
    [
        dict(icon="🖨️", badge="QE",   title="Quantitative Easing",
             desc="How the Fed buys bonds and creates reserves.", key="fed_qe"),
        dict(icon="🔄", badge="OMO",  title="Open Market Ops",
             desc="Day-to-day reserve injection via T-bill purchases.", key="fed_omo"),
        dict(icon="🏦", badge="Repo", title="Repo Facility",
             desc="Overnight collateralized lending to primary dealers.", key="fed_repo"),
        dict(icon="↩️", badge="RRP",  title="Reverse Repo",
             desc="Draining excess liquidity through overnight RRPs.", key="fed_rrp"),
    ],
    [
        dict(icon="📉", badge="QT",   title="Quantitative Tightening",
             desc="Balance sheet runoff and its effect on reserves.", key="fed_qt"),
        dict(icon="💳", badge="IOR",  title="Interest on Reserves",
             desc="How IORB sets the floor for the fed funds rate.", key="fed_ior"),
        dict(icon="🆘", badge="LOLR", title="Lender of Last Resort",
             desc="Emergency discount window lending under stress.", key="fed_lolr"),
        dict(icon="🌐", badge="Swap", title="FX Swap Lines",
             desc="Dollar liquidity to foreign central banks.", key="fed_swap"),
    ],
]

TREASURY = [
    [
        dict(icon="📜", badge="Issue",   title="Bond Issuance",
             desc="How Treasury auctions drain bank reserves.", key="tsy_issuance"),
        dict(icon="🏛️", badge="TGA",    title="TGA Drawdown",
             desc="Government spending injects reserves back.", key="tsy_tga"),
        dict(icon="💵", badge="Bills",   title="T-Bill Rollover",
             desc="Short-term bill rollover and reserve impact.", key="tsy_bills"),
        dict(icon="📊", badge="Deficit", title="Deficit Financing",
             desc="Borrowing to fund a deficit affects reserves.", key="tsy_deficit"),
    ],
]

BANKS = [
    [
        dict(icon="💰", badge="Credit",   title="Credit Creation",
             desc="Banks create deposits when they lend.", key="bnk_credit"),
        dict(icon="↔️", badge="Transfer", title="Reserve Transfer",
             desc="Interbank payments move reserves across Fed accounts.", key="bnk_transfer"),
        dict(icon="🏧", badge="Withdraw", title="Cash Withdrawal",
             desc="Withdrawal mechanics and reserve drain.", key="bnk_withdraw"),
        dict(icon="📋", badge="Capital",  title="Capital Requirements",
             desc="How regulatory ratios constrain credit expansion.", key="bnk_capital"),
    ],
]

COMBINED = [
    [
        dict(icon="⚡", badge="QE+Bond", title="QE & Bond Issuance",
             desc="Fed buys what Treasury issues — net reserve effect.", key="cmb_qe"),
        dict(icon="🔁", badge="Fiscal",  title="Fiscal + Monetary",
             desc="Deficit spending financed by QE.", key="cmb_fiscal"),
        dict(icon="🌊", badge="Crisis",  title="Crisis Playbook",
             desc="2008 & 2020: LOLR + QE + fiscal stimulus.", key="cmb_crisis"),
        dict(icon="🔜", badge="Soon",    title="Coming Soon",
             desc="More combined scenarios in progress.", key="cmb_soon"),
    ],
]

# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════
section("🏛️ Federal Reserve Operations",
        "Open market operations, QE, repo, and reserve management",
        "sh-fed")
render_rows(FED, "badge-fed", "acc-fed", "pages/01_fed.py")

section("💰 Treasury Operations",
        "Bond issuance, TGA movements, and reserve effects",
        "sh-treasury")
render_rows(TREASURY, "badge-treasury", "acc-treasury", "pages/02_treasury.py")

section("🏦 Banking System",
        "Credit creation, reserve transfers, and deposit mechanics",
        "sh-banks")
render_rows(BANKS, "badge-banks", "acc-banks", "pages/03_banks.py")

section("🔀 Combined Scenarios",
        "FED + Treasury + Banks interactions and net effects",
        "sh-combined")
render_rows(COMBINED, "badge-combined", "acc-combined", "pages/04_karma.py")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-title">About MoneySimulator</div>
    <div class="footer-desc">
        An educational platform visualizing Federal Reserve, Treasury,
        and banking system operations through accounting entries and flow diagrams.
    </div>
    <a href="https://veridelisi.substack.com/">📰 Veri Delisi Substack</a>
    <div class="footer-by">Created by <strong>Engin Yılmaz</strong> • 2026</div>
</div>
""", unsafe_allow_html=True)
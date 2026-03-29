import streamlit as st

st.set_page_config(page_title="MoneySimulator", layout="wide", page_icon="💵")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}

        .hero-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .hero-title { font-size: 3rem; font-weight: 700; margin-bottom: 1rem; }
        .hero-subtitle { font-size: 1.3rem; opacity: 0.9; margin-bottom: 1.5rem; font-weight: 300; }
        .hero-description { font-size: 1.1rem; opacity: 0.8; max-width: 650px; margin: 0 auto; line-height: 1.6; }

        .mini-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .mini-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.13);
            border-color: transparent;
        }
        .mini-card-header { padding: 1.2rem 1.2rem 0.8rem 1.2rem; }
        .mini-card-icon { font-size: 1.8rem; display: block; margin-bottom: 0.5rem; }
        .mini-card-badge {
            display: inline-block;
            background: rgba(255,255,255,0.25);
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border: 1px solid rgba(255,255,255,0.3);
            margin-bottom: 0.5rem;
        }
        .mini-card-title { font-size: 1rem; font-weight: 700; color: white; margin: 0; line-height: 1.3; }
        .mini-card-body { padding: 0.9rem 1.2rem 0.5rem 1.2rem; }
        .mini-card-desc { color: #64748b; font-size: 0.82rem; line-height: 1.5; }

        .g-fed      { background: linear-gradient(135deg, #1e3a5f 0%, #2d5a9e 100%); }
        .g-treasury { background: linear-gradient(135deg, #047857 0%, #10b981 100%); }
        .g-banks    { background: linear-gradient(135deg, #b45309 0%, #f59e0b 100%); }
        .g-combined { background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%); }

        .stat-box {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .stat-number { font-size: 2.2rem; font-weight: 700; color: #1e3a5f; display: block; }
        .stat-label { font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }

        .category-header {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 1.2rem 1.8rem;
            border-radius: 14px;
            margin: 2.5rem 0 1.2rem 0;
            border-left: 5px solid #1e3a5f;
        }
        .category-title { font-size: 1.3rem; font-weight: 700; color: #1e293b; margin: 0; }
        .category-subtitle { font-size: 0.9rem; color: #64748b; margin: 0.3rem 0 0 0; }

        .footer {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 2.5rem 2rem;
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
s1, s2, s3, s4 = st.columns(4)
for col, num, label in [
    (s1, "4",    "Categories"),
    (s2, "20+",  "Scenarios"),
    (s3, "T-Acc","Accounting"),
    (s4, "Flow", "Visualization"),
]:
    with col:
        st.markdown(f'<div class="stat-box"><span class="stat-number">{num}</span><span class="stat-label">{label}</span></div>', unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def mini_card(col, card, gradient):
    with col:
        st.markdown(f"""
        <div class="mini-card">
            <div class="mini-card-header {gradient}">
                <span class="mini-card-icon">{card['icon']}</span>
                <span class="mini-card-badge">{card['badge']}</span>
                <p class="mini-card-title">{card['title']}</p>
            </div>
            <div class="mini-card-body">
                <div class="mini-card-desc">{card['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Explore →", key=card["key"]):
            st.switch_page(card["page"])


def render_section(title, subtitle, rows, gradient, border_color):
    st.markdown(f"""
        <div class="category-header" style="border-left-color:{border_color}">
            <div class="category-title">{title}</div>
            <div class="category-subtitle">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)
    for row in rows:
        # Always 4 columns; empty cols stay blank
        cols = st.columns(4, gap="medium")
        for i, card in enumerate(row):
            mini_card(cols[i], card, gradient)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO DATA
# To add a new row: append a new list of up to 4 dicts inside the section list.
# To add a new card to a row: append a dict to an existing inner list.
# ══════════════════════════════════════════════════════════════════════════════

FED = [
    # ── Row 1 ──
    [
        dict(icon="🖨️", badge="QE",   title="Quantitative Easing",
             desc="How the Fed buys bonds and creates reserves from thin air.",
             page="pages/01_fed.py", key="fed_qe"),
        dict(icon="🔄", badge="OMO",  title="Open Market Operations",
             desc="Day-to-day reserve injection via Treasury bill purchases.",
             page="pages/01_fed.py", key="fed_omo"),
        dict(icon="🏦", badge="Repo", title="Repo Facility",
             desc="Overnight collateralized lending to primary dealers.",
             page="pages/01_fed.py", key="fed_repo"),
        dict(icon="↩️", badge="RRP",  title="Reverse Repo",
             desc="Draining excess liquidity through overnight reverse repos.",
             page="pages/01_fed.py", key="fed_rrp"),
    ],
    # ── Row 2 ──
    [
        dict(icon="📉", badge="QT",   title="Quantitative Tightening",
             desc="Balance sheet runoff and its effect on reserve levels.",
             page="pages/01_fed.py", key="fed_qt"),
        dict(icon="💳", badge="IOR",  title="Interest on Reserves",
             desc="How IORB sets the floor for the federal funds rate.",
             page="pages/01_fed.py", key="fed_ior"),
        dict(icon="🆘", badge="LOLR", title="Lender of Last Resort",
             desc="Emergency discount window lending during stress events.",
             page="pages/01_fed.py", key="fed_lolr"),
        dict(icon="🌐", badge="Swap", title="FX Swap Lines",
             desc="Dollar liquidity provision to foreign central banks.",
             page="pages/01_fed.py", key="fed_swap"),
    ],
]

TREASURY = [
    # ── Row 1 ──
    [
        dict(icon="📜", badge="Issue",   title="Bond Issuance",
             desc="How Treasury auctions drain reserves from the banking system.",
             page="pages/02_treasury.py", key="tsy_issuance"),
        dict(icon="🏛️", badge="TGA",    title="TGA Drawdown",
             desc="Government spending and how it injects reserves back.",
             page="pages/02_treasury.py", key="tsy_tga"),
        dict(icon="💵", badge="Bills",   title="T-Bill Rollover",
             desc="Short-term bill rollover mechanics and reserve impact.",
             page="pages/02_treasury.py", key="tsy_bills"),
        dict(icon="📊", badge="Deficit", title="Deficit Financing",
             desc="How borrowing to fund a deficit affects bank reserves.",
             page="pages/02_treasury.py", key="tsy_deficit"),
    ],
]

BANKS = [
    # ── Row 1 ──
    [
        dict(icon="💰", badge="Credit",    title="Credit Creation",
             desc="Banks create deposits when they lend — the multiplier myth busted.",
             page="pages/03_banks.py", key="bnk_credit"),
        dict(icon="↔️", badge="Transfer",  title="Reserve Transfer",
             desc="How interbank payments move reserves across Fed accounts.",
             page="pages/03_banks.py", key="bnk_transfer"),
        dict(icon="🏧", badge="Withdraw",  title="Cash Withdrawal",
             desc="Withdrawal mechanics and reserve drain on a single bank.",
             page="pages/03_banks.py", key="bnk_withdraw"),
        dict(icon="📋", badge="Capital",   title="Capital Requirements",
             desc="How regulatory capital ratios constrain credit expansion.",
             page="pages/03_banks.py", key="bnk_capital"),
    ],
]

COMBINED = [
    # ── Row 1 ──
    [
        dict(icon="⚡", badge="QE+Bond", title="QE & Bond Issuance",
             desc="When the Fed buys exactly what Treasury issues — net reserve effect.",
             page="pages/04_karma.py", key="cmb_qe_bond"),
        dict(icon="🔁", badge="Fiscal",  title="Fiscal + Monetary Mix",
             desc="Deficit spending financed by QE — helicopter money dynamics.",
             page="pages/04_karma.py", key="cmb_fiscal"),
        dict(icon="🌊", badge="Crisis",  title="Crisis Playbook",
             desc="2008 & 2020: LOLR + QE + fiscal stimulus in one flow.",
             page="pages/04_karma.py", key="cmb_crisis"),
        dict(icon="🔜", badge="Soon",    title="Coming Soon",
             desc="More combined scenarios in progress.",
             page="pages/04_karma.py", key="cmb_soon"),
    ],
]

# ── Render all sections ───────────────────────────────────────────────────────

render_section("🏦 Banking System",
               "Credit creation, reserve transfers, and deposit mechanics",
               BANKS, "g-banks", "#b45309")

render_section("🏛️ Federal Reserve Operations",
               "Open market operations, QE, repo, and reserve management",
               FED, "g-fed", "#1e3a5f")

render_section("💰 Treasury Operations",
               "Bond issuance, TGA movements, and reserve effects",
               TREASURY, "g-treasury", "#047857")

render_section("🔀 Combined Scenarios",
               "FED + Treasury + Banks interactions and net effects",
               COMBINED, "g-combined", "#6d28d9")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        <h3 style="margin-top:0">About MoneySimulator</h3>
        <p>An educational platform visualizing Federal Reserve, Treasury, and banking system
        operations through accounting entries and flow diagrams.</p>
        <div style="border-top:1px solid #475569;padding-top:1.5rem;margin-top:1.5rem">
            <a href="https://veridelisi.substack.com/">📰 Veri Delisi Substack</a><br>
            <span style="color:#94a3b8">Created by</span> <strong>Engin Yılmaz</strong> •
            <span style="color:#94a3b8">2026</span>
        </div>
    </div>
""", unsafe_allow_html=True)
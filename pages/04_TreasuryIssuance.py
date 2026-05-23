import streamlit as st
import plotly.graph_objects as go
from copy import deepcopy

st.set_page_config(
    page_title="Treasury Bond Issuance · MoneySimulator",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# HIDE DEFAULT SIDEBAR NAV
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Syne', 'Segoe UI', sans-serif !important;
}
.block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; }

/* Sidebar metrics */
.sb-metric {
    background:white;
    border:0.5px solid rgba(0,0,0,0.12);
    border-radius:8px;
    padding:10px 12px;
    margin-bottom:7px;
}
.sb-metric-label {
    font-size:10px;
    color:#6b6b6b;
    text-transform:uppercase;
    letter-spacing:0.5px;
}
.sb-metric-val {
    font-size:22px;
    font-weight:700;
    color:#1a1a1a;
    margin-top:1px;
}
.sb-metric-delta {
    font-size:11px;
    margin-top:1px;
}
.delta-pos { color:#1D9E75; }
.delta-neg { color:#D85A30; }
.delta-neu { color:#a0a0a0; }

.dots-row {
    display:flex;
    gap:5px;
    flex-wrap:wrap;
    margin-top:4px;
}
.dot-done {
    width:12px;
    height:12px;
    border-radius:50%;
    background:#1D9E75;
    display:inline-block;
}
.dot-active {
    width:12px;
    height:12px;
    border-radius:50%;
    background:#047857;
    outline:2px solid #A7F3D0;
    outline-offset:1px;
    display:inline-block;
}
.dot-empty {
    width:12px;
    height:12px;
    border-radius:50%;
    background:rgba(0,0,0,0.12);
    display:inline-block;
}

/* Mode cards */
.mode-card {
    border-radius:14px;
    padding:24px 28px;
    text-align:center;
    cursor:pointer;
    border:2px solid transparent;
    transition:all 0.2s;
}
.mode-card-training {
    background:#ECFDF5;
    border-color:#A7F3D0;
}
.mode-card-sim {
    background:#FFFBEB;
    border-color:#FCD34D;
}
.mode-title {
    font-size:18px;
    font-weight:800;
    color:#064E3B;
    margin:10px 0 6px 0;
}
.mode-sub {
    font-size:12px;
    color:#4B5563;
    line-height:1.5;
}
.mode-badge-t {
    display:inline-block;
    background:#047857;
    color:white;
    font-size:10px;
    font-weight:700;
    padding:3px 10px;
    border-radius:20px;
    margin-bottom:8px;
}
.mode-badge-s {
    display:inline-block;
    background:#F59E0B;
    color:white;
    font-size:10px;
    font-weight:700;
    padding:3px 10px;
    border-radius:20px;
    margin-bottom:8px;
}

/* Step header */
.step-header-card {
    background:#ECFDF5;
    border:1px solid #A7F3D0;
    border-radius:12px;
    padding:16px 20px;
    margin-bottom:10px;
}
.step-header-sim {
    background:#FFFBEB;
    border:1px solid #FCD34D;
    border-radius:12px;
    padding:16px 20px;
    margin-bottom:10px;
}
.step-badge {
    background:#D1FAE5;
    color:#065F46;
    font-size:10px;
    font-weight:700;
    padding:3px 10px;
    border-radius:20px;
    display:inline-block;
    margin-bottom:6px;
    text-transform:uppercase;
    letter-spacing:0.5px;
}
.step-badge-s {
    background:#FEF3C7;
    color:#92400E;
    font-size:10px;
    font-weight:700;
    padding:3px 10px;
    border-radius:20px;
    display:inline-block;
    margin-bottom:6px;
    text-transform:uppercase;
    letter-spacing:0.5px;
}
.step-title {
    font-size:17px;
    font-weight:700;
    color:#064E3B;
    margin-bottom:4px;
}
.step-desc {
    font-size:13px;
    color:#4B5563;
    line-height:1.6;
}
.tag {
    display:inline-block;
    font-size:11px;
    font-weight:700;
    padding:3px 10px;
    border-radius:20px;
    margin-top:7px;
}
.tag-green { background:#EAF3DE; color:#3B6D11; }
.tag-red   { background:#FCEBEB; color:#A32D2D; }
.tag-blue  { background:#E6F1FB; color:#185FA5; }
.tag-gold  { background:#FEF3C7; color:#92400E; }

/* Amount display */
.training-amount {
    background:#047857;
    color:white;
    font-size:28px;
    font-weight:800;
    padding:12px 28px;
    border-radius:12px;
    display:inline-block;
    margin:12px 0;
}

/* Flow strip */
.flow-strip {
    background:#f7f7f5;
    border:0.5px solid rgba(0,0,0,0.10);
    border-radius:10px;
    padding:12px 16px;
    margin-bottom:10px;
}
.flow-label {
    font-size:10px;
    color:#a0a0a0;
    text-transform:uppercase;
    letter-spacing:0.6px;
    margin-bottom:10px;
}
.flow-row {
    display:flex;
    align-items:center;
    flex-wrap:wrap;
    row-gap:8px;
}
.flow-node {
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:4px;
}
.flow-circle {
    width:46px;
    height:46px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
    font-weight:700;
    border:2px solid;
}
.flow-node-lbl {
    font-size:9px;
    color:#6b6b6b;
    text-align:center;
    max-width:64px;
    line-height:1.3;
}
.flow-arrow {
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:0 6px;
}
.flow-amt {
    font-size:9px;
    color:#6b6b6b;
    font-weight:700;
}
.flow-line {
    height:2px;
    width:38px;
    background:rgba(0,0,0,0.2);
    position:relative;
    margin:2px 0;
}
.flow-line::after {
    content:'';
    position:absolute;
    right:-5px;
    top:-4px;
    border-top:5px solid transparent;
    border-bottom:5px solid transparent;
    border-left:7px solid rgba(0,0,0,0.2);
}
.flow-note {
    font-size:9px;
    color:#a0a0a0;
}

/* Balance sheet */
.bsheet {
    border:0.5px solid rgba(0,0,0,0.12);
    border-radius:8px;
    overflow:hidden;
    margin-bottom:8px;
}
.bsheet.active {
    border:1.5px solid #047857;
}
.bsheet-head {
    padding:6px 10px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    border-bottom:0.5px solid rgba(0,0,0,0.08);
    background:#f7f7f5;
}
.bsheet-name {
    font-size:12px;
    font-weight:700;
    color:#1a1a1a;
}
.bsheet-active-badge {
    font-size:9px;
    background:#D1FAE5;
    color:#065F46;
    padding:1px 7px;
    border-radius:10px;
    font-weight:700;
}
.bsheet-body {
    display:grid;
    grid-template-columns:1fr 1fr;
}
.bsheet-col {
    padding:7px 9px;
}
.bsheet-col-left {
    border-right:0.5px solid rgba(0,0,0,0.08);
}
.col-title-a {
    font-size:9px;
    text-transform:uppercase;
    letter-spacing:0.4px;
    color:#185FA5;
    font-weight:700;
    margin-bottom:4px;
}
.col-title-l {
    font-size:9px;
    text-transform:uppercase;
    letter-spacing:0.4px;
    color:#A32D2D;
    font-weight:700;
    margin-bottom:4px;
}
.bsheet-row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:10px;
    color:#6b6b6b;
    padding:2px 0;
    gap:4px;
}
.bsheet-row .bval {
    font-weight:700;
    color:#1a1a1a;
    white-space:nowrap;
}
.bsheet-empty {
    padding:14px;
    text-align:center;
    font-size:11px;
    color:#a0a0a0;
}
.bsheet-total {
    padding:4px 9px;
    border-top:0.5px solid rgba(0,0,0,0.08);
    display:flex;
    justify-content:space-between;
    font-size:10px;
    font-weight:700;
    background:#f7f7f5;
}
.t-a { color:#185FA5; }
.t-l { color:#A32D2D; }

.bsheet-panel {
    background:#ffffff;
    border:0.5px solid rgba(0,0,0,0.10);
    border-radius:12px;
    padding:14px 16px;
    margin-top:12px;
}
.bsheet-panel-grid {
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap:12px;
}

/* Insight and choices */
.insight-bar {
    background:#ECFDF5;
    border:1px solid #A7F3D0;
    border-radius:8px;
    padding:10px 14px;
    font-size:12px;
    color:#065F46;
    line-height:1.6;
    margin:4px 0 10px 0;
}
.warning-bar {
    background:#FEF2F2;
    border:1px solid #FCA5A5;
    border-radius:8px;
    padding:10px 14px;
    font-size:12px;
    color:#991B1B;
    line-height:1.6;
    margin:8px 0 10px 0;
}
.choice-prompt {
    background:#FFFBEB;
    border:1px solid #FCD34D;
    border-radius:10px;
    padding:12px 16px;
    margin-bottom:12px;
}
.choice-prompt-label {
    font-size:12px;
    font-weight:700;
    color:#92400E;
    margin-bottom:2px;
}
.choice-prompt-sub {
    font-size:11px;
    color:#B45309;
}

/* Treasury monitor */
.monitor {
    background:white;
    border:0.5px solid rgba(0,0,0,0.10);
    border-radius:12px;
    padding:14px 16px;
    margin-bottom:12px;
}
.monitor-title {
    font-size:12px;
    font-weight:800;
    color:#064E3B;
    text-transform:uppercase;
    letter-spacing:0.5px;
    margin-bottom:10px;
}
.monitor-grid {
    display:grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap:8px;
}
.monitor-box {
    background:#F8FAFC;
    border-radius:8px;
    padding:10px;
}
.monitor-label {
    font-size:9px;
    color:#64748B;
    text-transform:uppercase;
    letter-spacing:0.4px;
}
.monitor-val {
    font-size:17px;
    font-weight:800;
    color:#0F172A;
    margin-top:3px;
}
.monitor-note {
    font-size:11px;
    color:#475569;
    margin-top:10px;
    line-height:1.5;
}

/* Complete */
.complete-card {
    background:linear-gradient(135deg,#DCFCE7,#D1FAE5);
    border:1px solid #86EFAC;
    border-radius:14px;
    padding:28px 32px;
    text-align:center;
    margin-bottom:16px;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .step-title { font-size:15px; }
    .step-desc { font-size:12px; }
    .training-amount {
        font-size:24px;
        padding:10px 20px;
    }
    .flow-circle {
        width:40px;
        height:40px;
        font-size:10px;
    }
    .flow-node-lbl {
        font-size:8px;
        max-width:52px;
    }
    .bsheet-panel-grid {
        grid-template-columns: 1fr;
    }
    .monitor-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 480px) {
    .step-header-card, .step-header-sim {
        padding:12px 16px;
        margin-bottom:8px;
    }
    .step-title {
        font-size:14px;
        margin-bottom:3px;
    }
    .step-desc {
        font-size:11px;
        line-height:1.4;
    }
    .training-amount {
        font-size:20px;
        padding:8px 16px;
        margin:8px 0;
    }
    .monitor-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────

SCENARIOS = [
    {
        "id": 1,
        "emoji": "🏁",
        "title": "Opening Position — Reserves in the Banking System",
        "short": "Bank X begins with reserves at the central bank and Investor A begins with a bank deposit.",
        "insight": """
        Before the auction, reserves sit on the banking system side of the Fed’s balance sheet.
        Investor A holds a deposit at Bank X. Treasury’s TGA balance is zero in this simplified setup.
        This opening position lets us see the reserve drain clearly when the bond is purchased.
        """,
        "tag": "📌 Starting Point",
        "tag_type": "blue",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["BankX", "CentralBank", "Treasury", "InvestorA"],
    },
    {
        "id": 2,
        "emoji": "📜",
        "title": "Treasury Sells a Bond to Investor A",
        "short": "Investor A buys a Treasury security using a Bank X deposit.",
        "insight": """
        Investor A exchanges a bank deposit for a Treasury security. Bank X debits Investor A’s deposit
        and transfers reserves to the Treasury General Account at the central bank. The key point:
        <strong>bank reserves fall, while the TGA rises</strong>.
        """,
        "tag": "🔻 Reserve Drain",
        "tag_type": "gold",
        "choice_type": "issuance",
        "training_amt": 200,
        "sim_opts": [100, 200, 300, 600],
        "sim_label": "How much Treasury debt does Investor A buy?",
        "involved": ["InvestorA", "BankX", "CentralBank", "Treasury"],
    },
    {
        "id": 3,
        "emoji": "🏛️",
        "title": "Settlement at the Fed — Reserves Become TGA Balances",
        "short": "The central bank’s liabilities shift from Bank X reserves to the Treasury’s TGA.",
        "insight": """
        The central bank did not create new reserves in this transaction. It simply changed the composition
        of its liabilities: <strong>Bank X reserves decreased</strong> and <strong>Treasury’s TGA increased</strong>.
        Treasury issuance therefore drains reserves from the banking system until Treasury later spends.
        """,
        "tag": "➡️ Composition Shift",
        "tag_type": "blue",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["CentralBank", "BankX", "Treasury"],
    },
    {
        "id": 4,
        "emoji": "🧾",
        "title": "Private Sector Portfolio Shift",
        "short": "Investor A now holds a Treasury security instead of a bank deposit.",
        "insight": """
        From Investor A’s perspective, the asset mix changed: deposits fell and Treasury securities rose.
        From Bank X’s perspective, both reserves and deposit liabilities fell. From Treasury’s perspective,
        the TGA increased and a new security liability was issued.
        """,
        "tag": "🔀 Deposit → Security",
        "tag_type": "blue",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["InvestorA", "BankX", "Treasury"],
    },
    {
        "id": 5,
        "emoji": "🎓",
        "title": "Treasury Bond Issuance Review",
        "short": "Bond issuance pulls reserves into the TGA and changes the private sector’s asset composition.",
        "insight": """
        Treasury bond issuance is not government spending. It is a financing operation that moves reserves
        from the banking system into the Treasury’s account at the central bank. The banking system loses
        reserves, the TGA rises, and the investor swaps a deposit for a Treasury security.
        """,
        "tag": "🎓 Complete",
        "tag_type": "green",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["BankX", "CentralBank", "Treasury", "InvestorA"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ENTITIES
# ─────────────────────────────────────────────────────────────────────────────

ENTITY_DEFS = {
    "BankX": {
        "label": "Bank X",
        "assets": {
            "Reserves": 500,
        },
        "liabilities": {
            "InvestorADep": 500,
        },
    },
    "CentralBank": {
        "label": "Central Bank",
        "assets": {
            "BalancingAssets": 500,
        },
        "liabilities": {
            "BankXReserves": 500,
            "TGA": 0,
        },
    },
    "Treasury": {
        "label": "Treasury",
        "assets": {
            "TGA": 0,
        },
        "liabilities": {
            "TreasurySecurities": 0,
        },
    },
    "InvestorA": {
        "label": "Investor A",
        "assets": {
            "Deposits": 500,
            "TreasurySecurities": 0,
        },
        "liabilities": {},
    },
}

ENTITY_ORDER = ["BankX", "CentralBank", "Treasury", "InvestorA"]

FRIENDLY = {
    "InvestorADep": "Investor A Dep",
    "BankXReserves": "Bank X Reserves",
    "TGA": "TGA",
    "TreasurySecurities": "Treasury Securities",
    "BalancingAssets": "Other Assets",
}

def fname(k):
    return FRIENDLY.get(k, k)

def init_state():
    return {
        k: {
            "assets": dict(v["assets"]),
            "liabilities": dict(v["liabilities"])
        }
        for k, v in ENTITY_DEFS.items()
    }

def apply_tx(state, txs):
    s = deepcopy(state)
    for entity, side, account, amount in txs:
        e = s[entity]

        if side == "debit":
            if account in e["assets"]:
                e["assets"][account] += amount
            elif account in e["liabilities"]:
                e["liabilities"][account] -= amount
            else:
                raise KeyError(f"{account} not found in {entity}")

        elif side == "credit":
            if account in e["assets"]:
                e["assets"][account] -= amount
            elif account in e["liabilities"]:
                e["liabilities"][account] += amount
            else:
                raise KeyError(f"{account} not found in {entity}")

    return s

# ─────────────────────────────────────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(state):
    bank_reserves = state["BankX"]["assets"].get("Reserves", 0)
    cb_reserves = state["CentralBank"]["liabilities"].get("BankXReserves", 0)
    tga = state["Treasury"]["assets"].get("TGA", 0)
    deposits = state["InvestorA"]["assets"].get("Deposits", 0)
    securities = state["InvestorA"]["assets"].get("TreasurySecurities", 0)
    outstanding = state["Treasury"]["liabilities"].get("TreasurySecurities", 0)

    return {
        "bank_reserves": bank_reserves,
        "cb_reserves": cb_reserves,
        "tga": tga,
        "deposits": deposits,
        "investor_securities": securities,
        "securities_outstanding": outstanding,
    }

def get_capacity(state):
    deposits = state["InvestorA"]["assets"].get("Deposits", 0)
    reserves = state["BankX"]["assets"].get("Reserves", 0)
    return min(deposits, reserves)

def issuance_allowed(state, amt):
    capacity = get_capacity(state)
    return amt <= capacity

# ─────────────────────────────────────────────────────────────────────────────
# TRANSACTIONS
# ─────────────────────────────────────────────────────────────────────────────

def build_transactions(sc_id, amt):
    if sc_id == 2:
        return [
            # Investor A pays for the Treasury security by losing deposit
            ("InvestorA", "credit", "Deposits", amt),
            ("InvestorA", "debit", "TreasurySecurities", amt),

            # Bank X removes Investor A's deposit liability and transfers reserves
            ("BankX", "debit", "InvestorADep", amt),
            ("BankX", "credit", "Reserves", amt),

            # Central Bank shifts liabilities from Bank X reserves to Treasury TGA
            ("CentralBank", "debit", "BankXReserves", amt),
            ("CentralBank", "credit", "TGA", amt),

            # Treasury receives TGA asset and issues security liability
            ("Treasury", "debit", "TGA", amt),
            ("Treasury", "credit", "TreasurySecurities", amt),
        ]

    return []

# ─────────────────────────────────────────────────────────────────────────────
# FLOW BUILDER
# ─────────────────────────────────────────────────────────────────────────────

BX = {
    "id": "BankX",
    "label": "Bank X",
    "abbr": "BX",
    "bg": "#E6F1FB",
    "border": "#378ADD",
    "color": "#185FA5"
}

CB = {
    "id": "CentralBank",
    "label": "Central Bank",
    "abbr": "Fed",
    "bg": "#E1F5EE",
    "border": "#1D9E75",
    "color": "#0F6E56"
}

TSY = {
    "id": "Treasury",
    "label": "Treasury",
    "abbr": "Tsy",
    "bg": "#ECFDF5",
    "border": "#047857",
    "color": "#065F46"
}

INV = {
    "id": "InvestorA",
    "label": "Investor A",
    "abbr": "IA",
    "bg": "#FEF3C7",
    "border": "#F59E0B",
    "color": "#92400E"
}

def arr(amt, note):
    return {"arrow": True, "amt": amt, "note": note}

def build_flow(sc_id, amt):
    a = f"${amt}"

    if sc_id == 1:
        return [CB, arr("$500", "reserves"), BX, arr("$500", "deposit"), INV]

    if sc_id == 2:
        return [
            INV,
            arr(f"{a} deposit", "payment"),
            BX,
            arr(f"{a} reserves", "to TGA"),
            CB,
            arr(f"{a} TGA", "credited"),
            TSY,
        ]

    if sc_id == 3:
        return [BX, arr("Reserves ↓", "drain"), CB, arr("TGA ↑", "liability shift"), TSY]

    if sc_id == 4:
        return [INV, arr("Deposit ↓", "portfolio shift"), TSY, arr("Security ↑", "asset held"), INV]

    if sc_id == 5:
        return [BX, arr("Reserves ↓", "banking system"), CB, arr("TGA ↑", "Treasury account"), TSY]

    return []

# ─────────────────────────────────────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def dots_html(current, total):
    parts = []
    for i in range(total):
        cls = "dot-done" if i < current else ("dot-active" if i == current else "dot-empty")
        parts.append(f'<span class="{cls}"></span>')
    return f'<div class="dots-row">{"".join(parts)}</div>'

def flow_html(nodes):
    if not nodes:
        return ""

    parts = []
    for n in nodes:
        if n.get("id"):
            parts.append(
                f'<div class="flow-node">'
                f'<div class="flow-circle" style="background:{n["bg"]};border-color:{n["border"]};color:{n["color"]};">{n["abbr"]}</div>'
                f'<div class="flow-node-lbl">{n["label"]}</div>'
                f'</div>'
            )
        elif n.get("arrow"):
            parts.append(
                f'<div class="flow-arrow">'
                f'<div class="flow-amt">{n["amt"]}</div>'
                f'<div class="flow-line"></div>'
                f'<div class="flow-note">{n.get("note", "")}</div>'
                f'</div>'
            )

    return f'<div class="flow-row">{"".join(parts)}</div>'

def money_fmt(v):
    if v < 0:
        return f"-${abs(v)}"
    return f"${v}"

def bsheet_html(ek, state, active):
    e = state[ek]
    label = ENTITY_DEFS[ek]["label"]
    assets = [(k, v) for k, v in e["assets"].items() if v != 0]
    liabs = [(k, v) for k, v in e["liabilities"].items() if v != 0]

    ta = sum(v for _, v in assets)
    tl = sum(v for _, v in liabs)

    if ta == 0 and tl == 0:
        return (
            f'<div class="bsheet">'
            f'<div class="bsheet-head">'
            f'<span class="bsheet-name" style="color:#a0a0a0;">{label}</span>'
            f'</div>'
            f'<div class="bsheet-empty">empty</div>'
            f'</div>'
        )

    badge = '<span class="bsheet-active-badge">active</span>' if active else ""
    acls = " active" if active else ""

    ar = "".join(
        f'<div class="bsheet-row"><span>{fname(k)}</span><span class="bval">{money_fmt(v)}</span></div>'
        for k, v in assets
    ) or '<div class="bsheet-row" style="color:#ccc;font-size:10px;">—</div>'

    lr = "".join(
        f'<div class="bsheet-row"><span>{fname(k)}</span><span class="bval">{money_fmt(v)}</span></div>'
        for k, v in liabs
    ) or '<div class="bsheet-row" style="color:#ccc;font-size:10px;">—</div>'

    return (
        f'<div class="bsheet{acls}">'
        f'<div class="bsheet-head">'
        f'<span class="bsheet-name">{label}</span>{badge}'
        f'</div>'
        f'<div class="bsheet-body">'
        f'<div class="bsheet-col bsheet-col-left">'
        f'<div class="col-title-a">Assets</div>{ar}'
        f'</div>'
        f'<div class="bsheet-col">'
        f'<div class="col-title-l">Liabilities</div>{lr}'
        f'</div>'
        f'</div>'
        f'<div class="bsheet-total">'
        f'<span class="t-a">{money_fmt(ta)}</span>'
        f'<span class="t-l">{money_fmt(tl)}</span>'
        f'</div>'
        f'</div>'
    )

def render_step_balance_sheets(state, involved_entities):
    if not involved_entities:
        return

    blocks = "".join(bsheet_html(ek, state, True) for ek in involved_entities)
    st.markdown(
        f'<div class="bsheet-panel"><div class="bsheet-panel-grid">{blocks}</div></div>',
        unsafe_allow_html=True
    )

def render_monitor(state):
    m = compute_metrics(state)
    capacity = get_capacity(state)

    st.markdown(
        f"""
        <div class="monitor">
            <div class="monitor-title">📜 Treasury Issuance Monitor</div>
            <div class="monitor-grid">
                <div class="monitor-box">
                    <div class="monitor-label">Bank X Reserves</div>
                    <div class="monitor-val">${m["bank_reserves"]}</div>
                </div>
                <div class="monitor-box">
                    <div class="monitor-label">Treasury TGA</div>
                    <div class="monitor-val">${m["tga"]}</div>
                </div>
                <div class="monitor-box">
                    <div class="monitor-label">Investor Deposits</div>
                    <div class="monitor-val">${m["deposits"]}</div>
                </div>
                <div class="monitor-box">
                    <div class="monitor-label">Securities Outstanding</div>
                    <div class="monitor-val">${m["securities_outstanding"]}</div>
                </div>
            </div>
            <div class="monitor-note">
                Remaining auction capacity in this simplified setup: <strong>${capacity}</strong>.
                It is limited by Investor A's deposit balance and Bank X's available reserves.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def reserve_tga_chart(history, height=260):
    labels = [d["label"] for d in history]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=labels,
            y=[d["bank_reserves"] for d in history],
            name="Bank X Reserves",
            marker_color="#85B7EB"
        )
    )

    fig.add_trace(
        go.Bar(
            x=labels,
            y=[d["tga"] for d in history],
            name="Treasury TGA",
            marker_color="#10B981"
        )
    )

    fig.update_layout(
        barmode="group",
        hovermode=False,
        height=height,
        dragmode=False,
        margin=dict(t=50, b=10, l=30, r=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="left",
            x=0,
            font=dict(size=10)
        ),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(size=10), fixedrange=True),
        bargap=0.4,
    )

    return fig

def append_history(label, state):
    m = compute_metrics(state)
    st.session_state[ss("history")].append({
        "label": label,
        "bank_reserves": m["bank_reserves"],
        "tga": m["tga"],
        "deposits": m["deposits"],
        "securities": m["securities_outstanding"],
    })

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

PREFIX = "tsy_issue_"

def ss(k):
    return PREFIX + k

for key, default in [
    ("mode", None),
    ("step", 0),
    ("ledger", None),
    ("history", None),
    ("chosen", {}),
    ("confirmed", set()),
    ("blocked_msg", None),
]:
    full = ss(key)
    if full not in st.session_state:
        st.session_state[full] = default

if st.session_state[ss("ledger")] is None:
    st.session_state[ss("ledger")] = init_state()

if st.session_state[ss("history")] is None:
    m0 = compute_metrics(init_state())
    st.session_state[ss("history")] = [{
        "label": "Start",
        "bank_reserves": m0["bank_reserves"],
        "tga": m0["tga"],
        "deposits": m0["deposits"],
        "securities": m0["securities_outstanding"],
    }]

def reset():
    for key in ["mode", "step", "ledger", "history", "chosen", "confirmed", "blocked_msg"]:
        full = ss(key)
        if full in st.session_state:
            del st.session_state[full]
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# MODE SELECTION SCREEN
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state[ss("mode")] is None:
    if st.button("← Back to Home", use_container_width=False):
        st.switch_page("streamlit_app.py")

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;margin-bottom:2rem;'>
            <div style='font-size:2rem;font-weight:800;color:#064E3B;'>📜 Treasury Bond Issuance</div>
            <div style='font-size:1rem;color:#6b6b6b;margin-top:6px;'>
                How Treasury auctions drain bank reserves into the TGA
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="mode-card mode-card-training">
            <span class="mode-badge-t">📖 Training</span>
            <div class="mode-title">Learn the Mechanics</div>
            <div class="mode-sub">
                Fixed issuance amount.<br>
                Follow the reserve drain step by step.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Start Training →", use_container_width=True, type="primary"):
            st.session_state[ss("mode")] = "training"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card mode-card-sim">
            <span class="mode-badge-s">🎮 Simulation</span>
            <div class="mode-title">Choose the Auction Size</div>
            <div class="mode-sub">
                Pick the Treasury issuance amount.<br>
                See whether settlement can be completed.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Start Simulation →", use_container_width=True):
            st.session_state[ss("mode")] = "simulation"
            st.rerun()

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# TOP NAV AND SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

mode = st.session_state[ss("mode")]
step_i = st.session_state[ss("step")]
sc = SCENARIOS[min(step_i, len(SCENARIOS) - 1)]
IS_TRAINING = mode == "training"

if mode is not None:
    col_nav_home, col_nav_spacer = st.columns([1, 5])
    with col_nav_home:
        if st.button("← Back to Treasury", use_container_width=True, type="secondary"):
            reset()
            st.switch_page("streamlit_app.py")
with st.sidebar:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    mode_label = "📖 Training Mode" if IS_TRAINING else "🎮 Simulation Mode"
    mode_color = "#047857" if IS_TRAINING else "#F59E0B"

    st.markdown(
        f'<div style="text-align:center;background:{mode_color};color:white;border-radius:8px;padding:6px;font-size:11px;font-weight:700;margin-bottom:10px;">{mode_label}</div>',
        unsafe_allow_html=True
    )

    display_step = min(step_i + 1, len(SCENARIOS))

    st.markdown(
        f'<div class="sb-metric">'
        f'<div class="sb-metric-label">Progress</div>'
        f'<div class="sb-metric-val">Step {display_step} / {len(SCENARIOS)}</div>'
        f'{dots_html(min(step_i, len(SCENARIOS) - 1), len(SCENARIOS))}'
        f'</div>',
        unsafe_allow_html=True
    )

    m = compute_metrics(st.session_state[ss("ledger")])
    hist = st.session_state[ss("history")]

    prev_reserves = hist[-2]["bank_reserves"] if len(hist) > 1 else hist[-1]["bank_reserves"]
    reserve_delta = m["bank_reserves"] - prev_reserves

    reserve_delta_html = (
        f'<div class="sb-metric-delta delta-pos">▲ +${reserve_delta} this step</div>'
        if reserve_delta > 0 else
        f'<div class="sb-metric-delta delta-neg">▼ −${abs(reserve_delta)} this step</div>'
        if reserve_delta < 0 else
        f'<div class="sb-metric-delta delta-neu">→ No reserve change</div>'
    )

    st.markdown(
        f'<div class="sb-metric">'
        f'<div class="sb-metric-label">Bank X Reserves</div>'
        f'<div class="sb-metric-val">${m["bank_reserves"]}</div>'
        f'{reserve_delta_html}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="sb-metric">'
        f'<div class="sb-metric-label">Treasury TGA</div>'
        f'<div class="sb-metric-val">${m["tga"]}</div>'
        f'<div class="sb-metric-delta delta-neu">Treasury account at the Fed</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="sb-metric">'
        f'<div class="sb-metric-label">Investor Deposits</div>'
        f'<div class="sb-metric-val">${m["deposits"]}</div>'
        f'<div class="sb-metric-delta delta-neu">Private bank money</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("↺ Restart", use_container_width=True):
            reset()

    with c2:
        if st.button("⇄ Switch Mode", use_container_width=True):
            reset()

# ─────────────────────────────────────────────────────────────────────────────
# COMPLETE SCREEN
# ─────────────────────────────────────────────────────────────────────────────

if step_i >= len(SCENARIOS):
    st.markdown(
        '<div class="complete-card">'
        '<div style="font-size:48px;margin-bottom:8px;">🎓</div>'
        '<div style="font-size:22px;font-weight:800;color:#065F46;margin-bottom:6px;">Treasury Issuance Complete!</div>'
        '<div style="font-size:14px;color:#047857;line-height:1.6;">'
        'You traced how Treasury bond issuance drains reserves from Bank X and raises the TGA.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    m = compute_metrics(st.session_state[ss("ledger")])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Final Bank X Reserves", f"${m['bank_reserves']}")

    with c2:
        st.metric("Final TGA", f"${m['tga']}")

    with c3:
        st.metric("Investor Deposits", f"${m['deposits']}")

    with c4:
        st.metric("Treasury Securities", f"${m['securities_outstanding']}")

    st.markdown("### 📊 Reserve Drain Journey")
    st.plotly_chart(
        reserve_tga_chart(st.session_state[ss("history")], height=320),
        use_container_width=True
    )

    if st.button("↺ Play Again", type="primary", use_container_width=True):
        reset()

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# STEP HEADER
# ─────────────────────────────────────────────────────────────────────────────

tag_cls = {
    "green": "tag-green",
    "red": "tag-red",
    "blue": "tag-blue",
    "gold": "tag-gold",
}[sc["tag_type"]]

header_cls = "step-header-card" if IS_TRAINING else "step-header-sim"
badge_cls = "step-badge" if IS_TRAINING else "step-badge-s"

st.markdown(
    f'<div class="{header_cls}">'
    f'<span class="{badge_cls}">{"📖 Training" if IS_TRAINING else "🎮 Simulation"} · Step {sc["id"]} of {len(SCENARIOS)}</span>'
    f'<div class="step-title">{sc["emoji"]} {sc["title"]}</div>'
    f'<div class="step-desc">{sc["short"]}</div>'
    f'<span class="tag {tag_cls}">{sc["tag"]}</span>'
    f'</div>',
    unsafe_allow_html=True
)

col_main = st.container()

with col_main:
    already_confirmed = step_i in st.session_state[ss("confirmed")]

    if sc["choice_type"] == "none":
        st.markdown(f'<div class="insight-bar">💡 {sc["insight"]}</div>', unsafe_allow_html=True)

        flow_nodes = build_flow(sc["id"], 0)
        if flow_nodes:
            st.markdown(
                f'<div class="flow-strip"><div class="flow-label">Transaction Flow</div>{flow_html(flow_nodes)}</div>',
                unsafe_allow_html=True
            )

        render_monitor(st.session_state[ss("ledger")])
        render_step_balance_sheets(st.session_state[ss("ledger")], sc["involved"])

        st.session_state[ss("confirmed")].add(step_i)

    elif IS_TRAINING:
        amt = sc["training_amt"]

        if not already_confirmed:
            st.markdown(
                f'<div style="margin:10px 0 6px 0;font-size:12px;font-weight:700;color:#4B5563;text-transform:uppercase;letter-spacing:0.5px;">Auction Amount</div>'
                f'<div class="training-amount">${amt}</div>',
                unsafe_allow_html=True
            )

            st.markdown(f'<div class="insight-bar">💡 {sc["insight"]}</div>', unsafe_allow_html=True)

            flow_nodes = build_flow(sc["id"], amt)
            if flow_nodes:
                st.markdown(
                    f'<div class="flow-strip"><div class="flow-label">Transaction Flow</div>{flow_html(flow_nodes)}</div>',
                    unsafe_allow_html=True
                )

            render_monitor(st.session_state[ss("ledger")])

            if st.button(f"✓ Apply ${amt} Issuance and Continue", type="primary", use_container_width=True):
                if not issuance_allowed(st.session_state[ss("ledger")], amt):
                    cap = get_capacity(st.session_state[ss("ledger")])
                    st.session_state[ss("blocked_msg")] = (
                        f"❌ Settlement blocked. The selected issuance amount is ${amt}, "
                        f"but the maximum available capacity is ${cap}."
                    )
                    st.rerun()

                txs = build_transactions(sc["id"], amt)
                new_ledger = apply_tx(st.session_state[ss("ledger")], txs)
                st.session_state[ss("ledger")] = new_ledger
                st.session_state[ss("chosen")][step_i] = amt
                st.session_state[ss("confirmed")].add(step_i)
                append_history(f"Step {sc['id']}", new_ledger)
                st.session_state[ss("blocked_msg")] = None
                st.rerun()

            if st.session_state[ss("blocked_msg")]:
                st.markdown(
                    f'<div class="warning-bar">{st.session_state[ss("blocked_msg")]}</div>',
                    unsafe_allow_html=True
                )

        else:
            render_monitor(st.session_state[ss("ledger")])
            render_step_balance_sheets(st.session_state[ss("ledger")], sc["involved"])

    else:
        if already_confirmed:
            render_monitor(st.session_state[ss("ledger")])
            render_step_balance_sheets(st.session_state[ss("ledger")], sc["involved"])

        else:
            st.markdown(
                f'<div class="choice-prompt">'
                f'<div class="choice-prompt-label">🎯 Make Your Choice</div>'
                f'<div class="choice-prompt-sub">{sc["sim_label"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            btn_cols = st.columns(len(sc["sim_opts"]))

            for idx, opt in enumerate(sc["sim_opts"]):
                with btn_cols[idx]:
                    is_sel = st.session_state[ss("chosen")].get(step_i) == opt

                    if st.button(
                        f"${opt}",
                        key=f"tsy_issue_opt_{step_i}_{opt}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True
                    ):
                        st.session_state[ss("chosen")][step_i] = opt
                        st.session_state[ss("blocked_msg")] = None
                        st.rerun()

            chosen_amt = st.session_state[ss("chosen")].get(step_i)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if chosen_amt is not None:
                projected_capacity = get_capacity(st.session_state[ss("ledger")])

                st.markdown(
                    f"""
                    <div class="monitor">
                        <div class="monitor-title">🧮 Projected Settlement Test</div>
                        <div class="monitor-grid">
                            <div class="monitor-box">
                                <div class="monitor-label">Chosen Issuance</div>
                                <div class="monitor-val">${chosen_amt}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Available Capacity</div>
                                <div class="monitor-val">${projected_capacity}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Projected Bank Reserves</div>
                                <div class="monitor-val">${st.session_state[ss("ledger")]["BankX"]["assets"]["Reserves"] - chosen_amt}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Projected TGA</div>
                                <div class="monitor-val">${st.session_state[ss("ledger")]["Treasury"]["assets"]["TGA"] + chosen_amt}</div>
                            </div>
                        </div>
                        <div class="monitor-note">
                            If the issuance amount exceeds available deposits or reserves, settlement is blocked.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                flow_nodes = build_flow(sc["id"], chosen_amt)
                if flow_nodes:
                    st.markdown(
                        f'<div class="flow-strip"><div class="flow-label">Projected Transaction Flow</div>{flow_html(flow_nodes)}</div>',
                        unsafe_allow_html=True
                    )

                if st.button(
                    f"✓ Confirm ${chosen_amt} Treasury Issuance",
                    key=f"tsy_issue_confirm_{step_i}",
                    type="primary",
                    use_container_width=True
                ):
                    if not issuance_allowed(st.session_state[ss("ledger")], chosen_amt):
                        cap = get_capacity(st.session_state[ss("ledger")])
                        st.session_state[ss("blocked_msg")] = (
                            f"❌ Settlement blocked. Investor A tries to buy ${chosen_amt} of Treasury securities, "
                            f"but available capacity is only ${cap}. The balance sheet is unchanged."
                        )
                        st.rerun()

                    txs = build_transactions(sc["id"], chosen_amt)
                    new_ledger = apply_tx(st.session_state[ss("ledger")], txs)

                    st.session_state[ss("ledger")] = new_ledger
                    st.session_state[ss("chosen")][step_i] = chosen_amt
                    st.session_state[ss("confirmed")].add(step_i)
                    append_history(f"Step {sc['id']}", new_ledger)
                    st.session_state[ss("blocked_msg")] = None

                    st.rerun()

                if st.session_state[ss("blocked_msg")]:
                    st.markdown(
                        f'<div class="warning-bar">{st.session_state[ss("blocked_msg")]}</div>',
                        unsafe_allow_html=True
                    )

            else:
                st.markdown(
                    '<div style="text-align:center;color:#9CA3AF;font-size:12px;padding:8px 0;">👆 Pick an auction amount above to continue</div>',
                    unsafe_allow_html=True
                )



# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

nav1, nav2 = st.columns(2)

with nav1:
    if st.button("← Back", use_container_width=True, disabled=(step_i == 0)):
        st.session_state[ss("step")] = max(0, step_i - 1)
        st.rerun()

with nav2:
    can_advance = step_i in st.session_state[ss("confirmed")]
    label = "Finish 🎓" if step_i == len(SCENARIOS) - 1 else "Next Step →"

    if st.button(label, use_container_width=True, disabled=not can_advance, type="primary"):
        st.session_state[ss("step")] = step_i + 1
        st.rerun()# Treasury Scenarios

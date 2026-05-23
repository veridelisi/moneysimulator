import streamlit as st
from copy import deepcopy

st.set_page_config(
    page_title="Deficit Spending Cycle · MoneySimulator",
    page_icon="🔁",
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

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}

/* Sidebar button */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    min-height: 54px !important;
    padding: 10px 16px !important;
    white-space: pre-line !important;
    line-height: 1.15 !important;
    font-size: 14px !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

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
.tag-blue  { background:#E6F1FB; color:#185FA5; }
.tag-red   { background:#FCEBEB; color:#A32D2D; }
.tag-gold  { background:#FEF3C7; color:#92400E; }

/* Amount */
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

/* Flow */
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
    max-width:72px;
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
.bsheet-total {
    padding:4px 9px;
    border-top:0.5px solid rgba(0,0,0,0.08);
    display:flex;
    justify-content:space-between;
    font-size:10px;
    font-weight:700;
    background:#f7f7f5;
}
.bsheet-empty {
    padding:14px;
    text-align:center;
    font-size:11px;
    color:#a0a0a0;
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

/* Info */
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

/* Monitor */
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

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .bsheet-panel-grid {
        grid-template-columns: 1fr;
    }
    .monitor-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 480px) {
    .monitor-grid {
        grid-template-columns: 1fr;
    }
    .training-amount {
        font-size:20px;
        padding:8px 16px;
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
        "title": "Opening Position — Before the Deficit Cycle",
        "short": "Investor A has deposits, Bank X has reserves, and Treasury starts with an empty TGA.",
        "insight": """
        This scenario combines two operations: Treasury issuance and Treasury spending.
        First, Treasury sells securities and pulls reserves into the TGA.
        Then Treasury spends from the TGA, sending reserves and deposits back into the private sector.
        The key question is the <strong>net reserve effect</strong>.
        """,
        "tag": "📌 Starting Point",
        "tag_type": "blue",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["InvestorA", "BankX", "CentralBank", "Treasury", "HouseholdB"],
    },
    {
        "id": 2,
        "emoji": "📜",
        "title": "Treasury Issues Securities",
        "short": "Investor A buys Treasury securities using a Bank X deposit.",
        "insight": """
        Treasury issuance drains reserves from the banking system into the TGA.
        Investor A swaps a bank deposit for a Treasury security.
        Bank X loses reserves and loses the matching deposit liability.
        Treasury receives a TGA balance and issues a security liability.
        """,
        "tag": "🔻 Reserve Drain",
        "tag_type": "red",
        "choice_type": "issuance",
        "training_amt": 300,
        "sim_opts": [100, 200, 300, 500],
        "sim_label": "How much does Treasury issue?",
        "involved": ["InvestorA", "BankX", "CentralBank", "Treasury"],
    },
    {
        "id": 3,
        "emoji": "🏛️",
        "title": "Treasury Spends from the TGA",
        "short": "Treasury spends to Household B through Bank X.",
        "insight": """
        Treasury spending draws down the TGA and injects reserves back into the banking system.
        Bank X receives reserves and credits Household B with a new deposit.
        Spending is the mirror image of issuance: <strong>TGA falls, reserves rise, and deposits rise</strong>.
        """,
        "tag": "💚 Reserve Injection",
        "tag_type": "green",
        "choice_type": "spending",
        "training_amt": 200,
        "sim_opts": [100, 200, 300, 400, 500],
        "sim_label": "How much does Treasury spend?",
        "involved": ["Treasury", "CentralBank", "BankX", "HouseholdB"],
    },
    {
        "id": 4,
        "emoji": "⚖️",
        "title": "Net Reserve Effect",
        "short": "Compare reserve drain from issuance with reserve injection from spending.",
        "insight": """
        The net reserve effect depends on the size of the operations.
        If issuance is larger than spending, reserves end lower and the TGA remains higher.
        If spending is larger than issuance, reserves end higher and the TGA falls.
        If they are equal, reserves return to the starting level.
        """,
        "tag": "📊 Net Effect",
        "tag_type": "gold",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["BankX", "CentralBank", "Treasury", "InvestorA", "HouseholdB"],
    },
    {
        "id": 5,
        "emoji": "🎓",
        "title": "Deficit Spending Cycle Review",
        "short": "Issuance, spending, and the net reserve effect.",
        "insight": """
        Deficit finance is not a single transaction. Treasury issuance first drains reserves into the TGA.
        Treasury spending later injects reserves and deposits back into the private sector.
        The final reserve level depends on whether spending is larger, smaller, or equal to issuance.
        """,
        "tag": "🎓 Complete",
        "tag_type": "green",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": ["BankX", "CentralBank", "Treasury", "InvestorA", "HouseholdB"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ENTITIES
# ─────────────────────────────────────────────────────────────────────────────

ENTITY_DEFS = {
    "InvestorA": {
        "label": "Investor A",
        "assets": {
            "Deposits": 500,
            "TreasurySecurities": 0,
        },
        "liabilities": {
            "NetWorth": 500,
        },
    },
    "HouseholdB": {
        "label": "Household B",
        "assets": {
            "Deposits": 0,
        },
        "liabilities": {
            "NetWorth": 0,
        },
    },
    "BankX": {
        "label": "Bank X",
        "assets": {
            "Reserves": 500,
        },
        "liabilities": {
            "InvestorADep": 500,
            "HouseholdBDep": 0,
        },
    },
    "CentralBank": {
        "label": "Central Bank",
        "assets": {
            "OtherAssets": 500,
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
            "FiscalBalance": 0,
        },
    },
}

ENTITY_ORDER = ["InvestorA", "HouseholdB", "BankX", "CentralBank", "Treasury"]

FRIENDLY = {
    "Deposits": "Deposits",
    "TreasurySecurities": "Treasury Securities",
    "NetWorth": "Net Worth",
    "Reserves": "Reserves",
    "InvestorADep": "Investor A Dep",
    "HouseholdBDep": "Household B Dep",
    "OtherAssets": "Other Assets",
    "BankXReserves": "Bank X Reserves",
    "TGA": "TGA",
    "FiscalBalance": "Fiscal Balance",
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

START_RESERVES = 500

def compute_metrics(state):
    current_reserves = state["BankX"]["assets"].get("Reserves", 0)
    net_reserve_effect = current_reserves - START_RESERVES

    issuance = state["Treasury"]["liabilities"].get("TreasurySecurities", 0)
    spending = state["HouseholdB"]["assets"].get("Deposits", 0)

    return {
        "bank_reserves": current_reserves,
        "tga": state["Treasury"]["assets"].get("TGA", 0),
        "investor_deposits": state["InvestorA"]["assets"].get("Deposits", 0),
        "household_deposits": state["HouseholdB"]["assets"].get("Deposits", 0),
        "securities": issuance,
        "spending": spending,
        "net_reserve_effect": net_reserve_effect,
    }

def get_issuance_capacity(state):
    investor_deposits = state["InvestorA"]["assets"].get("Deposits", 0)
    bank_reserves = state["BankX"]["assets"].get("Reserves", 0)
    return min(investor_deposits, bank_reserves)

def get_spending_capacity(state):
    return state["Treasury"]["assets"].get("TGA", 0)

def issuance_allowed(state, amt):
    return amt <= get_issuance_capacity(state)

def spending_allowed(state, amt):
    return amt <= get_spending_capacity(state)

def net_effect_label(net):
    if net > 0:
        return f"Reserve injection: +${net}"
    if net < 0:
        return f"Reserve drain: -${abs(net)}"
    return "Neutral: $0"

# ─────────────────────────────────────────────────────────────────────────────
# TRANSACTIONS
# ─────────────────────────────────────────────────────────────────────────────

def build_transactions(sc_id, amt):
    if sc_id == 2:
        return [
            ("InvestorA", "credit", "Deposits", amt),
            ("InvestorA", "debit", "TreasurySecurities", amt),

            ("BankX", "debit", "InvestorADep", amt),
            ("BankX", "credit", "Reserves", amt),

            ("CentralBank", "debit", "BankXReserves", amt),
            ("CentralBank", "credit", "TGA", amt),

            ("Treasury", "debit", "TGA", amt),
            ("Treasury", "credit", "TreasurySecurities", amt),
        ]

    if sc_id == 3:
        return [
            ("Treasury", "credit", "TGA", amt),
            ("Treasury", "debit", "FiscalBalance", amt),

            ("CentralBank", "debit", "TGA", amt),
            ("CentralBank", "credit", "BankXReserves", amt),

            ("BankX", "debit", "Reserves", amt),
            ("BankX", "credit", "HouseholdBDep", amt),

            ("HouseholdB", "debit", "Deposits", amt),
            ("HouseholdB", "credit", "NetWorth", amt),
        ]

    return []

# ─────────────────────────────────────────────────────────────────────────────
# FLOW BUILDER
# ─────────────────────────────────────────────────────────────────────────────

INV = {
    "id": "InvestorA",
    "label": "Investor A",
    "abbr": "IA",
    "bg": "#FEF3C7",
    "border": "#F59E0B",
    "color": "#92400E",
}

HHB = {
    "id": "HouseholdB",
    "label": "Household B",
    "abbr": "HB",
    "bg": "#FBEAF0",
    "border": "#D4537E",
    "color": "#72243E",
}

BX = {
    "id": "BankX",
    "label": "Bank X",
    "abbr": "BX",
    "bg": "#E6F1FB",
    "border": "#378ADD",
    "color": "#185FA5",
}

CB = {
    "id": "CentralBank",
    "label": "Central Bank",
    "abbr": "Fed",
    "bg": "#E1F5EE",
    "border": "#1D9E75",
    "color": "#0F6E56",
}

TSY = {
    "id": "Treasury",
    "label": "Treasury",
    "abbr": "Tsy",
    "bg": "#ECFDF5",
    "border": "#047857",
    "color": "#065F46",
}

def arr(amt, note):
    return {"arrow": True, "amt": amt, "note": note}

def build_flow(sc_id, amt):
    a = f"${amt}"

    if sc_id == 1:
        return [INV, arr("$500 deposit", "at Bank X"), BX, arr("$500 reserves", "at Fed"), CB]

    if sc_id == 2:
        return [
            INV,
            arr(f"{a} deposit ↓", "buys bond"),
            BX,
            arr(f"{a} reserves ↓", "to TGA"),
            CB,
            arr(f"{a} TGA ↑", "credited"),
            TSY,
        ]

    if sc_id == 3:
        return [
            TSY,
            arr(f"{a} TGA ↓", "spending"),
            CB,
            arr(f"{a} reserves ↑", "to bank"),
            BX,
            arr(f"{a} deposit ↑", "recipient"),
            HHB,
        ]

    if sc_id == 4:
        return [
            TSY,
            arr("Issuance", "drain"),
            CB,
            arr("Spending", "inject"),
            BX,
        ]

    if sc_id == 5:
        return [
            INV,
            arr("Deposit → Security", "issuance"),
            TSY,
            arr("TGA → Deposit", "spending"),
            HHB,
        ]

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
        f'<div class="col-title-l">Liabilities / Equity</div>{lr}'
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

    net = m["net_reserve_effect"]
    net_color = "#15803D" if net > 0 else "#B91C1C" if net < 0 else "#475569"

    st.markdown(
        f"""
        <div class="monitor">
            <div class="monitor-title">🔁 Deficit Cycle Monitor</div>
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
                    <div class="monitor-label">Securities Issued</div>
                    <div class="monitor-val">${m["securities"]}</div>
                </div>
                <div class="monitor-box">
                    <div class="monitor-label">Gov Spending</div>
                    <div class="monitor-val">${m["spending"]}</div>
                </div>
            </div>
            <div class="monitor-note">
                Net reserve effect from starting reserves of $500:
                <strong style="color:{net_color};">{net_effect_label(net)}</strong>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_net_effect_card(net):
    if net > 0:
        net_text = f"Reserve injection: +${net}"
        net_color = "#15803D"
        net_bg = "#DCFCE7"
    elif net < 0:
        net_text = f"Reserve drain: -${abs(net)}"
        net_color = "#B91C1C"
        net_bg = "#FEE2E2"
    else:
        net_text = "Neutral: $0"
        net_color = "#475569"
        net_bg = "#F1F5F9"

    st.markdown(
        f"""
        <div style="
            background:{net_bg};
            border:1px solid rgba(0,0,0,0.08);
            border-radius:12px;
            padding:14px 16px;
            min-height:86px;
        ">
            <div style="
                font-size:13px;
                color:#374151;
                font-weight:600;
                margin-bottom:8px;
            ">
                Net Reserve Effect
            </div>
            <div style="
                font-size:22px;
                line-height:1.2;
                color:{net_color};
                font-weight:800;
                white-space:normal;
                word-break:break-word;
            ">
                {net_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

PREFIX = "tsy_deficit_"

def ss(k):
    return PREFIX + k

for key, default in [
    ("mode", None),
    ("step", 0),
    ("ledger", None),
    ("chosen", {}),
    ("confirmed", set()),
    ("blocked_msg", None),
]:
    full = ss(key)

    if full not in st.session_state:
        st.session_state[full] = default

if st.session_state[ss("ledger")] is None:
    st.session_state[ss("ledger")] = init_state()

def reset():
    for key in ["mode", "step", "ledger", "chosen", "confirmed", "blocked_msg"]:
        full = ss(key)

        if full in st.session_state:
            del st.session_state[full]

    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# MODE SELECTION
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state[ss("mode")] is None:
    if st.button("← Back to Home", use_container_width=False):
        st.switch_page("streamlit_app.py")

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;margin-bottom:2rem;'>
            <div style='font-size:2rem;font-weight:800;color:#064E3B;'>🔁 Deficit Spending Cycle</div>
            <div style='font-size:1rem;color:#6b6b6b;margin-top:6px;'>
                Issuance, spending, and the net reserve effect
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
                Fixed issuance and spending amounts.<br>
                Watch the net reserve effect.
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
            <div class="mode-title">Choose the Cycle Size</div>
            <div class="mode-sub">
                Pick issuance and spending amounts.<br>
                Compare the final reserve effect.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Start Simulation →", use_container_width=True):
            st.session_state[ss("mode")] = "simulation"
            st.rerun()

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# NAV AND SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

mode = st.session_state[ss("mode")]
step_i = st.session_state[ss("step")]
sc = SCENARIOS[min(step_i, len(SCENARIOS) - 1)]
IS_TRAINING = mode == "training"

if mode is not None:
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] div[data-testid="column"]:first-child button {
        min-height: 62px !important;
        padding: 10px 12px !important;
        white-space: pre-line !important;
        line-height: 1.15 !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_nav_home, col_nav_spacer = st.columns([2.4, 5.6])

    with col_nav_home:
        if st.button("← Back\nto Treasury Deficit", use_container_width=True, type="secondary"):
            reset()
            st.switch_page("streamlit_app.py")

with st.sidebar:
    if st.button("← Back\nto Home", use_container_width=True):
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
    net = m["net_reserve_effect"]
    delta_cls = "delta-pos" if net > 0 else "delta-neg" if net < 0 else "delta-neu"

    st.markdown(
        f'<div class="sb-metric">'
        f'<div class="sb-metric-label">Bank X Reserves</div>'
        f'<div class="sb-metric-val">${m["bank_reserves"]}</div>'
        f'<div class="sb-metric-delta {delta_cls}">{net_effect_label(net)}</div>'
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
        f'<div class="sb-metric-label">Securities Issued</div>'
        f'<div class="sb-metric-val">${m["securities"]}</div>'
        f'<div class="sb-metric-delta delta-neu">Treasury liabilities</div>'
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
        '<div style="font-size:22px;font-weight:800;color:#065F46;margin-bottom:6px;">Deficit Cycle Complete!</div>'
        '<div style="font-size:14px;color:#047857;line-height:1.6;">'
        'You traced issuance, spending, and the final net reserve effect.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    m = compute_metrics(st.session_state[ss("ledger")])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Final Reserves", f"${m['bank_reserves']}")

    with c2:
        st.metric("Final TGA", f"${m['tga']}")

    with c3:
        st.metric("Securities Issued", f"${m['securities']}")

    with c4:
        render_net_effect_card(m["net_reserve_effect"])

    if st.button("↺ Play Again", type="primary", use_container_width=True):
        reset()

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# STEP HEADER
# ─────────────────────────────────────────────────────────────────────────────

tag_cls = {
    "green": "tag-green",
    "blue": "tag-blue",
    "red": "tag-red",
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

# ─────────────────────────────────────────────────────────────────────────────
# MAIN STEP LOGIC
# ─────────────────────────────────────────────────────────────────────────────

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
            label = "Treasury Issuance Amount" if sc["choice_type"] == "issuance" else "Government Spending Amount"

            st.markdown(
                f'<div style="margin:10px 0 6px 0;font-size:12px;font-weight:700;color:#4B5563;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>'
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

            button_text = "✓ Apply Treasury Issuance and Continue" if sc["choice_type"] == "issuance" else "✓ Apply Government Spending and Continue"

            if st.button(f"{button_text} (${amt})", type="primary", use_container_width=True):
                current_state = st.session_state[ss("ledger")]

                if sc["choice_type"] == "issuance" and not issuance_allowed(current_state, amt):
                    cap = get_issuance_capacity(current_state)
                    st.session_state[ss("blocked_msg")] = (
                        f"❌ Issuance blocked. Treasury tries to issue ${amt}, "
                        f"but settlement capacity is only ${cap}."
                    )
                    st.rerun()

                if sc["choice_type"] == "spending" and not spending_allowed(current_state, amt):
                    cap = get_spending_capacity(current_state)
                    st.session_state[ss("blocked_msg")] = (
                        f"❌ Spending blocked. Treasury tries to spend ${amt}, "
                        f"but the TGA balance is only ${cap}."
                    )
                    st.rerun()

                txs = build_transactions(sc["id"], amt)
                new_ledger = apply_tx(current_state, txs)

                st.session_state[ss("ledger")] = new_ledger
                st.session_state[ss("chosen")][step_i] = amt
                st.session_state[ss("confirmed")].add(step_i)
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
        # ── SIMULATION MODE ──
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

            current_state = st.session_state[ss("ledger")]

            available_opts = sc["sim_opts"]

            if sc["choice_type"] == "issuance":
                capacity = get_issuance_capacity(current_state)
                available_opts = [x for x in sc["sim_opts"] if x <= capacity]

                if not available_opts and capacity > 0:
                    available_opts = [capacity]

            elif sc["choice_type"] == "spending":
                capacity = get_spending_capacity(current_state)
                available_opts = [x for x in sc["sim_opts"] if x <= capacity]

                if not available_opts and capacity > 0:
                    available_opts = [capacity]

            if not available_opts:
                st.markdown(
                    '<div class="warning-bar">❌ No valid amount is available for this step. The transaction cannot settle.</div>',
                    unsafe_allow_html=True
                )

            else:
                btn_cols = st.columns(len(available_opts))

                for idx, opt in enumerate(available_opts):
                    with btn_cols[idx]:
                        is_sel = st.session_state[ss("chosen")].get(step_i) == opt

                        if st.button(
                            f"${opt}",
                            key=f"tsy_deficit_opt_{step_i}_{opt}",
                            type="primary" if is_sel else "secondary",
                            use_container_width=True
                        ):
                            st.session_state[ss("chosen")][step_i] = opt
                            st.session_state[ss("blocked_msg")] = None
                            st.rerun()

            chosen_amt = st.session_state[ss("chosen")].get(step_i)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if chosen_amt is not None:
                current_state = st.session_state[ss("ledger")]
                current_reserves = current_state["BankX"]["assets"]["Reserves"]
                current_tga = current_state["Treasury"]["assets"]["TGA"]

                if sc["choice_type"] == "issuance":
                    projected_reserves = current_reserves - chosen_amt
                    projected_tga = current_tga + chosen_amt
                    action_label = "Projected Treasury Issuance"
                    capacity = get_issuance_capacity(current_state)
                    confirm_label = "Treasury Issuance"

                elif sc["choice_type"] == "spending":
                    projected_reserves = current_reserves + chosen_amt
                    projected_tga = current_tga - chosen_amt
                    action_label = "Projected Government Spending"
                    capacity = get_spending_capacity(current_state)
                    confirm_label = "Government Spending"

                else:
                    projected_reserves = current_reserves
                    projected_tga = current_tga
                    action_label = "Projected Transaction"
                    capacity = 0
                    confirm_label = "Transaction"

                projected_net = projected_reserves - START_RESERVES

                st.markdown(
                    f"""
                    <div class="monitor">
                        <div class="monitor-title">🧮 {action_label}</div>
                        <div class="monitor-grid">
                            <div class="monitor-box">
                                <div class="monitor-label">Chosen Amount</div>
                                <div class="monitor-val">${chosen_amt}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Available Capacity</div>
                                <div class="monitor-val">${capacity}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Projected Reserves</div>
                                <div class="monitor-val">${projected_reserves}</div>
                            </div>
                            <div class="monitor-box">
                                <div class="monitor-label">Projected TGA</div>
                                <div class="monitor-val">${projected_tga}</div>
                            </div>
                        </div>
                        <div class="monitor-note">
                            Projected net reserve effect from starting reserves of $500:
                            <strong>{net_effect_label(projected_net)}</strong>.
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
                    f"✓ Confirm ${chosen_amt} {confirm_label}",
                    key=f"tsy_deficit_confirm_{step_i}",
                    type="primary",
                    use_container_width=True
                ):
                    if sc["choice_type"] == "issuance":
                        if not issuance_allowed(current_state, chosen_amt):
                            cap = get_issuance_capacity(current_state)
                            st.session_state[ss("blocked_msg")] = (
                                f"❌ Issuance blocked. Treasury tries to issue ${chosen_amt}, "
                                f"but settlement capacity is only ${cap}. The balance sheet is unchanged."
                            )
                            st.rerun()

                    elif sc["choice_type"] == "spending":
                        if not spending_allowed(current_state, chosen_amt):
                            cap = get_spending_capacity(current_state)
                            st.session_state[ss("blocked_msg")] = (
                                f"❌ Spending blocked. Treasury tries to spend ${chosen_amt}, "
                                f"but the TGA balance is only ${cap}. The balance sheet is unchanged."
                            )
                            st.rerun()

                    txs = build_transactions(sc["id"], chosen_amt)
                    new_ledger = apply_tx(current_state, txs)

                    st.session_state[ss("ledger")] = new_ledger
                    st.session_state[ss("chosen")][step_i] = chosen_amt
                    st.session_state[ss("confirmed")].add(step_i)
                    st.session_state[ss("blocked_msg")] = None

                    st.rerun()

                if st.session_state[ss("blocked_msg")]:
                    st.markdown(
                        f'<div class="warning-bar">{st.session_state[ss("blocked_msg")]}</div>',
                        unsafe_allow_html=True
                    )

            else:
                st.markdown(
                    '<div style="text-align:center;color:#9CA3AF;font-size:12px;padding:8px 0;">👆 Pick an amount above to continue</div>',
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
        st.rerun()
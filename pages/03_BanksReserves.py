import streamlit as st
import plotly.graph_objects as go
from copy import deepcopy

st.set_page_config(
    page_title="Reserve Transfer · MoneySimulator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------- STOP Expanded -----------------
st.markdown(
    """
<style>
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}
</style>
""",
    unsafe_allow_html=True,
)

# ─── TOP NAV ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.nav-container { display: flex; gap: 0.5rem; justify-content: center; }
</style>
<div class="nav-container">
</div>
""", unsafe_allow_html=True)



# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Syne', 'Segoe UI', sans-serif !important;
}
.block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; }


.sb-metric { background:white; border:0.5px solid rgba(0,0,0,0.12); border-radius:8px; padding:10px 12px; margin-bottom:7px; }
.sb-metric-label { font-size:10px; color:#6b6b6b; text-transform:uppercase; letter-spacing:0.5px; }
.sb-metric-val   { font-size:22px; font-weight:700; color:#1a1a1a; margin-top:1px; }
.sb-metric-delta { font-size:11px; margin-top:1px; }
.delta-pos { color:#1D9E75; } .delta-neg { color:#D85A30; } .delta-neu { color:#a0a0a0; }

.dots-row { display:flex; gap:5px; flex-wrap:wrap; margin-top:4px; }
.dot-done   { width:12px;height:12px;border-radius:50%;background:#1D9E75;display:inline-block; }
.dot-active { width:12px;height:12px;border-radius:50%;background:#378ADD;outline:2px solid #B5D4F4;outline-offset:1px;display:inline-block; }
.dot-empty  { width:12px;height:12px;border-radius:50%;background:rgba(0,0,0,0.12);display:inline-block; }

.mode-card {
    border-radius:14px; padding:24px 28px; text-align:center; cursor:pointer;
    border:2px solid transparent; transition:all 0.2s;
}
.mode-card-training  { background:#EEF2FF; border-color:#C7D2FE; }
.mode-card-sim       { background:#FFFBEB; border-color:#FCD34D; }
.mode-title   { font-size:18px; font-weight:800; color:#1E1B4B; margin:10px 0 6px 0; }
.mode-sub     { font-size:12px; color:#4B5563; line-height:1.5; }
.mode-badge-t { display:inline-block; background:#6366F1; color:white; font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; margin-bottom:8px; }
.mode-badge-s { display:inline-block; background:#F59E0B; color:white; font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; margin-bottom:8px; }

.step-header-card { background:#EEF2FF; border:1px solid #C7D2FE; border-radius:12px; padding:16px 20px; margin-bottom:10px; }
.step-header-sim  { background:#FFFBEB; border:1px solid #FCD34D; border-radius:12px; padding:16px 20px; margin-bottom:10px; }
.step-badge   { background:#E6F1FB; color:#185FA5; font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; display:inline-block; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px; }
.step-badge-s { background:#FEF3C7; color:#92400E; font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; display:inline-block; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px; }
.step-title { font-size:17px; font-weight:700; color:#1E1B4B; margin-bottom:4px; }
.step-desc  { font-size:13px; color:#4B5563; line-height:1.6; }
.tag { display:inline-block; font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; margin-top:7px; }
.tag-green { background:#EAF3DE; color:#3B6D11; }
.tag-red   { background:#FCEBEB; color:#A32D2D; }
.tag-blue  { background:#E6F1FB; color:#185FA5; }

.training-amount {
    background:#6366F1; color:white; font-size:28px; font-weight:800;
    padding:12px 28px; border-radius:12px; display:inline-block; margin:12px 0;
}
.flow-strip { background:#f7f7f5; border:0.5px solid rgba(0,0,0,0.10); border-radius:10px; padding:12px 16px; margin-bottom:10px; }
.flow-label { font-size:10px; color:#a0a0a0; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:10px; }
.flow-row { display:flex; align-items:center; flex-wrap:wrap; row-gap:8px; }
.flow-node { display:flex; flex-direction:column; align-items:center; gap:4px; }
.flow-circle { width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid; }
.flow-node-lbl { font-size:9px; color:#6b6b6b; text-align:center; max-width:54px; line-height:1.3; }
.flow-arrow { display:flex; flex-direction:column; align-items:center; padding:0 6px; }
.flow-amt  { font-size:9px; color:#6b6b6b; font-weight:700; }
.flow-line { height:2px; width:38px; background:rgba(0,0,0,0.2); position:relative; margin:2px 0; }
.flow-line::after { content:''; position:absolute; right:-5px; top:-4px; border-top:5px solid transparent; border-bottom:5px solid transparent; border-left:7px solid rgba(0,0,0,0.2); }
.flow-note { font-size:9px; color:#a0a0a0; }

.bsheet { border:0.5px solid rgba(0,0,0,0.12); border-radius:8px; overflow:hidden; margin-bottom:8px; }
.bsheet.active { border:1.5px solid #378ADD; }
.bsheet-head { padding:6px 10px; display:flex; align-items:center; justify-content:space-between; border-bottom:0.5px solid rgba(0,0,0,0.08); background:#f7f7f5; }
.bsheet-name { font-size:12px; font-weight:700; color:#1a1a1a; }
.bsheet-active-badge { font-size:9px; background:#E6F1FB; color:#185FA5; padding:1px 7px; border-radius:10px; font-weight:700; }
.bsheet-body { display:grid; grid-template-columns:1fr 1fr; }
.bsheet-col { padding:7px 9px; }
.bsheet-col-left { border-right:0.5px solid rgba(0,0,0,0.08); }
.col-title-a { font-size:9px; text-transform:uppercase; letter-spacing:0.4px; color:#185FA5; font-weight:700; margin-bottom:4px; }
.col-title-l { font-size:9px; text-transform:uppercase; letter-spacing:0.4px; color:#A32D2D; font-weight:700; margin-bottom:4px; }
.bsheet-row { display:flex; justify-content:space-between; align-items:center; font-size:10px; color:#6b6b6b; padding:2px 0; gap:4px; }
.bsheet-row .bval { font-weight:700; color:#1a1a1a; white-space:nowrap; }
.bsheet-empty { padding:14px; text-align:center; font-size:11px; color:#a0a0a0; }
.bsheet-total { padding:4px 9px; border-top:0.5px solid rgba(0,0,0,0.08); display:flex; justify-content:space-between; font-size:10px; font-weight:700; background:#f7f7f5; }
.t-a { color:#185FA5; } .t-l { color:#A32D2D; }

.insight-bar { background:#EAF3DE; border-radius:8px; padding:10px 14px; font-size:12px; color:#3B6D11; line-height:1.6; margin:4px 0 10px 0; }
.choice-prompt { background:#FFFBEB; border:1px solid #FCD34D; border-radius:10px; padding:12px 16px; margin-bottom:12px; }
.choice-prompt-label { font-size:12px; font-weight:700; color:#92400E; margin-bottom:2px; }
.choice-prompt-sub   { font-size:11px; color:#B45309; }
.chosen-pill { display:inline-block; background:#1E40AF; color:white; font-size:13px; font-weight:700; padding:4px 14px; border-radius:20px; margin-bottom:8px; }
.complete-card { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); border:1px solid #86EFAC; border-radius:14px; padding:28px 32px; text-align:center; margin-bottom:16px; }

.bsheet-panel {
    background:#ffffff;
    border:0.5px solid rgba(0,0,0,0.10);
    border-radius:12px;
    padding:14px 16px;
    margin-top:12px;
}
.bsheet-panel-title {
    font-size:12px;
    font-weight:800;
    color:#1E1B4B;
    text-transform:uppercase;
    letter-spacing:0.5px;
    margin-bottom:10px;
}
.bsheet-panel-grid {
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap:12px;
}
.bsheet-stage-title {
    font-size:11px;
    font-weight:800;
    color:#475569;
    margin-bottom:8px;
    text-transform:uppercase;
    letter-spacing:0.4px;
}
.delta-chip {
    display:inline-block;
    font-size:10px;
    font-weight:800;
    border-radius:999px;
    padding:3px 8px;
    margin-left:6px;
}
.delta-up   { background:#DCFCE7; color:#166534; }
.delta-down { background:#FEE2E2; color:#991B1B; }
.delta-flat { background:#E5E7EB; color:#374151; }

.entity-delta-box {
    background:#fff;
    border:1px dashed rgba(0,0,0,0.10);
    border-radius:10px;
    padding:10px 12px;
    margin-top:10px;
    margin-bottom:12px;
}
.entity-delta-title {
    font-size:11px;
    font-weight:800;
    color:#334155;
    margin-bottom:6px;
    text-transform:uppercase;
    letter-spacing:0.4px;
}
.entity-delta-row {
    display:flex;
    justify-content:space-between;
    gap:8px;
    font-size:11px;
    padding:3px 0;
}
.entity-delta-name { color:#475569; }
.entity-delta-val.up { color:#15803D; font-weight:800; }
.entity-delta-val.down { color:#B91C1C; font-weight:800; }
.entity-delta-val.flat { color:#6B7280; font-weight:700; }

/* Mobile Responsive Design */
@media (max-width: 768px) {
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    

    
    .step-title { font-size:15px; }
    .step-desc { font-size:12px; }
    
    .training-amount { font-size:24px; padding:10px 20px; }
    
    .flow-circle { width:40px; height:40px; font-size:10px; }
    .flow-node-lbl { font-size:8px; max-width:48px; }
    
    .bsheet-body { grid-template-columns:1fr 1fr; }
    .bsheet-col-left { border-right:none; border-bottom:0.5px solid rgba(0,0,0,0.08); }
    
    .bsheet-panel-grid { grid-template-columns: 1fr; }
    
    .choice-prompt { padding:10px 14px; font-size:11px; }
    .mode-card { padding:18px 20px; }
    .mode-title { font-size:16px; }
    .mode-sub { font-size:11px; }

    .bsheet-head { padding:5px 8px; }
    .bsheet-name { font-size:11px; }
    .bsheet-active-badge { font-size:8px; padding:1px 6px; }
    .bsheet-col { padding:6px 7px; }
    .col-title-a, .col-title-l { font-size:8px; margin-bottom:3px; }
    .bsheet-row { font-size:9px; gap:3px; }
    .bsheet-row .bval { font-size:9px; }
    .bsheet-total { font-size:9px; padding:4px 7px; }
}

@media (max-width: 480px) {
    .step-header-card, .step-header-sim { padding:12px 16px; margin-bottom:8px; }
    .step-badge, .step-badge-s { font-size:9px; padding:2px 8px; }
    .step-title { font-size:14px; margin-bottom:3px; }
    .step-desc { font-size:11px; line-height:1.4; }
    
    .training-amount { font-size:20px; padding:8px 16px; margin:8px 0; }
    
    .flow-strip { padding:10px 12px; margin-bottom:8px; }
    .flow-label { font-size:9px; }
    .flow-circle { width:36px; height:36px; font-size:9px; }
    .flow-node-lbl { font-size:7px; max-width:44px; }
    
    .insight-bar { padding:8px 12px; font-size:11px; }
    
    .choice-prompt { padding:9px 12px; font-size:10px; margin-bottom:10px; }
    .choice-prompt-label { font-size:11px; }
    .choice-prompt-sub { font-size:10px; }
    
    .tag { font-size:10px; padding:2px 8px; margin-top:5px; }
    
    .sb-metric { padding:8px 10px; margin-bottom:6px; }
    .sb-metric-val { font-size:18px; }
    .sb-metric-label { font-size:9px; }
    
    .mode-card { padding:14px 16px; }
    .mode-title { font-size:15px; margin:8px 0 4px 0; }
    .mode-sub { font-size:10px; }
    
    .complete-card { padding:20px 24px; }

    .bsheet-name { font-size:10px; }
    .bsheet-col { padding:5px 6px; }
    .col-title-a, .col-title-l { font-size:7px; }
    .bsheet-row { font-size:8px; }
    .bsheet-row .bval { font-size:8px; }
    .bsheet-total { font-size:8px; }
}

</style>
""", unsafe_allow_html=True)


# ─── SCENARIOS ────────────────────────────────────────────────────────────────
# training_amt: fixed amount used in training mode
# sim_opts: choices shown in simulation mode
SCENARIOS = [
    {
        "id": 1, "emoji": "✨",
        "title": "Bank X Grants a Loan to Customer A",
        "short": "Bank X approves Customer A's loan and creates a matching deposit on its own balance sheet.",
        "insight": "Bank X does not lend out pre-existing deposits. It expands both sides of its balance sheet at once: a <strong>Loan</strong> asset and a <strong>Customer A Deposit</strong> liability. Customer A receives new purchasing power.",
        "tag": "💚 Money Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 200,
        "sim_opts": [100, 200, 300, 400],
        "sim_label": "How much does Bank X loan to Customer A?",
        "involved": ["BankX", "CustomerA"],
    },
    {
        "id": 2, "emoji": "💳",
        "title": "Bank Y Grants a Loan to Customer B",
        "short": "Bank Y grants Customer B a loan and creates a new deposit for Customer B.",
        "insight": "Bank Y creates money in the same way. It records a <strong>Loan</strong> on the asset side and a <strong>Customer B Deposit</strong> on the liability side. This is a second independent credit-creation event.",
        "tag": "💚 Money Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 150,
        "sim_opts": [100, 150, 200, 300],
        "sim_label": "How much does Bank Y loan to Customer B?",
        "involved": ["BankY", "CustomerB"],
    },
    {
        "id": 3, "emoji": "🏦",
        "title": "Bank X Grants a Loan to Customer C",
        "short": "Bank X also grants Customer C a loan, creating another deposit inside Bank X.",
        "insight": "Bank X now has two deposit customers. The loan to Customer C creates a new <strong>Customer C Deposit</strong> liability. No reserves are required for this same-bank money creation event.",
        "tag": "💚 Money Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 120,
        "sim_opts": [80, 120, 180, 240],
        "sim_label": "How much does Bank X loan to Customer C?",
        "involved": ["BankX", "CustomerC"],
    },
    {
        "id": 4, "emoji": "🏛️",
        "title": "Central Bank Provides Reserves to Both Banks",
        "short": "The Central Bank provides reserves to Bank X and Bank Y for settlement capacity.",
        "insight": "Reserves are the <strong>settlement currency between banks</strong>. They sit on the Central Bank's ledger. They do not enter customer deposits directly, but they allow banks to settle payments across banks.",
        "tag": "➡️ No M1 Change", "tag_type": "blue",
        "choice_type": "reserve",
        "training_amt": 300,
        "sim_opts": [200, 300, 400, 500],
        "sim_label": "How much in reserves does the Central Bank provide to each bank?",
        "involved": ["BankX", "BankY", "CentralBank"],
    },
    {
        "id": 5, "emoji": "🔁",
        "title": "Customer A Sends Money to Customer C — Same Bank Transfer",
        "short": "Customer A pays Customer C. Both customers are at Bank X, so only Bank X's deposit liabilities shift.",
        "insight": "This is a <strong>same-bank transfer</strong>. Bank X reduces Customer A's deposit and increases Customer C's deposit. No reserves move, because the payment stays inside Bank X. Total M1 is unchanged.",
        "tag": "➡️ No M1 Change", "tag_type": "blue",
        "choice_type": "transfer_same",
        "training_amt": 50,
        "sim_opts": [20, 50, 80, 100],
        "sim_label": "How much does Customer A send to Customer C?",
        "involved": ["BankX", "CustomerA", "CustomerC"],
    },
    {
        "id": 6, "emoji": "⚡",
        "title": "Customer B Sends Money to Customer A — Interbank Reserve Transfer",
        "short": "Customer B pays Customer A. The payment crosses from Bank Y to Bank X, so reserves must move.",
        "insight": "This is an <strong>interbank transfer</strong>. Customer B's deposit at Bank Y falls and Customer A's deposit at Bank X rises. To settle the payment, Bank Y transfers reserves to Bank X through the Central Bank. Total M1 is unchanged, but reserves shift between banks.",
        "tag": "➡️ No M1 Change", "tag_type": "blue",
        "choice_type": "transfer_interbank",
        "training_amt": 70,
        "sim_opts": [30, 70, 100, 130],
        "sim_label": "How much does Customer B send to Customer A?",
        "involved": ["BankX", "BankY", "CentralBank", "CustomerA", "CustomerB"],
    },
    {
        "id": 7, "emoji": "🎓",
        "title": "Reserve Transfer Review",
        "short": "Review the difference between same-bank deposit transfers and interbank reserve settlement.",
        "insight": "Same-bank transfers only rearrange deposit liabilities inside one bank. Interbank transfers require reserve settlement between banks. Loans create deposits; transfers move deposits; reserves settle payments across banks.",
        "tag": "🎓 Complete!", "tag_type": "green",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": [],
    },
]

# ─── ENTITIES ─────────────────────────────────────────────────────────────────
ENTITY_DEFS = {
    "BankX":       {"label": "Bank X",       "assets": {"Loans":0,"Reserves":0,"Cash":0},    "liabilities": {"CustADep":0,"CustCDep":0,"DueCB":0}},
    "BankY":       {"label": "Bank Y",       "assets": {"Loans":0,"Reserves":0,"Cash":0},    "liabilities": {"CustBDep":0,"DueCB":0}},
    "CentralBank": {"label": "Central Bank", "assets": {"LoansToBanks":0},                   "liabilities": {"Reserves":0,"Cash":0}},
    "CustomerA":   {"label": "Customer A",   "assets": {"Deposits":0,"Cash":0},              "liabilities": {"Loans":0}},
    "CustomerB":   {"label": "Customer B",   "assets": {"Deposits":0,"Cash":0},              "liabilities": {"Loans":0}},
    "CustomerC":   {"label": "Customer C",   "assets": {"Deposits":0,"Cash":0},              "liabilities": {"Loans":0}},
}
ENTITY_ORDER = ["BankX","BankY","CentralBank","CustomerA","CustomerB","CustomerC"]
FRIENDLY = {
    "CustADep":"Cust A Dep","CustBDep":"Cust B Dep","CustCDep":"Cust C Dep",
    "DueCB":"Due to CB","LoansToBanks":"Loans→Banks",
}
def fname(k): return FRIENDLY.get(k, k)

def init_state():
    return {k: {"assets": dict(v["assets"]), "liabilities": dict(v["liabilities"])} for k, v in ENTITY_DEFS.items()}

def apply_tx(state, txs):
    s = deepcopy(state)
    for entity, side, account, amount in txs:
        e = s[entity]
        if side == "debit":
            if account in e["assets"]:        e["assets"][account]      += amount
            elif account in e["liabilities"]: e["liabilities"][account] -= amount
        else:
            if account in e["assets"]:        e["assets"][account]      -= amount
            elif account in e["liabilities"]: e["liabilities"][account] += amount
    return s

def compute_ms(state):
    bank_deps = (state["BankX"]["liabilities"].get("CustADep",0)
               + state["BankX"]["liabilities"].get("CustCDep",0)
               + state["BankY"]["liabilities"].get("CustBDep",0))
    cash = (state["CustomerA"]["assets"].get("Cash",0)
          + state["CustomerB"]["assets"].get("Cash",0)
          + state["CustomerC"]["assets"].get("Cash",0))
    return bank_deps, cash, bank_deps + cash

# ─── TRANSACTION BUILDERS ─────────────────────────────────────────────────────
def build_transactions(sc_id, amt):
    if sc_id == 1:
        # Bank X creates a loan for Customer A.
        return [
            ("BankX","debit","Loans",amt), ("BankX","credit","CustADep",amt),
            ("CustomerA","debit","Deposits",amt), ("CustomerA","credit","Loans",amt),
        ]
    elif sc_id == 2:
        # Bank Y creates a loan for Customer B.
        return [
            ("BankY","debit","Loans",amt), ("BankY","credit","CustBDep",amt),
            ("CustomerB","debit","Deposits",amt), ("CustomerB","credit","Loans",amt),
        ]
    elif sc_id == 3:
        # Bank X creates a loan for Customer C.
        return [
            ("BankX","debit","Loans",amt), ("BankX","credit","CustCDep",amt),
            ("CustomerC","debit","Deposits",amt), ("CustomerC","credit","Loans",amt),
        ]
    elif sc_id == 4:
        # Central Bank provides reserves to both banks.
        return [
            ("BankX","debit","Reserves",amt), ("BankX","credit","DueCB",amt),
            ("BankY","debit","Reserves",amt), ("BankY","credit","DueCB",amt),
            ("CentralBank","debit","LoansToBanks",amt*2), ("CentralBank","credit","Reserves",amt*2),
        ]
    elif sc_id == 5:
        # Customer A pays Customer C inside Bank X: deposits shift, no reserves move.
        return [
            ("BankX","debit","CustADep",amt), ("BankX","credit","CustCDep",amt),
            ("CustomerA","credit","Deposits",amt),
            ("CustomerC","debit","Deposits",amt),
        ]
    elif sc_id == 6:
        # Customer B pays Customer A across banks: deposits shift and reserves settle.
        return [
            ("BankY","debit","CustBDep",amt), ("BankY","credit","Reserves",amt),
            ("BankX","debit","Reserves",amt), ("BankX","credit","CustADep",amt),
            ("CustomerB","credit","Deposits",amt),
            ("CustomerA","debit","Deposits",amt),
        ]
    return []

# ─── FLOW BUILDER ─────────────────────────────────────────────────────────────
BX  = {"id":"BankX",      "label":"Bank X",      "abbr":"BX", "bg":"#E6F1FB","border":"#378ADD","color":"#185FA5"}
BY  = {"id":"BankY",      "label":"Bank Y",      "abbr":"BY", "bg":"#EAF3DE","border":"#1D9E75","color":"#3B6D11"}
CB  = {"id":"CentralBank","label":"Central Bank","abbr":"FED", "bg":"#E1F5EE","border":"#1D9E75","color":"#0F6E56"}
CA  = {"id":"CustomerA",  "label":"Customer A",  "abbr":"A", "bg":"#FAEEDA","border":"#EF9F27","color":"#854F0B"}
CUSTB = {"id":"CustomerB",  "label":"Customer B",  "abbr":"B", "bg":"#FBEAF0","border":"#D4537E","color":"#72243E"}
CC  = {"id":"CustomerC",  "label":"Customer C",  "abbr":"C", "bg":"#F3E8FF","border":"#A855F7","color":"#581C87"}

def arr(amt, note): return {"arrow":True,"amt":amt,"note":note}

def build_flow(sc_id, amt):
    a = f"${amt}"
    if sc_id == 1: return [BX, arr(f"{a} loan","creates ↗"), CA]
    elif sc_id == 2: return [BY, arr(f"{a} loan","creates ↗"), CUSTB]
    elif sc_id == 3: return [BX, arr(f"{a} loan","creates ↗"), CC]
    elif sc_id == 4: return [CB, arr(f"{a} each","reserves"), BX, BY]
    elif sc_id == 5: return [CA, arr(f"{a} deposit","inside BX"), BX, arr(f"{a} deposit","same bank"), CC]
    elif sc_id == 6: return [CUSTB, BY, arr(f"{a} reserves","via FED"), CB, arr(f"{a} reserves","settled"), BX, CA]
    return []

# ─── RENDER HELPERS ───────────────────────────────────────────────────────────
def dots_html(current, total):
    parts = []
    for i in range(total):
        cls = "dot-done" if i < current else ("dot-active" if i == current else "dot-empty")
        parts.append(f'<span class="{cls}"></span>')
    return f'<div class="dots-row">{"".join(parts)}</div>'

def flow_html(nodes):
    if not nodes: return ""
    parts = []
    for n in nodes:
        if n.get("id"):
            parts.append(
                f'<div class="flow-node">'
                f'<div class="flow-circle" style="background:{n["bg"]};border-color:{n["border"]};color:{n["color"]};">{n["abbr"]}</div>'
                f'<div class="flow-node-lbl">{n["label"]}</div></div>'
            )
        elif n.get("arrow"):
            parts.append(
                f'<div class="flow-arrow">'
                f'<div class="flow-amt">{n["amt"]}</div>'
                f'<div class="flow-line"></div>'
                f'<div class="flow-note">{n.get("note","")}</div></div>'
            )
    return f'<div class="flow-row">{"".join(parts)}</div>'

def bsheet_html(ek, state, active):
    e = state[ek]
    label = ENTITY_DEFS[ek]["label"]
    assets = [(k,v) for k,v in e["assets"].items() if v != 0]
    liabs  = [(k,v) for k,v in e["liabilities"].items() if v != 0]
    ta = sum(v for _,v in assets)
    tl = sum(v for _,v in liabs)
    if ta == 0 and tl == 0:
        return (f'<div class="bsheet"><div class="bsheet-head">'
                f'<span class="bsheet-name" style="color:#a0a0a0;">{label}</span></div>'
                f'<div class="bsheet-empty">empty</div></div>')
    badge = '<span class="bsheet-active-badge">active</span>' if active else ""
    acls  = " active" if active else ""
    ar = "".join(f'<div class="bsheet-row"><span>{fname(k)}</span><span class="bval">${v}</span></div>' for k,v in assets) \
         or '<div class="bsheet-row" style="color:#ccc;font-size:10px;">—</div>'
    lr = "".join(f'<div class="bsheet-row"><span>{fname(k)}</span><span class="bval">${v}</span></div>' for k,v in liabs) \
         or '<div class="bsheet-row" style="color:#ccc;font-size:10px;">—</div>'
    tl_str = f"-${abs(tl)}" if tl < 0 else f"${tl}"
    return (f'<div class="bsheet{acls}"><div class="bsheet-head"><span class="bsheet-name">{label}</span>{badge}</div>'
            f'<div class="bsheet-body">'
            f'<div class="bsheet-col bsheet-col-left"><div class="col-title-a">Assets</div>{ar}</div>'
            f'<div class="bsheet-col"><div class="col-title-l">Liabilities</div>{lr}</div>'
            f'</div><div class="bsheet-total"><span class="t-a">${ta}</span><span class="t-l">{tl_str}</span></div></div>')



def render_step_balance_sheets(state, involved_entities):
    if not involved_entities:
        return

    blocks = "".join(bsheet_html(ek, state, True) for ek in involved_entities)
    st.markdown(
        f'<div class="bsheet-panel"><div class="bsheet-panel-grid">{blocks}</div></div>',
        unsafe_allow_html=True
    )


def ms_chart(history, height=240):
    labels = [d["label"] for d in history]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=[d["bank"] for d in history], name="Bank Deposits", marker_color="#85B7EB"))
    fig.add_trace(go.Bar(x=labels, y=[d["cash"] for d in history], name="Cash in Circ.", marker_color="#C084FC"))
    fig.add_trace(go.Scatter(x=labels, y=[d["total"] for d in history], name="Total M1", mode="lines+markers",
                             line=dict(color="#EF9F27", width=3, shape="spline"),
                             marker=dict(size=8, color="#EF9F27", line=dict(width=2, color="white"))))
    if history:
        last = history[-1]
        fig.add_annotation(x=last["label"], y=last["total"], text=f"<b>${last['total']}</b>",
                           showarrow=False, yshift=14, font=dict(size=12, color="#D97706"),
                           bgcolor="white", bordercolor="#EF9F27", borderwidth=1, borderpad=3)
    fig.update_layout(
        barmode="stack", hovermode=False, height=height, dragmode=False,
        margin=dict(t=50, b=10, l=30, r=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="left", x=0, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", tickfont=dict(size=10), fixedrange=True),
        bargap=0.4,
    )
    return fig

# ─── SESSION STATE ────────────────────────────────────────────────────────────
PREFIX = "cc_"
def ss(k): return PREFIX + k

for key, default in [
    ("mode", None), ("step", 0), ("ledger", None),
    ("ms_history", None), ("chosen", {}), ("confirmed", set()),
]:
    full = ss(key)
    if full not in st.session_state:
        st.session_state[full] = default

if st.session_state[ss("ledger")] is None:
    st.session_state[ss("ledger")] = init_state()
if st.session_state[ss("ms_history")] is None:
    bm, cm, tot = compute_ms(init_state())
    st.session_state[ss("ms_history")] = [{"label":"Start","bank":bm,"cash":cm,"total":tot}]

def reset():
    for key in ["mode","step","ledger","ms_history","chosen","confirmed"]:
        del st.session_state[ss(key)]
    st.rerun()

# ─── MODE SELECTION SCREEN ────────────────────────────────────────────────────
if st.session_state[ss("mode")] is None:
    if st.button("← Back to Home", use_container_width=False):
        st.switch_page("streamlit_app.py")

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align:center;margin-bottom:2rem;'>
            <div style='font-size:2rem;font-weight:800;color:#1E1B4B;'>🏦 Reserve Transfer</div>
            <div style='font-size:1rem;color:#6b6b6b;margin-top:6px;'>
                From loan creation to same-bank and interbank reserve settlement
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
                Fixed amounts, automatic flow.<br>
                We walk you through every step — you focus on understanding.
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
            <div class="mode-title">Make Your Own Decisions</div>
            <div class="mode-sub">
                You choose the amounts at each step.<br>
                See how your decisions shape the money supply.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Start Simulation →", use_container_width=True):
            st.session_state[ss("mode")] = "simulation"
            st.rerun()
    st.stop()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
mode   = st.session_state[ss("mode")]
step_i = st.session_state[ss("step")]
sc     = SCENARIOS[min(step_i, len(SCENARIOS)-1)]
IS_TRAINING = mode == "training"

# ─── TOP NAV (when in mode) ───────────────────────────────────────────────────
if mode is not None:
    col_nav_home, col_nav_spacer = st.columns([1, 5])
    with col_nav_home:
        if st.button("← Back to Reserve Transfer", use_container_width=True, type="secondary"):
            reset()
            st.switch_page("03_Banks.py")

with st.sidebar:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Mode badge
    mode_label = "📖 Training Mode" if IS_TRAINING else "🎮 Simulation Mode"
    mode_color = "#6366F1" if IS_TRAINING else "#F59E0B"
    st.markdown(
        f'<div style="text-align:center;background:{mode_color};color:white;border-radius:8px;padding:6px;font-size:11px;font-weight:700;margin-bottom:10px;">{mode_label}</div>',
        unsafe_allow_html=True
    )

    display_step = min(step_i + 1, len(SCENARIOS))
    st.markdown(
        f'<div class="sb-metric"><div class="sb-metric-label">Progress</div>'
        f'<div class="sb-metric-val">Step {display_step} / {len(SCENARIOS)}</div>'
        f'{dots_html(min(step_i, len(SCENARIOS)-1), len(SCENARIOS))}</div>',
        unsafe_allow_html=True
    )

    bm, cm, tot = compute_ms(st.session_state[ss("ledger")])
    hist = st.session_state[ss("ms_history")]
    prev_tot = hist[-2]["total"] if len(hist) > 1 else 0
    delta = tot - prev_tot
    delta_html = (f'<div class="sb-metric-delta delta-pos">▲ +${delta} this step</div>' if delta > 0
                  else f'<div class="sb-metric-delta delta-neg">▼ −${abs(delta)} this step</div>' if delta < 0
                  else f'<div class="sb-metric-delta delta-neu">→ No change this step</div>')
    st.markdown(
        f'<div class="sb-metric"><div class="sb-metric-label">Money Supply (M1)</div>'
        f'<div class="sb-metric-val">${tot}</div>{delta_html}'
        f'<div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center;background:#EEF6FF;border-radius:6px;padding:5px 8px;">'
        f'<span style="font-size:10px;color:#3B6D9E;">🏦 Bank Deposits</span>'
        f'<span style="font-size:13px;font-weight:800;color:#185FA5;">${bm}</span></div>'
        f'<div style="margin-top:4px;display:flex;justify-content:space-between;align-items:center;background:#F5F0FF;border-radius:6px;padding:5px 8px;">'
        f'<span style="font-size:10px;color:#7C3AED;">💵 Cash in Circ.</span>'
        f'<span style="font-size:13px;font-weight:800;color:#6D28D9;">${cm}</span></div></div>',
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

# ─── COMPLETE SCREEN ──────────────────────────────────────────────────────────
if step_i >= len(SCENARIOS):
    st.markdown(
        '<div class="complete-card"><div style="font-size:48px;margin-bottom:8px;">🎓</div>'
        '<div style="font-size:22px;font-weight:800;color:#065F46;margin-bottom:6px;">Full Cycle Complete!</div>'
        '<div style="font-size:14px;color:#047857;line-height:1.6;">'
        'You traced loan creation, same-bank deposit transfer, and interbank reserve settlement. All accounted for.'
        '</div></div>',
        unsafe_allow_html=True
    )
    bm, cm, tot = compute_ms(st.session_state[ss("ledger")])
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Final M1", f"${tot}")
    with c2: st.metric("Bank Deposits", f"${bm}")
    with c3: st.metric("Cash in Circ.", f"${cm}")
    st.markdown("### 📊 Money Supply Journey")
    st.plotly_chart(ms_chart(st.session_state[ss("ms_history")], height=300), use_container_width=True)
    if st.button("↺ Play Again", type="primary", use_container_width=True):
        reset()
    st.stop()

# ─── STEP HEADER ──────────────────────────────────────────────────────────────
tag_cls = {"green":"tag-green","red":"tag-red","blue":"tag-blue"}[sc["tag_type"]]
header_cls = "step-header-card" if IS_TRAINING else "step-header-sim"
badge_cls  = "step-badge" if IS_TRAINING else "step-badge-s"
st.markdown(
    f'<div class="{header_cls}">'
    f'<span class="{badge_cls}">{"📖 Training" if IS_TRAINING else "🎮 Simulation"} · Step {sc["id"]} of {len(SCENARIOS)}</span>'
    f'<div class="step-title">{sc["emoji"]} {sc["title"]}</div>'
    f'<div class="step-desc">{sc["short"]}</div>'
    f'<span class="tag {tag_cls}">{sc["tag"]}</span>'
    f'</div>',
    unsafe_allow_html=True
)

col_main, col_chart = st.columns([3, 2])

with col_main:
    already_confirmed = step_i in st.session_state[ss("confirmed")]


    if sc["choice_type"] == "none":
        # Auto-confirm
        st.markdown(f'<div class="insight-bar">💡 {sc["insight"]}</div>', unsafe_allow_html=True)
        st.session_state[ss("confirmed")].add(step_i)

    elif IS_TRAINING:
        # ── TRAINING MODE ──
        amt = sc["training_amt"]
        if not already_confirmed:
            st.markdown(
                f'<div style="margin:10px 0 6px 0;font-size:12px;font-weight:700;color:#4B5563;text-transform:uppercase;letter-spacing:0.5px;">Amount for this step</div>'
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
            if st.button(f"✓ Apply ${amt} and Continue", type="primary", use_container_width=True):
                txs = build_transactions(sc["id"], amt)
                new_ledger = apply_tx(st.session_state[ss("ledger")], txs)
                st.session_state[ss("ledger")] = new_ledger
                bm, cm, tot = compute_ms(new_ledger)
                st.session_state[ss("ms_history")].append({"label":f"Step {sc['id']}","bank":bm,"cash":cm,"total":tot})
                st.session_state[ss("confirmed")].add(step_i)
                st.session_state[ss("chosen")][step_i] = amt
                st.rerun()
        else:
            render_step_balance_sheets(
            st.session_state[ss("ledger")],
            sc["involved"]
    )

            if len(st.session_state[ss("ms_history")]) > 1:
                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    st.plotly_chart(
                    ms_chart(st.session_state[ss("ms_history")]),
                    use_container_width=True
        )

    else:
        # ── SIMULATION MODE ──
        if already_confirmed:
            render_step_balance_sheets(
                st.session_state[ss("ledger")],
                sc["involved"]
            )
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
                        key=f"cc_opt_{step_i}_{opt}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True
                    ):
                        st.session_state[ss("chosen")][step_i] = opt
                        st.rerun()

            chosen_amt = st.session_state[ss("chosen")].get(step_i)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if chosen_amt is not None:
                if st.button(
                    f"✓ Confirm ${chosen_amt} and Apply",
                    key=f"cc_confirm_{step_i}",
                    type="primary",
                    use_container_width=True
                ):
                    txs = build_transactions(sc["id"], chosen_amt)
                    new_ledger = apply_tx(st.session_state[ss("ledger")], txs)

                    st.session_state[ss("ledger")] = new_ledger
                    st.session_state[ss("chosen")][step_i] = chosen_amt
                    st.session_state[ss("confirmed")].add(step_i)

                    bm, cm, tot = compute_ms(new_ledger)
                    st.session_state[ss("ms_history")].append(
                        {"label": f"Step {sc['id']}", "bank": bm, "cash": cm, "total": tot}
                    )
                    st.rerun()
            else:
                st.markdown(
                    '<div style="text-align:center;color:#9CA3AF;font-size:12px;padding:8px 0;">👆 Pick an amount above to continue</div>',
                    unsafe_allow_html=True
                )




# ── Navigation (Rendered Last for Mobile Layout) ────────────────────────────────
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
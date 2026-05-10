from pathlib import Path
import re

src_path = Path(__file__)
src = src_path.read_text(encoding="utf-8")

new_scenarios = r'''SCENARIOS = [
    {
        "id": 1, "emoji": "✨",
        "title": "Bank X Grants a Loan to Customer A",
        "short": "Bank X creates a loan for Customer A and simultaneously creates a deposit.",
        "insight": "Bank X does not lend out pre-existing money. It expands both sides of its balance sheet: <strong>Loan</strong> on assets and <strong>Customer A Deposit</strong> on liabilities. Customer A receives new purchasing power.",
        "tag": "💚 Deposit Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 200,
        "sim_opts": [100, 200, 300, 400],
        "sim_label": "How much does Bank X loan to Customer A?",
        "involved": ["BankX", "CustomerA"],
    },
    {
        "id": 2, "emoji": "💳",
        "title": "Bank Y Grants a Loan to Customer B",
        "short": "Bank Y independently creates credit for Customer B.",
        "insight": "Bank Y creates money in exactly the same way: a <strong>Loan</strong> appears on the asset side and a <strong>Deposit</strong> appears on the liability side. Deposits are created by bank lending.",
        "tag": "💚 Deposit Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 150,
        "sim_opts": [100, 150, 200, 300],
        "sim_label": "How much does Bank Y loan to Customer B?",
        "involved": ["BankY", "CustomerB"],
    },
    {
        "id": 3, "emoji": "🧾",
        "title": "Bank X Grants a Loan to Customer C",
        "short": "A second customer at Bank X receives newly created bank money.",
        "insight": "Bank X can create another deposit for Customer C through the same accounting operation. Now Bank X has deposits for two customers: Customer A and Customer C.",
        "tag": "💚 Deposit Created", "tag_type": "green",
        "choice_type": "loan",
        "training_amt": 100,
        "sim_opts": [50, 100, 150, 200],
        "sim_label": "How much does Bank X loan to Customer C?",
        "involved": ["BankX", "CustomerC"],
    },
    {
        "id": 4, "emoji": "🏛️",
        "title": "Central Bank Provides Reserves to Both Banks",
        "short": "The Central Bank supplies settlement balances to Bank X and Bank Y.",
        "insight": "Reserves are not customer money. They are the <strong>settlement asset between banks</strong>. When customers at different banks pay each other, reserves move across accounts at the Central Bank.",
        "tag": "➡️ No M1 Change", "tag_type": "blue",
        "choice_type": "reserve",
        "training_amt": 300,
        "sim_opts": [200, 300, 400, 500],
        "sim_label": "How much in reserves does the Central Bank provide to each bank?",
        "involved": ["BankX", "BankY", "CentralBank"],
    },
    {
        "id": 5, "emoji": "🔁",
        "title": "Customer A Pays Customer B — Reserves Move from Bank X to Bank Y",
        "short": "A deposit payment crosses banks, so reserves must settle in the background.",
        "insight": "Customer A's deposit at Bank X falls and Customer B's deposit at Bank Y rises. Behind the scenes, <strong>Bank X loses reserves</strong> and <strong>Bank Y gains reserves</strong>. Total customer deposits do not change; ownership changes.",
        "tag": "🔁 Reserve Transfer", "tag_type": "blue",
        "choice_type": "transfer",
        "training_amt": 80,
        "sim_opts": [20, 50, 80, 100],
        "sim_label": "How much does Customer A transfer to Customer B?",
        "involved": ["BankX", "BankY", "CentralBank", "CustomerA", "CustomerB"],
    },
    {
        "id": 6, "emoji": "↩️",
        "title": "Customer B Pays Customer C — Reserves Move Back to Bank X",
        "short": "Now the payment goes in the opposite direction: from Bank Y to Bank X.",
        "insight": "Customer B's deposit at Bank Y falls and Customer C's deposit at Bank X rises. This time <strong>Bank Y loses reserves</strong> and <strong>Bank X gains reserves</strong>. The payment system reallocates reserves across banks.",
        "tag": "🔁 Reserve Transfer", "tag_type": "blue",
        "choice_type": "transfer",
        "training_amt": 60,
        "sim_opts": [20, 40, 60, 80],
        "sim_label": "How much does Customer B transfer to Customer C?",
        "involved": ["BankX", "BankY", "CentralBank", "CustomerB", "CustomerC"],
    },
    {
        "id": 7, "emoji": "🎓",
        "title": "Reserve Transfer Review",
        "short": "You completed the interbank settlement circuit.",
        "insight": "Bank loans create customer deposits. Interbank payments do not create new M1; they move deposits between customers and move reserves between banks. Reserves are the settlement layer behind deposit payments.",
        "tag": "🎓 Complete!", "tag_type": "green",
        "choice_type": "none",
        "training_amt": 0,
        "sim_opts": [],
        "sim_label": "",
        "involved": [],
    },
]'''

src = re.sub(r'SCENARIOS = \[.*?\]\n\n# ─── ENTITIES', new_scenarios + "\n\n# ─── ENTITIES", src, flags=re.S)

new_entities = r'''ENTITY_DEFS = {
    "BankX":       {"label": "Bank X",       "assets": {"Loans":0,"Reserves":0},              "liabilities": {"CustADep":0,"CustCDep":0,"DueCB":0}},
    "BankY":       {"label": "Bank Y",       "assets": {"Loans":0,"Reserves":0},              "liabilities": {"CustBDep":0,"DueCB":0}},
    "CentralBank": {"label": "Central Bank", "assets": {"LoansToBanks":0},                   "liabilities": {"Reserves":0}},
    "CustomerA":   {"label": "Customer A",   "assets": {"Deposits":0},                       "liabilities": {"Loans":0}},
    "CustomerB":   {"label": "Customer B",   "assets": {"Deposits":0},                       "liabilities": {"Loans":0}},
    "CustomerC":   {"label": "Customer C",   "assets": {"Deposits":0},                       "liabilities": {"Loans":0}},
}
ENTITY_ORDER = ["BankX","BankY","CentralBank","CustomerA","CustomerB","CustomerC"]
FRIENDLY = {
    "CustADep":"Cust A Dep","CustBDep":"Cust B Dep","CustCDep":"Cust C Dep",
    "DueCB":"Due to CB","LoansToBanks":"Loans→Banks",
}'''
src = re.sub(r'ENTITY_DEFS = \{.*?FRIENDLY = \{.*?\}', new_entities, src, flags=re.S)

# replace compute_ms to include CustCDep and CustomerC cash if ever added
new_compute = r'''def compute_ms(state):
    bank_deps = (
        state["BankX"]["liabilities"].get("CustADep",0)
        + state["BankX"]["liabilities"].get("CustCDep",0)
        + state["BankY"]["liabilities"].get("CustBDep",0)
    )
    cash = (
        state["CustomerA"]["assets"].get("Cash",0)
        + state["CustomerB"]["assets"].get("Cash",0)
        + state["CustomerC"]["assets"].get("Cash",0)
    )
    return bank_deps, cash, bank_deps + cash'''
src = re.sub(r'def compute_ms\(state\):.*?return bank_deps, cash, bank_deps \+ cash', new_compute, src, flags=re.S)

new_tx = r'''def build_transactions(sc_id, amt):
    if sc_id == 1:
        return [
            ("BankX","debit","Loans",amt), ("BankX","credit","CustADep",amt),
            ("CustomerA","debit","Deposits",amt), ("CustomerA","credit","Loans",amt),
        ]
    elif sc_id == 2:
        return [
            ("BankY","debit","Loans",amt), ("BankY","credit","CustBDep",amt),
            ("CustomerB","debit","Deposits",amt), ("CustomerB","credit","Loans",amt),
        ]
    elif sc_id == 3:
        return [
            ("BankX","debit","Loans",amt), ("BankX","credit","CustCDep",amt),
            ("CustomerC","debit","Deposits",amt), ("CustomerC","credit","Loans",amt),
        ]
    elif sc_id == 4:
        return [
            ("BankX","debit","Reserves",amt), ("BankX","credit","DueCB",amt),
            ("BankY","debit","Reserves",amt), ("BankY","credit","DueCB",amt),
            ("CentralBank","debit","LoansToBanks",amt*2), ("CentralBank","credit","Reserves",amt*2),
        ]
    elif sc_id == 5:
        return [
            # Customer A pays Customer B.
            # Bank X deposit liability falls; Bank X reserve asset falls.
            ("BankX","debit","CustADep",amt), ("BankX","credit","Reserves",amt),

            # Bank Y receives reserves and credits Customer B's deposit.
            ("BankY","debit","Reserves",amt), ("BankY","credit","CustBDep",amt),

            # Customer balance sheets: A loses deposit, B gains deposit.
            ("CustomerA","credit","Deposits",amt),
            ("CustomerB","debit","Deposits",amt),
        ]
    elif sc_id == 6:
        return [
            # Customer B pays Customer C.
            # Bank Y deposit liability falls; Bank Y reserve asset falls.
            ("BankY","debit","CustBDep",amt), ("BankY","credit","Reserves",amt),

            # Bank X receives reserves and credits Customer C's deposit.
            ("BankX","debit","Reserves",amt), ("BankX","credit","CustCDep",amt),

            # Customer balance sheets: B loses deposit, C gains deposit.
            ("CustomerB","credit","Deposits",amt),
            ("CustomerC","debit","Deposits",amt),
        ]
    return []'''
src = re.sub(r'def build_transactions\(sc_id, amt\):.*?return \[\]\n\n# ─── FLOW BUILDER', new_tx + "\n\n# ─── FLOW BUILDER", src, flags=re.S)

# replace flow node definitions and build_flow
new_flow_defs = r'''BX  = {"id":"BankX",      "label":"Bank X",      "abbr":"BX", "bg":"#E6F1FB","border":"#378ADD","color":"#185FA5"}
BY  = {"id":"BankY",      "label":"Bank Y",      "abbr":"BY", "bg":"#EAF3DE","border":"#1D9E75","color":"#3B6D11"}
CB  = {"id":"CentralBank","label":"Central Bank","abbr":"Fed", "bg":"#E1F5EE","border":"#1D9E75","color":"#0F6E56"}
CA  = {"id":"CustomerA",  "label":"Customer A",  "abbr":"CA", "bg":"#FAEEDA","border":"#EF9F27","color":"#854F0B"}
CBb = {"id":"CustomerB",  "label":"Customer B",  "abbr":"CB", "bg":"#FBEAF0","border":"#D4537E","color":"#72243E"}
CC  = {"id":"CustomerC",  "label":"Customer C",  "abbr":"CC", "bg":"#F3E8FF","border":"#9333EA","color":"#581C87"}

def arr(amt, note): return {"arrow":True,"amt":amt,"note":note}

def build_flow(sc_id, amt):
    a = f"${amt}"
    if sc_id == 1:
        return [BX, arr(f"{a} loan","deposit created"), CA]
    elif sc_id == 2:
        return [BY, arr(f"{a} loan","deposit created"), CBb]
    elif sc_id == 3:
        return [BX, arr(f"{a} loan","deposit created"), CC]
    elif sc_id == 4:
        return [CB, arr(f"{a} each","reserves"), BX, BY]
    elif sc_id == 5:
        return [CA, arr(f"{a} payment","deposit ↓"), BX, arr(f"{a} reserves","Fed transfer"), CB, arr(f"{a} reserves","settlement"), BY, arr(f"{a} deposit","deposit ↑"), CBb]
    elif sc_id == 6:
        return [CBb, arr(f"{a} payment","deposit ↓"), BY, arr(f"{a} reserves","Fed transfer"), CB, arr(f"{a} reserves","settlement"), BX, arr(f"{a} deposit","deposit ↑"), CC]
    return []'''
src = re.sub(r'BX  = .*?def build_flow\(sc_id, amt\):.*?return \[\]\n\n# ─── RENDER HELPERS', new_flow_defs + "\n\n# ─── RENDER HELPERS", src, flags=re.S)

# Update page title/header
src = src.replace('page_title="Credit Creation · MoneySimulator"', 'page_title="Reserve Transfer · MoneySimulator"')
src = src.replace('"<div style=\'font-size:2rem;font-weight:800;color:#1E1B4B;\'>🏦 Credit Creation</div>"', '"<div style=\'font-size:2rem;font-weight:800;color:#1E1B4B;\'>🔁 Reserve Transfer</div>"')
src = src.replace('From loan to cash withdrawal — the full monetary circuit', 'Interbank payments move reserves across Fed/Central Bank accounts')
src = src.replace('← Back to Credit Creation', '← Back to Reserve Transfer')

out_path = Path(__file__)
out_path.write_text(src, encoding="utf-8")
out_path

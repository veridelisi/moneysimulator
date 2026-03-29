
import os

folders = [
    "pages",
    "assets/icons",
    "assets/images",
    "data",
    "components",
    "utils",
]

files = {
    "pages/01_fed.py": "# FED Scenarios\n",
    "pages/02_treasury.py": "# Treasury Scenarios\n",
    "pages/03_banks.py": "# Banks Scenarios\n",
    "pages/04_karma.py": "# Karma Scenarios\n",
    "data/scenarios.json": "{}\n",
    "components/t_account.py": "# T-Account component\n",
    "components/flow_chart.py": "# Flow chart component\n",
    "components/balance_sheet.py": "# Balance sheet component\n",
    "utils/helpers.py": "# Helper functions\n",
    "requirements.txt": "streamlit\nplotly\npandas\n",
    "README.md": "# MoneySimulator\n",
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"📁 {folder}")

for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)
    print(f"📄 {filepath}")

print("\n✅ Yapı hazır!")

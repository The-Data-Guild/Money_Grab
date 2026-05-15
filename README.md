# Money Grab

Simple GUI tool to record expenses and generate a PDF split report.

**Features**
- Add named expenses with costs
- Calculate total and per-person split
- Export a formatted PDF report

**Setup**
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # macOS / Linux
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

**Run**

```bash
python main.py
```

The GUI will open. Enter an expense name and cost, click "Add Expense", set a number in "Split By", then click "Calculate and Generate PDF".

**Notes & Improvements implemented**
- Refactored the GUI into a `MoneyGrabApp` class for clearer structure and easier testing.
- Fixed Enter-key behavior and removed broken wait-variable logic.
- Improved PDF pagination and timestamped filenames.
- Added `requirements.txt` and improved `main.py` launcher.

**Ideas for project evolution**
- Persist expenses to a local JSON or SQLite database and add load/save.
- Add CSV import/export and itemized receipts parsing.
- Support per-person assignment (who paid / owes what) and generate individual statements.
- Add a web frontend (Flask/FastAPI) to make it accessible from mobile devices.
- Add unit tests and a CI workflow (GitHub Actions) for automated checks.

Contributions welcome — open an issue or PR with suggested improvements.

# Mutual Fund Portfolio Data Automation & Consolidation

## Overview

This project automates the process of collecting and consolidating mutual fund portfolio data from Axis Mutual Fund's statutory disclosures website.

The objective was to download the **Monthly Scheme Portfolio (December 2025 – Consolidated)** file, clean the data, and convert it into a structured CSV format that can be reused for analysis. The solution includes both website automation and data parsing using Python.

---

## Data Source

**Website:** https://www.axismf.com/statutory-disclosures

**Section:** Monthly Scheme Portfolios

**Selection used:**
- Year: 2025
- Month: December
- Scheme: Consolidated

The downloaded Excel file contains:
- An **Index** sheet with scheme mappings
- Multiple **scheme-level portfolio sheets**, one per mutual fund scheme

---

## Data Model & Assumptions

### Data Model

The final output is a single CSV file where:

- Each row represents **one instrument holding within one mutual fund scheme**
- AMC and scheme information is repeated per row to keep the dataset flat and easy to analyze

**Fields included in the final CSV:**
- `amc_name`
- `scheme_code`
- `scheme_name`
- `instrument_name`
- `instrument_type` (Equity / Debt / Other)
- `isin`
- `quantity`
- `market_value_lakhs`
- `portfolio_percent`
- `reporting_date`

The schema is intentionally generic so it can be reused for other AMCs with minimal changes.

---

### Cleaning Logic & Assumptions

- Scheme codes and names are mapped dynamically using the **Index** sheet
- Header rows in scheme sheets are not consistent, so the script detects the correct header by searching for keywords such as `ISIN` and `Market`
- Rows are removed if:
  - Instrument name is missing
  - ISIN is missing
  - Market value is non-numeric
- Summary rows, totals, notes, receivables, and other non-investment entries are filtered out using text-based rules
- Instrument type is inferred from the scheme name using common keywords (equity, debt, liquid, etc.)
- Duplicate instrument records within the same scheme are removed as a safety check

---

## Automation Approach

Website automation is implemented using **Playwright (Python)** to handle Axis Mutual Fund's modern Ionic-based UI.

The automation script:
1. Navigates to the statutory disclosures page
2. Expands the "Monthly Scheme Portfolios" section
3. Selects:
   - Year: 2025
   - Month: December
   - Scheme: Consolidated
4. Handles Ionic dropdown popovers using keyboard interactions
5. Downloads all available Excel and PDF files

Playwright's native download handling is used to ensure files are captured reliably. The automation and data parsing steps are kept separate to make the workflow easier to debug and extend.

---

## Project Structure

```
├── automation.py                          # Playwright automation script
├── portfolio_parser.py                    # Excel parsing and CSV generation
├── downloads                              # Raw Excel/PDF files downloaded from Axis MF
├── axis_mf_portfolio_2025_12_clean.csv    # Final consolidated output
└── README.md                              # Project documentation
```

---

## How to Run (Using VS Code)

The project was developed and run using **VS Code**. All commands are executed from the VS Code integrated terminal.

### Prerequisites

- Python 3.9 or higher installed on the system
- VS Code with Python extension installed

### Step 1: Install Required Libraries

Open the project folder in VS Code and open the terminal (`View → Terminal` or `Ctrl + \``).

Install dependencies globally:

```bash
pip install pandas openpyxl playwright
playwright install
```

### Step 2: Run Website Automation (Download Files)

Run the Playwright automation script:

```bash
python automation.py
```

This will:
- Open a Chromium browser window
- Navigate to the Axis Mutual Fund statutory disclosures page
- Select December 2025 (Consolidated)
- Download the required Excel/PDF files

All downloaded files are saved inside the `downloads/` folder.

### Step 3: Generate the Clean CSV File

After the Excel file is downloaded, ensure the file path is correctly set in `portfolio_parser.py`, then run:

```bash
python portfolio_parser.py
```

This generates the consolidated output file: `axis_mf_portfolio_2025_12_clean.csv`

---

## Notes

- No virtual environment was used for this project
- All scripts were executed directly from the VS Code terminal
- The automation and parsing steps are intentionally separated for clarity and easier debugging

## Author

**Kshitish Kumar**   
This project was completed as part of the task for **Qonfido**

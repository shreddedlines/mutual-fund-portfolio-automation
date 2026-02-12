import pandas as pd

FILE_PATH = "Monthly Portfolio-31 12 25.xlsx"
REPORTING_DATE = "2025-12-31"
AMC_NAME = "Axis Mutual Fund"


def get_scheme_mapping(file_path):
    index_df = pd.read_excel(file_path, sheet_name="Index")
    return dict(zip(index_df["Short Name"], index_df["Scheme Name"]))


def classify_scheme_type(scheme_name):
    name = scheme_name.lower()

    if any(x in name for x in ["equity", "index", "nifty", "midcap", "smallcap"]):
        return "Equity"
    elif any(x in name for x in ["debt", "bond", "fixed term", "liquid", "gilt"]):
        return "Debt"
    else:
        return "Other"


def extract_scheme_data(file_path, sheet_name, scheme_name):
    raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # --- Find header row ---
    header_row = None
    for i in range(10):
        row = raw_df.iloc[i].astype(str).str.lower()
        if "isin" in row.values and "market" in " ".join(row.values):
            header_row = i
            break

    if header_row is None:
        return pd.DataFrame()

    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)

    # --- Rename required columns ---
    df = df.rename(columns={
        df.columns[1]: "instrument_name",
        df.columns[2]: "isin",
        df.columns[4]: "quantity",
        df.columns[5]: "market_value_lakhs",
        df.columns[6]: "portfolio_percent",
    })

    # --- CORE DATA CLEANING (IMPORTANT PART) ---

    # 1. Instrument name must exist
    df = df[df["instrument_name"].notna()]

    # 2. ISIN must exist (removes headers, cash, notes)
    df = df[df["isin"].notna()]

    # 3. Market value must be numeric
    df["market_value_lakhs"] = pd.to_numeric(
        df["market_value_lakhs"], errors="coerce"
    )
    df = df[df["market_value_lakhs"].notna()]

    # 4. Remove known non-investment text rows (extra safety)
    bad_patterns = (
        "total|sub total|listed|unlisted|instrument|note|ytm|repo|"
        "receivable|payable|clearing"
    )

    df = df[~df["instrument_name"].str.contains(
        bad_patterns, case=False, na=False
    )]

    # --- Add metadata columns ---
    df["amc_name"] = AMC_NAME
    df["scheme_code"] = sheet_name
    df["scheme_name"] = scheme_name
    df["instrument_type"] = classify_scheme_type(scheme_name)
    df["reporting_date"] = REPORTING_DATE

    # --- Remove duplicates (safety) ---
    df = df.drop_duplicates(
        subset=["scheme_code", "instrument_name", "isin"]
    )

    return df[
        [
            "amc_name",
            "scheme_code",
            "scheme_name",
            "instrument_name",
            "instrument_type",
            "isin",
            "quantity",
            "market_value_lakhs",
            "portfolio_percent",
            "reporting_date",
        ]
    ]


def main():
    scheme_map = get_scheme_mapping(FILE_PATH)
    all_data = []

    for sheet, scheme_name in scheme_map.items():
        try:
            scheme_df = extract_scheme_data(FILE_PATH, sheet, scheme_name)
            if not scheme_df.empty:
                all_data.append(scheme_df)
        except Exception as e:
            print(f"Skipped {sheet}: {e}")

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("axis_mf_portfolio_2025_12_clean.csv", index=False)

    print(" Clean CSV generated successfully !!!!!!!")


if __name__ == "__main__":
    main()

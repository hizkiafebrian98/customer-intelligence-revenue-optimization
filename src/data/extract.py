
from pathlib import Path

import pandas as pd


# Project directory: repository root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Default raw dataset location
DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" / "online_retail_II.xlsx"
)

# Original source columns
SOURCE_COLUMNS = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
]

# Original workbook sheets
SHEET_NAMES = [
    "Year 2009-2010",
    "Year 2010-2011",
]


def extract_online_retail(file_path=None):
    """
    Extract and combine both sheets of the UCI Online Retail II dataset.

    Parameters
    ----------
    file_path : str or Path, optional
        Path to the original Excel workbook.
        Defaults to data/raw/online_retail_II.xlsx.

    Returns
    -------
    pandas.DataFrame
        Combined raw transaction records with the original eight columns.
    """

    if file_path is None:
        file_path = DEFAULT_DATA_PATH

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    extracted_sheets = []

    for sheet_name in SHEET_NAMES:
        df_sheet = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            engine="openpyxl",
        )

        missing_columns = [
            column
            for column in SOURCE_COLUMNS
            if column not in df_sheet.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing expected columns in {sheet_name}: "
                f"{missing_columns}"
            )

        df_sheet = df_sheet[SOURCE_COLUMNS].copy()

        extracted_sheets.append(df_sheet)

    df_extracted = pd.concat(
        extracted_sheets,
        ignore_index=True,
    )

    return df_extracted


if __name__ == "__main__":
    df = extract_online_retail()

    print("Extraction completed.")
    print("Dataset dimensions:", df.shape)
    print("Columns:", df.columns.tolist())

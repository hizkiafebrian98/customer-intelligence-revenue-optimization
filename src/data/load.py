
from pathlib import Path

import pandas as pd
from sqlalchemy import text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REFERENCE_DIR = PROJECT_ROOT / "data" / "reference"

BATCH_SIZE = 10_000

EXPECTED_COUNTS = {
    "retail_transactions": 1_033_036,
    "duplicate_transaction_audit": 34_335,
    "transaction_taxonomy": 16,
    "description_mapping": 1_387,
}


def normalize_columns(df):
    """Convert source column names to lowercase snake_case."""

    column_mapping = {
        "Invoice": "invoice",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "Price": "price",
        "Customer ID": "customer_id",
        "Country": "country",
        "YearMonth": "year_month",
        "StockCode_normalized": "stock_code_normalized",
    }

    renamed_columns = {
        column: column_mapping.get(
            column,
            column.lower().replace(" ", "_")
        )
        for column in df.columns
    }

    return df.rename(columns=renamed_columns)


def prepare_transaction_data(df):
    """Prepare transaction data for PostgreSQL insertion."""

    df = normalize_columns(df.copy())

    # Convert invoice timestamps to datetime.
    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="raise"
    )

    # Convert monthly periods to Python date values.
    df["year_month"] = (
        pd.PeriodIndex(
            df["year_month"].astype(str),
            freq="M"
        )
        .to_timestamp()
        .date
    )

    # Convert nullable customer identifiers to integers.
    df["customer_id"] = (
        pd.to_numeric(df["customer_id"], errors="raise")
        .astype("Int64")
        .astype(object)
    )

    df["customer_id"] = df["customer_id"].where(
        pd.notna(df["customer_id"]),
        None
    )

    return df


def load_online_retail(engine, replace_existing=False):
    """
    Load all four datasets into PostgreSQL.

    If replace_existing is True, existing table contents
    are deleted and replaced within one transaction.
    """

    # --------------------------------------------------------
    # 1. Read source datasets
    # --------------------------------------------------------

    print("Reading source datasets...")

    df_transactions = pd.read_parquet(
        PROCESSED_DIR / "online_retail_clean.parquet"
    )

    df_duplicates = pd.read_csv(
        PROCESSED_DIR / "duplicate_audit.csv"
    )

    df_taxonomy = pd.read_csv(
        REFERENCE_DIR / "transaction_taxonomy.csv"
    )

    df_descriptions = pd.read_csv(
        REFERENCE_DIR / "description_mapping.csv"
    )

    # --------------------------------------------------------
    # 2. Prepare column names and data types
    # --------------------------------------------------------

    df_transactions = prepare_transaction_data(
        df_transactions
    )

    df_duplicates = prepare_transaction_data(
        df_duplicates
    )

    df_taxonomy = normalize_columns(df_taxonomy)
    df_descriptions = normalize_columns(df_descriptions)

    datasets = {
        "retail_transactions": df_transactions,
        "duplicate_transaction_audit": df_duplicates,
        "transaction_taxonomy": df_taxonomy,
        "description_mapping": df_descriptions,
    }

    # --------------------------------------------------------
    # 3. Verify expected source record counts
    # --------------------------------------------------------

    for table_name, df in datasets.items():
        expected = EXPECTED_COUNTS[table_name]

        if len(df) != expected:
            raise ValueError(
                f"{table_name}: expected {expected} records, "
                f"received {len(df)}."
            )

    print("Source record counts verified.")

    # --------------------------------------------------------
    # 4. Verify destination table columns
    # --------------------------------------------------------

    from sqlalchemy import inspect

    inspector = inspect(engine)

    for table_name, df in datasets.items():
        database_columns = [
            column["name"]
            for column in inspector.get_columns(
                table_name,
                schema="public"
            )
        ]

        if set(df.columns) != set(database_columns):
            raise ValueError(
                f"Column mismatch detected in {table_name}."
            )

        # Match PostgreSQL column order.
        datasets[table_name] = df[database_columns]

    # --------------------------------------------------------
    # 5. Execute loading in one database transaction
    # --------------------------------------------------------

    with engine.begin() as connection:

        existing_counts = {}

        for table_name in EXPECTED_COUNTS:
            existing_counts[table_name] = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM public.{table_name}"
                )
            ).scalar_one()

        has_existing_data = any(
            count > 0 for count in existing_counts.values()
        )

        if has_existing_data and not replace_existing:
            raise RuntimeError(
                "Existing records detected. "
                "Set replace_existing=True only when "
                "you intentionally want to reload all tables."
            )

        if replace_existing:
            print("Removing existing table contents...")

            for table_name in [
                "retail_transactions",
                "duplicate_transaction_audit",
                "transaction_taxonomy",
                "description_mapping",
            ]:
                connection.execute(
                    text(f"DELETE FROM public.{table_name}")
                )

        # Reference tables must be loaded before transactions
        # because transaction tables reference the taxonomy.
        load_order = [
            "transaction_taxonomy",
            "description_mapping",
            "retail_transactions",
            "duplicate_transaction_audit",
        ]

        for table_name in load_order:
            df = datasets[table_name]

            print(
                f"Loading {table_name}: "
                f"{len(df):,} records..."
            )

            df.to_sql(
                name=table_name,
                con=connection,
                schema="public",
                if_exists="append",
                index=False,
                chunksize=BATCH_SIZE,
                method=None,
            )

        # ----------------------------------------------------
        # 6. Verify database record counts
        # ----------------------------------------------------

        print("\nVerifying loaded record counts...")

        loaded_counts = {}

        for table_name, expected in EXPECTED_COUNTS.items():
            actual = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM public.{table_name}"
                )
            ).scalar_one()

            loaded_counts[table_name] = actual

            if actual != expected:
                raise ValueError(
                    f"{table_name}: expected {expected}, "
                    f"found {actual}."
                )

            print(
                f"{table_name}: {actual:,} / {expected:,}"
            )

    print("\nAll datasets loaded and verified successfully.")

    return loaded_counts

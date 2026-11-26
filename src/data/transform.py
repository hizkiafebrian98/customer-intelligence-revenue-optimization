
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REFERENCE_DIR = PROJECT_ROOT / "data" / "reference"

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

DELIVERY_STOCKCODES = ["POST", "C2", "23444", "DOT"]


def transform_online_retail(
    raw_df,
    reference_dir=None,
):
    """
    Transform the extracted Online Retail II data.

    Returns:
        df_classified: Full dataset with transaction classifications.
        df_clean: Primary analytical dataset without excess exact duplicates.
        df_duplicate_audit: Excluded excess exact duplicate records.
    """

    if reference_dir is None:
        reference_dir = DEFAULT_REFERENCE_DIR

    reference_dir = Path(reference_dir)

    description_mapping_path = (
        reference_dir / "description_mapping.csv"
    )
    taxonomy_path = (
        reference_dir / "transaction_taxonomy.csv"
    )

    if not description_mapping_path.exists():
        raise FileNotFoundError(
            f"Description mapping not found: {description_mapping_path}"
        )

    if not taxonomy_path.exists():
        raise FileNotFoundError(
            f"Transaction taxonomy not found: {taxonomy_path}"
        )

    # ---------------------------------------------------------
    # 1. Validate and copy source data
    # ---------------------------------------------------------

    missing_columns = [
        column
        for column in SOURCE_COLUMNS
        if column not in raw_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required source columns: {missing_columns}"
        )

    df = raw_df[SOURCE_COLUMNS].copy(deep=True)
    df = df.reset_index(drop=True)

    # ---------------------------------------------------------
    # 2. Load reference data
    # ---------------------------------------------------------

    description_mapping = pd.read_csv(
        description_mapping_path,
        dtype={"StockCode": "string"},
    )

    transaction_taxonomy = pd.read_csv(
        taxonomy_path,
    )

    if description_mapping["StockCode"].duplicated().any():
        raise ValueError(
            "Description mapping contains duplicate StockCodes."
        )

    if transaction_taxonomy["transaction_category"].duplicated().any():
        raise ValueError(
            "Transaction taxonomy contains duplicate categories."
        )

    description_lookup = (
        description_mapping
        .set_index("StockCode")["imputed_description"]
    )

    # ---------------------------------------------------------
    # 3. Derive temporal feature
    # ---------------------------------------------------------

    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

    # ---------------------------------------------------------
    # 4. Impute descriptions using approved mapping
    # ---------------------------------------------------------

    df["Description_was_missing"] = (
        df["Description"].isna()
    )

    mapped_descriptions = (
        df["StockCode"]
        .astype("string")
        .map(description_lookup)
    )

    imputation_mask = (
        df["Description"].isna()
        & mapped_descriptions.notna()
    )

    df.loc[
        imputation_mask,
        "Description"
    ] = mapped_descriptions.loc[imputation_mask]

    # ---------------------------------------------------------
    # 5. Normalize descriptions and StockCodes
    # ---------------------------------------------------------

    df["Description_normalized"] = (
        df["Description"]
        .astype("string")
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    df["StockCode_normalized"] = (
        df["StockCode"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # ---------------------------------------------------------
    # 6. Derive transaction characteristics
    # ---------------------------------------------------------

    df["is_cancellation"] = (
        df["Invoice"]
        .astype(str)
        .str.startswith("C")
    )

    df["has_customer_id"] = (
        df["Customer ID"].notna()
    )

    df["has_positive_quantity"] = (
        df["Quantity"] > 0
    )

    df["has_positive_price"] = (
        df["Price"] > 0
    )

    df["has_positive_line_value"] = (
        df["Quantity"] * df["Price"] > 0
    )

    df["candidate_paid_purchase"] = (
        ~df["is_cancellation"]
        & df["has_customer_id"]
        & df["has_positive_quantity"]
        & df["has_positive_price"]
    )

    df["line_value"] = (
        df["Quantity"] * df["Price"]
    )

    # ---------------------------------------------------------
    # 7. Classify zero-price activity
    # ---------------------------------------------------------

    df["is_zero_price"] = (
        df["Price"] == 0
    )

    df["zero_price_category"] = "not_zero_price"

    zero_price_mask = df["is_zero_price"]

    df.loc[
        zero_price_mask
        & (df["Quantity"] > 0)
        & df["Customer ID"].notna(),
        "zero_price_category",
    ] = "positive_zero_price_identified_customer"

    df.loc[
        zero_price_mask
        & (df["Quantity"] > 0)
        & df["Customer ID"].isna(),
        "zero_price_category",
    ] = "positive_zero_price_anonymous"

    df.loc[
        zero_price_mask
        & (df["Quantity"] < 0),
        "zero_price_category",
    ] = "negative_zero_price"

    df.loc[
        zero_price_mask
        & (df["Quantity"] == 0),
        "zero_price_category",
    ] = "zero_quantity_zero_price"

    # ---------------------------------------------------------
    # 8. Initial transaction classification
    # ---------------------------------------------------------

    df["transaction_category"] = "unclassified"

    stockcode = df["StockCode_normalized"]

    # Delivery-related transactions
    df.loc[
        stockcode.isin(DELIVERY_STOCKCODES),
        "transaction_category",
    ] = "delivery_charge"

    # Manual transactions
    df.loc[
        stockcode.eq("M"),
        "transaction_category",
    ] = "manual_transaction"

    # Discount-related transactions
    df.loc[
        stockcode.eq("D"),
        "transaction_category",
    ] = "discount_related_transaction"

    # Financial adjustments
    df.loc[
        stockcode.isin(["ADJUST", "ADJUST2"]),
        "transaction_category",
    ] = "financial_adjustment"

    # Bank charges
    df.loc[
        stockcode.eq("BANK CHARGES"),
        "transaction_category",
    ] = "bank_charge"

    # Bad-debt adjustments
    df.loc[
        stockcode.eq("B"),
        "transaction_category",
    ] = "bad_debt_adjustment"

    # Operational adjustment candidates
    operational_adjustment_mask = (
        ~df["is_cancellation"]
        & (df["Quantity"] < 0)
        & (df["Price"] == 0)
        & df["Customer ID"].isna()
    )

    df.loc[
        operational_adjustment_mask
        & df["transaction_category"].eq("unclassified"),
        "transaction_category",
    ] = "operational_adjustment_candidate"

    # Positive-quantity zero-price activity
    positive_zero_price_mask = (
        (df["Quantity"] > 0)
        & (df["Price"] == 0)
    )

    df.loc[
        positive_zero_price_mask
        & df["transaction_category"].eq("unclassified"),
        "transaction_category",
    ] = "zero_price_activity"

    # Identified-customer paid merchandise candidates
    df.loc[
        df["candidate_paid_purchase"]
        & df["transaction_category"].eq("unclassified"),
        "transaction_category",
    ] = "merchandise_candidate"

    # ---------------------------------------------------------
    # 9. Apply investigated special StockCode overrides
    # ---------------------------------------------------------

    special_overrides = {
        "23574": "packing_charge",
        "AMAZONFEE": "platform_fee_candidate",
        "S": "sample_transaction",
        "TEST001": "test_transaction_candidate",
    }

    for code, category in special_overrides.items():
        df.loc[
            stockcode.eq(code),
            "transaction_category",
        ] = category

    # ---------------------------------------------------------
    # 10. Classify remaining anonymous and cancellation records
    # ---------------------------------------------------------

    unclassified_mask = (
        df["transaction_category"].eq("unclassified")
    )

    group_a_mask = (
        ~df["is_cancellation"]
        & df["Customer ID"].isna()
        & (df["Quantity"] > 0)
        & (df["Price"] > 0)
        & unclassified_mask
    )

    group_b_mask = (
        df["is_cancellation"]
        & df["Customer ID"].notna()
        & (df["Quantity"] < 0)
        & (df["Price"] > 0)
        & unclassified_mask
    )

    group_c_mask = (
        df["is_cancellation"]
        & df["Customer ID"].isna()
        & (df["Quantity"] < 0)
        & (df["Price"] > 0)
        & unclassified_mask
    )

    df.loc[
        group_a_mask,
        "transaction_category",
    ] = "anonymous_merchandise_candidate"

    df.loc[
        group_b_mask,
        "transaction_category",
    ] = "merchandise_cancellation_candidate"

    df.loc[
        group_c_mask,
        "transaction_category",
    ] = "anonymous_merchandise_cancellation_candidate"

    # Stop if any records remain unclassified.
    remaining_unclassified = (
        df["transaction_category"].eq("unclassified").sum()
    )

    if remaining_unclassified > 0:
        raise ValueError(
            f"{remaining_unclassified} records remain unclassified."
        )

    # ---------------------------------------------------------
    # 11. Merge transaction taxonomy
    # ---------------------------------------------------------

    df = df.merge(
        transaction_taxonomy,
        on="transaction_category",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    if df["merchandise_revenue_treatment"].isna().any():
        raise ValueError(
            "Some transaction categories have no taxonomy definition."
        )

    # ---------------------------------------------------------
    # 12. Derive analytical eligibility flags
    # ---------------------------------------------------------

    df["is_merchandise_revenue_record"] = (
        df["merchandise_revenue_treatment"].isin(
            ["include_positive", "include_negative"]
        )
    )

    df["is_customer_analytics_eligible"] = (
        df["customer_level_eligible"]
        & df["Customer ID"].notna()
    )

    df["is_qualifying_purchase"] = (
        df["qualifying_purchase"]
        & df["Customer ID"].notna()
        & (df["Quantity"] > 0)
        & (df["Price"] > 0)
    )

    df["merchandise_revenue"] = (
        df["line_value"].where(
            df["is_merchandise_revenue_record"],
            0,
        )
    )

    df["qualifying_purchase_revenue"] = (
        df["line_value"].where(
            df["is_qualifying_purchase"],
            0,
        )
    )

    # ---------------------------------------------------------
    # 13. Identify excess exact duplicate records
    # ---------------------------------------------------------

    duplicate_mask = df.duplicated(
        subset=SOURCE_COLUMNS,
        keep="first",
    )

    df["is_excess_exact_duplicate"] = duplicate_mask

    # ---------------------------------------------------------
    # 14. Create primary and duplicate-audit datasets
    # ---------------------------------------------------------

    classified_columns = SOURCE_COLUMNS + [
        "YearMonth",
        "Description_was_missing",
        "is_cancellation",
        "has_customer_id",
        "has_positive_quantity",
        "has_positive_price",
        "has_positive_line_value",
        "candidate_paid_purchase",
        "Description_normalized",
        "is_zero_price",
        "zero_price_category",
        "StockCode_normalized",
        "transaction_category",
        "line_value",
        "merchandise_revenue_treatment",
        "customer_level_eligible",
        "qualifying_purchase",
        "notes",
        "is_merchandise_revenue_record",
        "is_customer_analytics_eligible",
        "is_qualifying_purchase",
        "merchandise_revenue",
        "qualifying_purchase_revenue",
        "is_excess_exact_duplicate",
    ]

    df = df[classified_columns]

    df_duplicate_audit = df.loc[
        duplicate_mask
    ].copy()

    df_clean = df.loc[
        ~duplicate_mask
    ].copy()

    # Preserve original row positions before resetting indexes.
    df_duplicate_audit["original_row_position"] = (
        df_duplicate_audit.index
    )

    df_clean["original_row_position"] = (
        df_clean.index
    )

    # Reset indexes.
    df_clean = df_clean.reset_index(drop=True)
    df_duplicate_audit = df_duplicate_audit.reset_index(drop=True)

    return df, df_clean, df_duplicate_audit
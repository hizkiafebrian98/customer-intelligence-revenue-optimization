
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

CLASSIFIED_COLUMNS = [
    *SOURCE_COLUMNS,
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

CLEANED_COLUMNS = CLASSIFIED_COLUMNS + [
    "original_row_position"
]


def validate_online_retail(
    raw_df,
    df_classified,
    df_clean,
    df_duplicate_audit,
    reference_dir=None,
):
    """
    Validate the extracted and transformed Online Retail II datasets.

    Returns:
        pd.DataFrame: Validation results with check names and statuses.

    This function does not modify the supplied DataFrames.
    """

    if reference_dir is None:
        reference_dir = DEFAULT_REFERENCE_DIR

    reference_dir = Path(reference_dir)

    results = []

    def add_check(name, passed, details=""):
        results.append({
            "check": name,
            "passed": bool(passed),
            "details": str(details),
        })

    # ---------------------------------------------------------
    # 1. Required source columns
    # ---------------------------------------------------------

    source_columns_exist = all(
        column in raw_df.columns
        for column in SOURCE_COLUMNS
    )

    add_check(
        "Required source columns",
        source_columns_exist,
        "All eight original dataset columns must be present.",
    )

    if not source_columns_exist:
        return pd.DataFrame(results)

    # ---------------------------------------------------------
    # 2. Expected output schemas
    # ---------------------------------------------------------

    add_check(
        "Classified schema",
        df_classified.columns.tolist() == CLASSIFIED_COLUMNS,
        f"Expected {len(CLASSIFIED_COLUMNS)} columns; "
        f"found {len(df_classified.columns)}.",
    )

    add_check(
        "Cleaned schema",
        df_clean.columns.tolist() == CLEANED_COLUMNS,
        f"Expected {len(CLEANED_COLUMNS)} columns; "
        f"found {len(df_clean.columns)}.",
    )

    add_check(
        "Duplicate audit schema",
        df_duplicate_audit.columns.tolist() == CLEANED_COLUMNS,
        f"Expected {len(CLEANED_COLUMNS)} columns; "
        f"found {len(df_duplicate_audit.columns)}.",
    )

    # ---------------------------------------------------------
    # 3. Record-count reconciliation
    # ---------------------------------------------------------

    total_records = len(raw_df)
    classified_records = len(df_classified)
    cleaned_records = len(df_clean)
    duplicate_records = len(df_duplicate_audit)

    add_check(
        "Classified record count",
        classified_records == total_records,
        f"Source: {total_records}; classified: {classified_records}.",
    )

    add_check(
        "Cleaned and audit reconciliation",
        cleaned_records + duplicate_records == total_records,
        f"Cleaned: {cleaned_records}; "
        f"audit: {duplicate_records}; "
        f"source: {total_records}.",
    )

    # ---------------------------------------------------------
    # 4. Duplicate identification
    # ---------------------------------------------------------

    expected_duplicate_mask = raw_df[
        SOURCE_COLUMNS
    ].reset_index(drop=True).duplicated(keep="first")

    duplicate_count = int(expected_duplicate_mask.sum())

    duplicate_flags_valid = (
        len(df_classified) == len(raw_df)
        and df_classified["is_excess_exact_duplicate"]
        .reset_index(drop=True)
        .equals(expected_duplicate_mask.reset_index(drop=True))
    )

    add_check(
        "Duplicate identification",
        duplicate_flags_valid,
        f"Expected excess duplicates: {duplicate_count}.",
    )

    # ---------------------------------------------------------
    # 5. Original row-position integrity
    # ---------------------------------------------------------

    positions_available = (
        "original_row_position" in df_clean.columns
        and "original_row_position" in df_duplicate_audit.columns
    )

    if positions_available:

        clean_positions = df_clean[
            "original_row_position"
        ]

        audit_positions = df_duplicate_audit[
            "original_row_position"
        ]

        positions_unique = (
            clean_positions.is_unique
            and audit_positions.is_unique
        )

        positions_disjoint = set(clean_positions).isdisjoint(
            set(audit_positions)
        )

        all_positions = (
            set(clean_positions)
            | set(audit_positions)
        )

        positions_complete = (
            all_positions == set(range(total_records))
        )

        add_check(
            "Unique original row positions",
            positions_unique,
            "Positions must be unique within each output dataset.",
        )

        add_check(
            "Disjoint original row positions",
            positions_disjoint,
            "Cleaned and audit datasets must not share positions.",
        )

        add_check(
            "Complete original row positions",
            positions_complete,
            "Every source row must appear in exactly one output dataset.",
        )

    else:
        add_check(
            "Original row-position integrity",
            False,
            "Required original_row_position column is missing.",
        )

    # ---------------------------------------------------------
    # 6. Verify cleaned and audit datasets against classification
    # ---------------------------------------------------------

    if positions_available and len(df_classified) == total_records:

        clean_expected = (
            df_classified
            .iloc[clean_positions.to_numpy()]
            .reset_index(drop=True)
        )

        audit_expected = (
            df_classified
            .iloc[audit_positions.to_numpy()]
            .reset_index(drop=True)
        )

        clean_actual = df_clean[
            CLASSIFIED_COLUMNS
        ].reset_index(drop=True)

        audit_actual = df_duplicate_audit[
            CLASSIFIED_COLUMNS
        ].reset_index(drop=True)

        add_check(
            "Cleaned records match classified source",
            clean_expected.equals(clean_actual),
            "All classified fields must match at their original positions.",
        )

        add_check(
            "Audit records match classified source",
            audit_expected.equals(audit_actual),
            "All audit fields must match at their original positions.",
        )

    # ---------------------------------------------------------
    # 7. Original source-field preservation
    # ---------------------------------------------------------

    if positions_available:

        raw_clean = (
            raw_df.iloc[clean_positions.to_numpy()][SOURCE_COLUMNS]
            .reset_index(drop=True)
        )

        clean_source = (
            df_clean[SOURCE_COLUMNS]
            .reset_index(drop=True)
        )

        for column in SOURCE_COLUMNS:

            if column == "Description":
                continue

            add_check(
                f"Source field preserved: {column}",
                raw_clean[column].equals(clean_source[column]),
                "Original source values must remain unchanged.",
            )

        original_missing_description = (
            raw_clean["Description"].isna()
        )

        description_flag_valid = (
            original_missing_description.reset_index(drop=True)
            .equals(
                df_clean["Description_was_missing"]
                .reset_index(drop=True)
            )
        )

        add_check(
            "Original missing-description indicator",
            description_flag_valid,
            "Indicator must reflect the original source values.",
        )

        original_descriptions_preserved = (
            raw_clean.loc[
                ~original_missing_description,
                "Description"
            ]
            .reset_index(drop=True)
            .equals(
                df_clean.loc[
                    ~df_clean["Description_was_missing"],
                    "Description"
                ].reset_index(drop=True)
            )
        )

        add_check(
            "Originally populated descriptions preserved",
            original_descriptions_preserved,
            "Existing descriptions must not be overwritten.",
        )

    # ---------------------------------------------------------
    # 8. Description mapping validation
    # ---------------------------------------------------------

    mapping_path = (
        reference_dir / "description_mapping.csv"
    )

    if mapping_path.exists() and positions_available:

        mapping = pd.read_csv(
            mapping_path,
            dtype={"StockCode": "string"},
        )

        mapping_lookup = mapping.set_index(
            "StockCode"
        )["imputed_description"]

        imputed_mask = (
            df_clean["Description_was_missing"]
            & df_clean["Description"].notna()
        )

        expected_imputed_descriptions = (
            df_clean.loc[imputed_mask, "StockCode"]
            .astype("string")
            .map(mapping_lookup)
        )

        actual_imputed_descriptions = (
            df_clean.loc[imputed_mask, "Description"]
            .astype("string")
        )

        mapping_valid = (
            expected_imputed_descriptions.notna()
            & expected_imputed_descriptions.reset_index(drop=True).eq(
                actual_imputed_descriptions.reset_index(drop=True)
            )
        ).all()

        add_check(
            "Description imputation matches approved mapping",
            mapping_valid,
            f"Imputed records checked: {int(imputed_mask.sum())}.",
        )

    else:
        add_check(
            "Description mapping validation",
            False,
            "Mapping file or original row positions unavailable.",
        )

    # ---------------------------------------------------------
    # 9. Transaction classification
    # ---------------------------------------------------------

    classification_complete = (
        df_classified["transaction_category"].notna().all()
        and not df_classified["transaction_category"].eq(
            "unclassified"
        ).any()
    )

    add_check(
        "Transaction classification completeness",
        classification_complete,
        f"Unclassified records: "
        f"{df_classified['transaction_category'].eq('unclassified').sum()}.",
    )

    # ---------------------------------------------------------
    # 10. Taxonomy consistency
    # ---------------------------------------------------------

    taxonomy_path = (
        reference_dir / "transaction_taxonomy.csv"
    )

    if taxonomy_path.exists():

        taxonomy = pd.read_csv(taxonomy_path)

        expected_taxonomy = (
            df_classified[["transaction_category"]]
            .merge(
                taxonomy,
                on="transaction_category",
                how="left",
                validate="many_to_one",
            )
        )

        taxonomy_columns = [
            "merchandise_revenue_treatment",
            "customer_level_eligible",
            "qualifying_purchase",
            "notes",
        ]

        taxonomy_valid = all(
            expected_taxonomy[column]
            .reset_index(drop=True)
            .equals(
                df_classified[column].reset_index(drop=True)
            )
            for column in taxonomy_columns
        )

        add_check(
            "Transaction taxonomy consistency",
            taxonomy_valid,
            "Classification attributes must match the approved taxonomy.",
        )

    else:
        add_check(
            "Transaction taxonomy consistency",
            False,
            "Transaction taxonomy file not found.",
        )

    # ---------------------------------------------------------
    # 11. Analytical eligibility validation
    # ---------------------------------------------------------

    expected_customer_eligibility = (
        df_classified["customer_level_eligible"]
        & df_classified["Customer ID"].notna()
    )

    add_check(
        "Customer analytics eligibility",
        df_classified["is_customer_analytics_eligible"]
        .equals(expected_customer_eligibility),
        "Eligibility must require an identified customer.",
    )

    expected_qualifying_purchase = (
        df_classified["qualifying_purchase"]
        & df_classified["Customer ID"].notna()
        & (df_classified["Quantity"] > 0)
        & (df_classified["Price"] > 0)
    )

    add_check(
        "Qualifying purchase eligibility",
        df_classified["is_qualifying_purchase"]
        .equals(expected_qualifying_purchase),
        "Must satisfy taxonomy, customer ID, quantity, and price rules.",
    )

    # ---------------------------------------------------------
    # 12. Revenue calculation validation
    # ---------------------------------------------------------

    expected_line_value = (
        df_classified["Quantity"]
        * df_classified["Price"]
    )

    add_check(
        "Line value calculation",
        df_classified["line_value"].equals(expected_line_value),
        "Line value must equal Quantity multiplied by Price.",
    )

    expected_merchandise_revenue = (
        df_classified["line_value"].where(
            df_classified["is_merchandise_revenue_record"],
            0,
        )
    )

    add_check(
        "Merchandise revenue calculation",
        df_classified["merchandise_revenue"]
        .equals(expected_merchandise_revenue),
        "Revenue must follow the merchandise treatment flag.",
    )

    expected_qualifying_revenue = (
        df_classified["line_value"].where(
            df_classified["is_qualifying_purchase"],
            0,
        )
    )

    add_check(
        "Qualifying purchase revenue calculation",
        df_classified["qualifying_purchase_revenue"]
        .equals(expected_qualifying_revenue),
        "Revenue must only include qualifying paid purchases.",
    )

    # ---------------------------------------------------------
    # 13. Final validation report
    # ---------------------------------------------------------

    report = pd.DataFrame(results)

    return report

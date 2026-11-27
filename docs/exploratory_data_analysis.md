# Exploratory Data Analysis

## 1. Overview

### Objective

This phase explores the cleaned Online Retail II transaction dataset to understand its distributions, relationships, temporal patterns, product and geographic composition, and unusual transaction behavior.

The analysis is intended to:

- Identify important transaction-level patterns and revenue distributions.
- Understand how quantity, unit price, and transaction value relate.
- Examine monthly, weekly, and hourly activity.
- Explore product and country-level revenue concentration.
- Investigate unusual transactions and potential relationships between purchases and cancellations.
- Establish evidence and limitations to inform subsequent customer analytics and segmentation.

This phase is exploratory. It does not establish causal relationships, customer intent, profitability, or confirmed inventory movements.

### Dataset

The analysis uses the cleaned and validated dataset produced in Phase 3:

- **Source:** Online Retail II, UCI Machine Learning Repository.
- **Original dataset period:** December 2009 to December 2011.
- **Records analyzed:** 1,033,036.
- **Columns:** 33.
- **Observed transaction date range:** December 1, 2009, 07:45 to December 9, 2011, 12:50.
- **Primary analytical file:** `data/processed/online_retail_clean.parquet`.

The dataset includes transaction attributes, customer and country identifiers, product descriptions, engineered financial measures, transaction classifications, and data-quality indicators.

### Analytical conventions

The analysis preserves the distinctions established during data preparation:

- **Merchandise revenue:** Includes positive and negative merchandise transactions, including cancellation candidates.
- **Qualifying purchase revenue:** Includes eligible positive-quantity, positive-price purchases from identified customers. It does not subtract subsequent cancellations.
- **Transaction lines:** Individual product transaction records; they are not equivalent to physical units or invoices.
- **Invoice groups:** Analytical groups based on invoice identifier, timestamp, customer, and country. These groups are used to avoid merging repeated invoice identifiers across different timestamps.
- **Net quantity:** The sum of positive and negative quantities within the relevant analytical grouping.

Neither revenue measure represents profit or gross margin.

## 2. Data overview and distributions

### Dataset structure

The cleaned dataset contains 1,033,036 records and 33 columns. The principal remaining missing values are:

| Column | Missing records | Percentage |
|---|---:|---:|
| Customer ID | 235,151 | 22.76% |
| Description | 1,622 | 0.16% |
| Description_normalized | 1,622 | 0.16% |

The dataset covers 43 countries, 5,305 original StockCode values, and 5,131 normalized StockCode values.

The analysis retains anonymous transactions rather than removing them solely because customer identifiers are missing.

### Numerical distributions

The transaction-level numerical variables are strongly affected by skewness and extreme observations.

| Variable | Mean | Median | Standard deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| Quantity | 10.08 | 3 | 175.20 | -80,995 | 80,995 |
| Price | 4.61 | 2.10 | 122.40 | -53,594.36 | 38,970 |
| line_value | 18.25 | 9.92 | 295.69 | -168,469.60 | 168,469.60 |
| merchandise_revenue | 18.31 | 9.90 | 269.08 | -168,469.60 | 168,469.60 |
| qualifying_purchase_revenue | 16.52 | 6.96 | 196.12 | 0 | 168,469.60 |

The differences between means and medians, together with the extreme values, indicate that averages alone do not adequately describe typical transaction behavior.

The analysis therefore uses medians, percentiles, distribution counts, and restricted histogram ranges to examine central patterns without allowing extreme observations to dominate visual interpretation.

### Quantity distribution

Of all transaction records:

- 1,010,540 (97.82%) have positive quantities.
- 22,496 (2.18%) have negative quantities.
- No records have zero quantity.

Positive quantities are concentrated at relatively low values. In the central 1st–99th percentile range, the first two histogram bins account for approximately 70.28% of positive-quantity records.

Negative quantities are also concentrated near zero: approximately 90.50% of negative-quantity records fall within the first two bins of the central distribution examined.

Positive and negative quantities are analyzed separately because they represent different transaction patterns.

### Price distribution

Price records comprise:

- 1,027,017 positive-price records (99.42%).
- 6,014 zero-price records (0.58%).
- 5 negative-price records (approximately 0.00048%).

The five negative-price records are classified as bad-debt adjustments. They have StockCode `B`, description `Adjust bad debt`, missing customer identifiers, and UK as the country. Their combined value is -158,676.14.

These records are retained in the dataset but are not interpreted as ordinary merchandise purchases.

Zero-price records occur across multiple transaction categories, including operational adjustments, anonymous activity, identified-customer activity, delivery charges, manual transactions, test candidates, and packing charges. They are not automatically interpreted as free gifts or samples.

### Qualifying purchase revenue

Qualifying purchase revenue is zero for 256,532 records (24.83%) and positive for 776,504 records (75.17%).

Among positive records, the distribution is highly right-skewed. Approximately 78.63% of positive records fall within the first three histogram bins in the examined central 98% range.

This indicates that most eligible purchase lines have relatively low transaction values, while a small number of extreme observations form a long upper tail.

## 3. Relationships between numerical variables

### Quantity and unit price

For positive-quantity, positive-price merchandise records (1,007,914 records), the correlation results are:

| Variable pair | Pearson correlation | Spearman correlation |
|---|---:|---:|
| Quantity and Price | -0.00 | -0.43 |
| Quantity and line_value | 0.81 | 0.68 |
| Price and line_value | 0.25 | 0.31 |

The near-zero Pearson correlation but negative Spearman correlation between quantity and price suggests a negative monotonic association that is not well represented by a simple linear relationship.

The relationship was also examined within individual products. Among 3,418 products with valid Spearman correlations and at least 30 transaction records, the median product-level correlation was -0.49. A total of 3,280 products (95.96%) had negative correlations.

This suggests that the negative quantity–price association is not solely attributable to differences in product mix. However, the observational analysis does not establish that larger quantities cause lower unit prices.

### Quantity and line value

Quantity has a positive relationship with line value, which is expected in part because line value is calculated from quantity and unit price.

Median line value generally increases across larger quantity groups, although the relationship is not strictly monotonic. For example, the median line value decreases from 16.50 in the 6–10 quantity group to 15.00 in the 11–20 group.

This relationship should not be interpreted as an independent business effect because quantity is a component of the line-value calculation.

## 4. Temporal analysis

### Monthly activity

Monthly activity and revenue vary across the observed period.

November is the strongest month in both years for several activity and revenue measures:

| Measure | November 2010 | November 2011 |
|---|---:|---:|
| Merchandise revenue | 1,394,652.86 | 1,423,318.71 |
| Qualifying purchase revenue | 1,155,978.39 | 1,136,121.50 |

November 2011 recorded the highest monthly transaction-line count, with 83,343 lines. November 2010 recorded the highest monthly invoice count, with 3,669 invoices.

December 2011 contains data only through December 9 and is therefore excluded from full-month comparisons.

### Year-over-year comparison

For January–November, 2011 compared with the corresponding months of 2010:

| Measure | Year-over-year change |
|---|---:|
| Transaction lines | +3.6% |
| Invoice groups | -8.5% |
| Identified customers | -2.1% |
| Merchandise revenue | +2.1% |
| Qualifying purchase revenue | -0.4% |

Transaction lines increased while invoice groups and identified customers decreased. This indicates a change in the observed transaction composition, but does not by itself explain the underlying business causes.

Average transaction lines per invoice group were higher in every comparable month except April 2011. This indicates more product-line records per analytical invoice group, not necessarily more physical units.

### Weekday patterns

Thursday recorded the highest transaction-line count and qualifying purchase revenue:

- 196,189 transaction lines.
- 11,335 invoice groups.
- 3,687,563.25 qualifying purchase revenue.

Saturday recorded only 402 transaction lines and 32 invoice groups. Sunday, however, had substantial activity, with 133,017 transaction lines.

The low Saturday activity is an observed pattern. The available data does not establish whether it reflects operating schedules, data coverage, or another cause.

### Hourly patterns

Activity peaked at 12:00:

- 154,256 transaction lines.
- 8,098 invoice groups.
- 2,753 identified customers.
- 2,659,699.24 qualifying purchase revenue.

The 11:00–15:00 period accounted for approximately 66.21% of transaction lines and 63.71% of qualifying purchase revenue.

Activity declined after 16:00. Very low activity at the earliest and latest observed hours should be interpreted cautiously.

## 5. Product analysis

### Product-level activity and revenue

Product performance was examined using normalized stock codes and descriptions.

The most frequently recorded product was `WHITE HANGING HEART T-LIGHT HOLDER` (StockCode `85123A`), with 5,752 transaction lines.

The highest qualifying purchase revenue among the products examined was recorded for `REGENCY CAKESTAND 3 TIER` (StockCode `22423`), at 277,656.25.

The product `PAPER CRAFT, LITTLE BIRDIE` (StockCode `23843`) ranked highly by qualifying purchase revenue, with 168,469.60, despite having only two transaction lines. One large purchase was followed by a full cancellation 12 minutes later. This illustrates why gross qualifying purchase revenue must not be interpreted as net realized merchandise revenue.

### Product revenue concentration

Net merchandise revenue is distributed across a broad product catalogue:

| Product group | Share of net merchandise revenue |
|---|---:|
| Top 10 products | 7.63% |
| Top 20 products | 11.03% |
| Top 50 products | 19.07% |
| Top 100 products | 28.96% |

Approximately 289 products account for 50% of net merchandise revenue, 674 for 70%, 1,036 for 80%, and 1,684 for 90%.

No individual product contributes more than 2% of total net merchandise revenue. This indicates that revenue is not dominated by a small number of individual stock codes. It does not establish concentration at broader product-category or brand levels.

### Geographic product mix

The Regency Cakestand appears among the top ten products in each of the five countries examined: UK, EIRE, Germany, Netherlands, and Australia.

Other products appear repeatedly across subsets of these countries, including Rabbit Night Light, Red Toadstool LED Night Light, and Spaceboy Lunch Box.

These overlaps describe similarities in top product revenue rankings, not definitive customer preferences.

The top ten products account for a larger share of qualifying purchase revenue in the Netherlands than in the UK, indicating greater concentration among the leading individual products in the Netherlands within this comparison.

## 6. Geographic analysis

### Country-level revenue concentration

The UK dominates observed merchandise revenue:

| Country | Merchandise revenue | Share of total merchandise revenue |
|---|---:|---:|
| United Kingdom | 16,161,392.63 | 85.42% |
| EIRE | 603,116.61 | 3.19% |
| Netherlands | 546,095.43 | 2.89% |
| Germany | 374,573.51 | 1.98% |
| France | 293,423.70 | 1.55% |

The five countries together account for approximately 95.02% of net merchandise revenue.

Country-level customer counts require caution. The same customer may appear in more than one country, and some countries have relatively few identified customers despite substantial invoice activity.

For example, EIRE has 806 invoice groups but only five distinct identified customer IDs in the dataset. This is an observed data characteristic, not an explanation of customer behavior.

### Revenue per invoice group

Average merchandise revenue per invoice group varies substantially by country.

Examples include:

- Netherlands: 2,199.09.
- Australia: 1,434.19.
- EIRE: 727.81.
- Germany: 350.04.
- United Kingdom: 290.94.

The Netherlands average is approximately 7.56 times the UK average, despite a similar average number of transaction lines per invoice group.

Differences in product mix, quantities, and unit prices may contribute to this pattern. The analysis does not establish a specific cause. Countries with very few invoice groups have unstable averages and should not be ranked without considering sample size.

## 7. Anomaly and pattern investigation

### Analytical invoice groups

The cleaned data contains 53,628 distinct original invoice identifiers. However, 83 identifiers are associated with two distinct timestamps, one minute apart.

To avoid combining these separate timestamp groups, the analysis created 53,711 analytical invoice groups using invoice identifier, timestamp, customer, and country.

The resulting analytical group identifier is unique across the aggregated invoice dataset and was mapped back to the transaction records.

This is an analytical grouping decision. It does not establish the commercial meaning of repeated source invoice identifiers.

### Invoice composition

Analytical invoice groups were classified according to the presence of positive merchandise revenue, negative merchandise revenue, and qualifying purchases.

| Invoice composition | Invoice groups | Transaction lines |
|---|---:|---:|
| Positive merchandise only | 39,599 | 1,007,471 |
| Negative merchandise only | 7,422 | 18,085 |
| No merchandise revenue | 6,690 | 7,480 |

No analytical invoice groups contained both positive and negative merchandise revenue under this classification.

### Extreme invoice groups

The 20 largest positive invoice groups totalled approximately 385,894.39 in merchandise revenue. The 20 largest negative groups totalled approximately -297,795.03.

Their combined net value was approximately 88,099.36.

Examples include:

- Customer 16446 purchased 80,995 units of `PAPER CRAFT, LITTLE BIRDIE` for 168,469.60. A cancellation for the same quantity and value followed 12 minutes later.
- Customer 12346 purchased 74,215 units of `MEDIUM CERAMIC TOP STORAGE JAR` for 77,183.60. A cancellation for the same quantity and value followed 16 minutes later.

These are strong arithmetic reversals at the transaction level, although the underlying commercial reason is not available.

### High-priced merchandise

A targeted investigation of positive-quantity merchandise records priced at 100 or above identified 178 records across 19 product-price combinations.

Many high-priced records correspond to recurring furniture products, such as vintage kitchen cabinets, sideboards, and mirrors.

One unusual case involved `PICNIC BASKET WICKER 60 PIECES` at 649.50. The product-price combination appeared in only two records, involving one identified customer. The same customer also had transactions involving a similarly named smaller picnic basket at a much lower price.

The evidence supports flagging this product-price combination for review, not declaring it an error.

### Purchase-to-cancellation matching

The 215 transaction lines underlying the 20 largest negative invoice groups were examined for earlier purchase candidates.

Exact matching required the same customer, normalized product code, absolute quantity, unit price, and an earlier timestamp.

| Matching classification | Cancellation lines |
|---|---:|
| One exact earlier purchase candidate | 126 |
| Multiple exact earlier purchase candidates | 70 |
| No exact earlier purchase candidate | 19 |

Of the 19 lines without an exact candidate, 17 had at least one earlier purchase candidate for the same customer and product when quantity and price requirements were relaxed. Two had no earlier same-customer, same-product purchase candidate.

These are candidate relationships, not confirmed purchase-to-cancellation links. Multiple candidate purchases, prior partial cancellations, and missing source-level linkage prevent definitive allocation.

### Customer 12931 case study

Two purchase invoices, `562439` and `563074`, occurred on August 4 and August 11, 2011. Two cancellation invoices, `C564940` and `C565044`, occurred on August 31.

Fourteen stock codes appeared in both the purchases and cancellations. For every overlapping stock code, the cancellation quantity was within the combined quantity purchased in the two earlier invoices.

Most unit prices matched. Two details require caution:

- StockCode `20974` had a purchase price of 0.55 and a cancellation price of 0.65.
- StockCode `23203` had different descriptions between purchase and cancellation records, despite sharing the same normalized stock code.

This is a strong product-level and temporal association with plausible partial cancellation. It does not prove that the cancellations reverse specific lines from the two purchase invoices.

## 8. Key findings

The EDA produced the following evidence-based observations:

1. Transaction-level quantities, prices, and revenue measures are highly skewed and affected by extreme observations.
2. Most positive purchase quantities and qualifying purchase values are concentrated at relatively low transaction values.
3. Quantity and unit price have a negative monotonic association, including within many individual products.
4. Transaction activity and revenue show meaningful temporal variation, with November particularly strong in both observed years.
5. The UK accounts for approximately 85.42% of net merchandise revenue.
6. Revenue is distributed across a broad range of individual products rather than dominated by a few stock codes.
7. Some large cancellations have plausible relationships with earlier purchases, but exact purchase-to-cancellation linkage is not consistently available.
8. Repeated invoice identifiers require timestamp-aware analytical grouping.
9. Unusual prices, quantities, and zero-value transactions should be investigated and classified rather than automatically removed.

## 9. Limitations

The analysis has several limitations:

- The dataset does not provide explicit links between original purchase lines and cancellation lines.
- Missing customer identifiers limit customer-level attribution for a substantial portion of transaction records.
- The observed period ends on December 9, 2011; December 2011 is incomplete.
- Revenue measures do not include product costs, operating costs, or profit margins.
- Qualifying purchase revenue does not subtract cancellations.
- Correlations describe associations and do not establish causality.
- Country and product comparisons may be affected by differences in sample sizes and transaction composition.
- Invoice grouping is an analytical convention and does not verify the commercial meaning of source invoice identifiers.
- Extreme transaction investigations focus on selected cases and should not be generalized to all records.

## 10. Conclusion and next phase

Phase 5 establishes a transaction-level understanding of the dataset, including its distributions, relationships, temporal patterns, product and geographic composition, and unusual transaction behavior.

The findings provide a foundation for Phase 6: **Customer Analytics & Segmentation**.

The next phase will shift the unit of analysis from individual transaction records to identified customers. It will examine customer recency, purchase frequency, monetary contribution, revenue concentration, and behavioral segments.

## Data source

Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6H. Licensed under CC BY 4.0.
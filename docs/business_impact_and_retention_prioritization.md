# Business Impact & Retention Prioritization

## 1. Overview

This phase translates customer purchase-propensity predictions into a business-oriented customer prioritization framework.

The objective is to combine predicted repeat-purchase probability with historical customer monetary value to identify customer groups that may warrant different levels of retention attention.

The analysis uses the selected Logistic Regression model from Phase 9 and the held-out test-period observations. It does not retrain or retune the model, change its decision threshold, or use test outcomes to assign customer priorities.

The resulting framework distinguishes customers based on:

- Predicted likelihood of making another purchase within 90 days.
- Historical qualifying purchase value during the preceding 180 days.

The analysis also evaluates customer purchasing behavior, compares alternative prioritization scenarios, and develops recommendations for potential retention strategies.

## 2. Analytical Framework

### 2.1 Prediction Dataset

The customer prioritization dataset was reconstructed using the selected Logistic Regression pipeline from Phase 9.

The model was trained using the training partition and generated repeat-purchase probabilities for the test partition.

| Metric | Value |
|---|---:|
| Test customer-snapshot observations | 5,534 |
| Unique customers in test observations | 2,968 |
| Final customer-level records | 2,968 |
| Customers with August 1, 2011 snapshot | 200 |
| Customers with September 1, 2011 snapshot | 2,768 |

For customers with multiple test-period observations, the latest available snapshot was retained.

Consequently, the customer-level prioritization dataset contains each customer's latest available snapshot, rather than a single common snapshot date.

All 2,968 customer records were retained, with no missing values in the analytical dataset.

### 2.2 Historical Monetary Value

Historical monetary value was reconstructed from the `log1p_monetary` feature:

`historical_monetary_180d = expm1(log1p_monetary)`

This represents the customer's qualifying purchase value during the preceding 180-day feature window.

It is not lifetime customer value, profit, or future revenue.

The historical monetary value distribution was strongly right-skewed.

| Statistic | Predicted probability | Historical monetary value |
|---|---:|---:|
| Count | 2,968 | 2,968 |
| Mean | 0.5233 | 1,197.23 |
| Standard deviation | 0.1975 | 4,213.65 |
| Minimum | 0.1252 | 2.90 |
| 25th percentile | 0.3581 | 229.31 |
| Median | 0.4791 | 454.18 |
| 75th percentile | 0.6792 | 1,037.29 |
| 90th percentile | 0.8159 | 2,104.76 |
| Maximum | 0.9966 | 118,081.92 |

### 2.3 Priority Classification

Two median-based thresholds were used to construct a 2 × 2 customer priority matrix.

- Predicted repeat-purchase probability: 0.4791.
- Historical monetary value: 454.18.

Customers with predicted probabilities at or above 0.4791 were classified as high propensity. Customers with historical monetary value at or above 454.18 were classified as high value.

The four priority groups were:

| Priority group | Classification |
|---|---|
| Priority 1 | High value, low propensity |
| Priority 2 | High value, high propensity |
| Priority 3 | Low value, low propensity |
| Priority 4 | Low value, high propensity |

These are analytical cutoffs based on the test-period customer population, not validated business thresholds.

## 3. Customer Priority Matrix

### 3.1 Group-Level Results

| Priority group | Customers | Customer share | Median probability | Mean probability | Median historical value | Total historical value | Historical value share |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 — High value, low propensity | 228 | 7.68% | 0.4310 | 0.4237 | 596.74 | 159,677.46 | 4.49% |
| P2 — High value, high propensity | 1,256 | 42.32% | 0.7119 | 0.7164 | 1,206.63 | 3,043,099.13 | 85.64% |
| P3 — Low value, low propensity | 1,256 | 42.32% | 0.3458 | 0.3434 | 205.97 | 275,587.57 | 7.76% |
| P4 — Low value, high propensity | 228 | 7.68% | 0.5350 | 0.5495 | 337.17 | 75,012.29 | 2.11% |
| **Total** | **2,968** | **100.00%** | | | | **3,553,376.45** | **100.00%** |

### 3.2 Retrospective Repeat-Purchase Outcomes

The actual 90-day target was used only to evaluate the priority groups retrospectively. It was not used to assign customer priorities.

| Priority group | Predicted repeat probability | Actual repeat rate | Repeat customers | Non-repeat customers |
|---|---:|---:|---:|---:|
| P1 — High value, low propensity | 42.37% | 41.67% | 95 | 133 |
| P2 — High value, high propensity | 71.64% | 78.90% | 991 | 265 |
| P3 — Low value, low propensity | 34.34% | 40.61% | 510 | 746 |
| P4 — Low value, high propensity | 54.95% | 57.89% | 132 | 96 |

The observed outcomes broadly support the distinction between high- and low-propensity groups.

However, the results also show that predicted propensity alone does not determine business priority. Historical monetary value provides an additional dimension for allocating attention.

## 4. Snapshot-Specific RFM Analysis

To avoid using future information from the full-history RFM analysis in Phase 6, customer purchasing behavior was profiled using features available within each customer's 180-day snapshot window.

The analysis used:

- Recency: days since the most recent qualifying purchase.
- Frequency: number of qualifying purchase invoice groups during the preceding 180 days.
- Monetary: qualifying purchase value during the preceding 180 days.

The features were used to describe the priority groups, not to create additional priority classifications.

### 4.1 RFM Profile by Priority Group

| Priority group | Median recency | Mean recency | Median frequency | Mean frequency | Median monetary | Mean monetary | Actual repeat rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 111.0 | 106.88 | 1 | 1.04 | 596.74 | 700.34 | 41.67% |
| P2 | 28.0 | 38.66 | 3 | 4.69 | 1,206.63 | 2,422.85 | 78.90% |
| P3 | 108.0 | 103.37 | 1 | 1.07 | 205.96 | 219.42 | 40.61% |
| P4 | 44.5 | 50.05 | 2 | 2.38 | 337.16 | 329.00 | 57.89% |

### 4.2 Interpretation

**Priority 1 — Historically valuable, but less active**

P1 customers have a median historical monetary value of 596.74, but a median recency of 111 days and median frequency of one purchase.

Their relatively high historical value combined with limited recent purchasing activity makes this group a potential candidate for focused retention review.

**Priority 2 — Strong purchasing momentum**

P2 customers have the lowest median recency at 28 days, the highest median frequency at three purchases, and the highest median monetary value at 1,206.63.

Their 78.90% observed repeat-purchase rate supports a relationship-maintenance approach rather than treating the entire group as at risk.

**Priority 3 — Low historical value and limited activity**

P3 customers have a median recency of 108 days, median frequency of one purchase, and median monetary value of 205.96.

Their actual repeat-purchase rate of 40.61% is close to P1's 41.67%. This demonstrates why propensity alone is insufficient for determining business priority.

**Priority 4 — Lower value, but stronger purchasing momentum**

P4 customers have a median recency of 44.5 days and median frequency of two purchases. Their actual repeat-purchase rate is 57.89%.

This group may be suitable for lower-intensity engagement or growth-oriented initiatives.

## 5. Business Prioritization Scenarios

Four scenarios were compared to evaluate the trade-offs between customer coverage and historical monetary value.

### 5.1 Scenario Comparison

| Scenario | Customers | Customer coverage | Historical monetary value | Historical value share | Mean predicted probability | Actual repeat rate |
|---|---:|---:|---:|---:|---:|---:|
| A — Focused retention | 228 | 7.68% | 159,677.46 | 4.49% | 0.4237 | 41.67% |
| B — Broad risk coverage | 1,484 | 50.00% | 435,265.03 | 12.25% | 0.3558 | 40.77% |
| C — High-value customer coverage | 1,484 | 50.00% | 3,202,776.59 | 90.13% | 0.6715 | 73.18% |
| D — Full customer coverage | 2,968 | 100.00% | 3,553,376.45 | 100.00% | 0.5233 | 58.22% |

### 5.2 Scenario Interpretation

**Scenario A — Focused retention**

This scenario targets P1 customers only.

It covers 7.68% of customers and represents 4.49% of historical monetary value. Its relatively small population makes it suitable for focused customer review and potentially personalized engagement.

**Scenario B — Broad risk coverage**

This scenario includes P1 and P3, covering all customers classified as low propensity.

It includes 50% of the customer population but represents only 12.25% of historical monetary value.

The scenario provides broader behavioral-risk coverage, but its lower historical value concentration suggests that resource-intensive treatment may not be appropriate for every customer.

**Scenario C — High-value customer coverage**

This scenario includes P1 and P2, covering all customers classified as high value.

It represents 90.13% of historical monetary value while covering 50% of customers.

However, most of these customers already have high predicted repeat-purchase propensity. This scenario is therefore better interpreted as a customer relationship-maintenance strategy than a focused at-risk retention strategy.

**Scenario D — Full customer coverage**

This scenario includes the entire customer population.

It provides complete coverage but does not differentiate intervention intensity by customer behavior or historical value.

### 5.3 Scenario Implications

The comparison illustrates that customer coverage and historical monetary value are not distributed proportionally.

- P1 provides a relatively focused population for retention review.
- P1 and P3 together provide broader low-propensity coverage.
- P1 and P2 together capture most of the historical monetary value.
- Full coverage may be appropriate for general customer communication, but not necessarily for allocating high-cost retention resources.

These scenarios compare customer selection strategies. They do not estimate campaign effectiveness, incremental repeat purchases, or financial returns.

## 6. Historical Value by Observed Outcome

To understand the historical value associated with customers who did not repeat purchase, historical monetary value was aggregated by priority group and actual 90-day outcome.

### 6.1 Results

| Priority group | Outcome | Customers | Historical monetary value | Mean historical value per customer | Share of group value |
|---|---|---:|---:|---:|---:|
| P1 | No repeat purchase | 133 | 95,168.45 | 715.55 | 59.60% |
| P1 | Repeat purchase | 95 | 64,509.01 | 679.04 | 40.40% |
| P2 | No repeat purchase | 265 | 381,684.12 | 1,440.32 | 12.54% |
| P2 | Repeat purchase | 991 | 2,661,415.01 | 2,685.59 | 87.46% |
| P3 | No repeat purchase | 746 | 157,512.81 | 211.14 | 57.16% |
| P3 | Repeat purchase | 510 | 118,074.76 | 231.52 | 42.84% |
| P4 | No repeat purchase | 96 | 30,188.70 | 314.47 | 40.25% |
| P4 | Repeat purchase | 132 | 44,823.59 | 339.57 | 59.75% |

### 6.2 Interpretation

**Priority 1**

P1 has the highest proportion of historical monetary value associated with non-repeat outcomes: 59.60%.

The 133 non-repeat customers account for 95,168.45 in historical monetary value, making P1 the strongest focused retention candidate in this analysis.

**Priority 2**

P2 has the largest absolute historical monetary value associated with non-repeat outcomes: 381,684.12.

However, this represents only 12.54% of the group's historical monetary value. Most P2 customers repeated purchase, so the entire group should not be treated as equally at risk.

**Priority 3**

P3 has 746 non-repeat customers and 157,512.81 in historical monetary value associated with those outcomes.

Its non-repeat value share of 57.16% is close to P1's, but its mean historical value per non-repeat customer is substantially lower.

This supports considering scalable, lower-cost engagement for P3 rather than applying the same treatment as P1.

**Priority 4**

P4 has 30,188.70 in historical monetary value associated with non-repeat outcomes, representing 40.25% of its group value.

Its higher observed repeat-purchase rate supports a lower-intensity engagement approach.

### 6.3 Interpretation Boundary

Historical monetary value associated with non-repeat outcomes is a retrospective descriptive measure.

It must not be interpreted as:

- Revenue lost.
- Revenue at risk.
- Revenue that could have been recovered.
- Expected future revenue.
- Revenue saved by a retention campaign.

The analysis does not establish whether a customer would have purchased again if an intervention had been applied.

## 7. Business Recommendations

Based on the combined propensity predictions, historical monetary value, snapshot-specific RFM profiles, and retrospective outcomes, a tiered customer prioritization strategy is recommended.

### 7.1 Priority 1 — Focused Retention Review

**Recommended approach:** Prioritize P1 for focused retention review and potentially personalized engagement.

P1 contains 228 customers, representing 7.68% of the population.

Its historical monetary value is relatively high, while purchasing activity is limited. Furthermore, 59.60% of its historical monetary value is associated with customers who did not repeat purchase.

Potential next steps include reviewing customer purchase history, identifying changes in purchasing patterns, and evaluating appropriate re-engagement approaches.

### 7.2 Priority 3 — Scalable, Lower-Cost Engagement

**Recommended approach:** Consider scalable engagement initiatives for P3.

P3 contains 1,256 customers, including 746 customers who did not repeat purchase.

Although the group has a similar non-repeat value proportion to P1, its historical monetary value per customer is considerably lower.

Lower-cost communication or engagement experiments may therefore be more appropriate than resource-intensive personalized interventions.

### 7.3 Priority 2 — Relationship Maintenance

**Recommended approach:** Maintain customer relationships and monitor changes in purchasing behavior.

P2 contains 85.64% of the total historical monetary value in the prioritization population.

Its customers demonstrate relatively recent purchasing activity, higher frequency, and a 78.90% observed repeat-purchase rate.

Customer experience, product availability, and continued relationship maintenance may be important considerations for this group.

### 7.4 Priority 4 — Growth Opportunities

**Recommended approach:** Consider routine engagement and growth-oriented opportunities.

P4 customers have relatively recent purchasing activity and a 57.89% observed repeat-purchase rate.

Potential initiatives could include product recommendations, cross-selling, and customer engagement experiments.

These opportunities should be evaluated before allocating substantial retention resources.

## 8. Limitations

Several limitations must be considered when interpreting the results.

### 8.1 Repeat Purchase Is Not Permanent Churn

The target measures whether a customer made at least one qualifying purchase within the next 90 days.

A customer without a purchase during this period is classified as a non-repeat outcome for the analysis. This does not establish permanent churn or customer loss.

### 8.2 Historical Monetary Value Is Not Customer Lifetime Value

Historical monetary value covers the preceding 180-day feature window.

It does not represent lifetime value, profit, contribution margin, or future revenue.

### 8.3 Snapshot Dates Are Not Uniform

The final customer-level dataset uses each customer's latest available test-period snapshot.

The retained snapshots are August 1 or September 1, 2011. Therefore, the customer-level analysis does not represent one common observation date.

### 8.4 Priority Thresholds Are Analytical

The probability and monetary thresholds are based on the medians of the test-period customer population.

They provide a transparent initial segmentation framework, but they have not been validated against operational capacity, campaign costs, or business-specific retention economics.

### 8.5 No Causal Intervention Analysis

The analysis does not include campaign assignments, treatment groups, intervention outcomes, or randomized experiments.

Consequently, it cannot establish whether a particular retention strategy would increase repeat purchases.

### 8.6 No ROI or Revenue-Saved Calculation

The dataset does not provide the campaign costs, margins, intervention effectiveness, or incremental revenue information required to calculate ROI or revenue saved.

### 8.7 Customer Overlap Across Temporal Partitions

Customers may appear in more than one temporal partition. The model's evaluation therefore does not establish generalization to entirely unseen customers.

## 9. Conclusion

This phase demonstrates how predictive modeling results can be translated into a practical customer prioritization framework.

Combining predicted repeat-purchase probability with historical monetary value reveals meaningful differences between customers who may require focused retention attention, scalable engagement, relationship maintenance, or growth-oriented initiatives.

The most actionable finding is the distinction between P1 and P3. Both groups have relatively low predicted repeat-purchase propensity and similar observed non-repeat rates, but P1 has substantially higher historical monetary value per customer.

P2, meanwhile, represents the largest share of historical monetary value and should be considered important for relationship maintenance, even though its predicted repeat-purchase propensity is already high.

The resulting framework provides a foundation for targeted business decisions and future retention experiments. However, its recommendations remain analytical hypotheses until tested through actual interventions and measured against incremental outcomes.

**Phase 10 deliverable:** A customer prioritization framework combining repeat-purchase propensity, historical monetary value, snapshot-specific RFM behavior, scenario comparison, and business recommendations.
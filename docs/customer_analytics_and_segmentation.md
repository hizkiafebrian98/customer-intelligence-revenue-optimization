# Customer Analytics and Segmentation

## 1. Overview

This phase analyzes customer purchasing behavior, customer value, revenue concentration, and behavioral segments using the cleaned Online Retail II dataset.

The analysis has two complementary objectives:

1. Develop an interpretable, rule-based RFM segmentation framework.
2. Apply K-Means clustering to identify behavioral groupings from customer purchasing metrics.

Cancellation behavior is also examined as a supplementary analytical dimension.

The objective is to translate historical purchasing patterns into actionable customer retention and engagement recommendations.

## 2. Dataset and Analytical Population

### 2.1 Customer population

The analytical population consists of customers with at least one qualifying purchase.

| Measure | Result |
|---|---:|
| Qualifying purchase records | 776,504 |
| Unique eligible customers | 5,852 |
| Customers with cancellation records | 2,446 |
| Customers with both purchases and cancellations | 2,423 |
| Cancellation-only customers | 23 |

The 23 cancellation-only customers are excluded from the customer segmentation population because they do not have qualifying purchases.

### 2.2 Analytical definitions

The following definitions are used throughout the analysis:

- **Observation date:** December 10, 2011, one day after the last observed purchase date.
- **Recency:** Number of days between the observation date and the customer's most recent qualifying purchase.
- **Frequency:** Number of distinct analytical invoice groups associated with qualifying purchases.
- **Monetary:** Sum of qualifying purchase revenue for each customer.
- **Purchase lines:** Number of qualifying transaction lines.
- **Unique products:** Number of distinct normalized stock codes purchased.

Monetary represents gross qualifying purchase revenue. It is not profit or net revenue after cancellations.

Cancellation activity is analyzed separately rather than deducted from purchase monetary values.

## 3. Customer Purchasing Behavior

### 3.1 RFM metric distributions

The customer-level dataset contains 5,852 customers.

| Metric | Mean | Median | 25th percentile | 75th percentile | Maximum |
|---|---:|---:|---:|---:|---:|
| Recency (days) | 200.73 | 96 | 26 | 380 | 739 |
| Frequency | 6.26 | 3 | 1 | 7 | 375 |
| Monetary (£) | 2,916.49 | 856.02 | 339.46 | 2,241.03 | 580,987.04 |

Frequency and monetary distributions are strongly right-skewed.

The maximum frequency of 375 invoices and maximum monetary value of £580,987.04 demonstrate substantial differences in purchasing behavior across customers.

Log transformations of frequency and monetary substantially improve distribution shape for clustering. Original values are retained for business interpretation.

### 3.2 Purchase frequency

| Purchase frequency | Customers | Percentage |
|---|---:|---:|
| 1 invoice | 1,615 | 27.60% |
| 2 invoices | 945 | 16.15% |
| 3–4 invoices | 1,146 | 19.58% |
| 5–8 invoices | 1,027 | 17.55% |
| 9+ invoices | 1,119 | 19.12% |

Approximately 43.75% of customers have only one or two observed purchase invoices.

The distribution suggests that encouraging repeat purchasing is an important potential growth opportunity.

### 3.3 Recency distribution

Recency is highly dispersed.

A notable concentration occurs between 360 and 420 days since the last qualifying purchase: 537 customers, representing 9.18% of the population.

The concentration is associated with the historical distribution of customers' last observed purchase dates. It should not automatically be interpreted as evidence of a particular customer behavior or cause.

## 4. Customer Value and Revenue Concentration

Revenue is concentrated among a relatively small proportion of customers.

| Customer population | Customers | Cumulative revenue share |
|---|---:|---:|
| Top 1% | 59 | 32.09% |
| Top 5% | 293 | 51.98% |
| Top 10% | 586 | 63.90% |
| Top 20% | 1,171 | 77.17% |
| Top 30% | 1,756 | 84.96% |
| Top 50% | 2,926 | 93.53% |

The top 10% of customers contribute 63.90% of qualifying purchase revenue.

This concentration makes the retention of high-value customer relationships an important business priority.

### 4.1 Revenue by purchase frequency

| Purchase frequency | Customers | Revenue share |
|---|---:|---:|
| 1 invoice | 1,615 | 3.25% |
| 2 invoices | 945 | 4.72% |
| 3–4 invoices | 1,146 | 8.50% |
| 5–8 invoices | 1,027 | 13.68% |
| 9+ invoices | 1,119 | 69.84% |

Customers with nine or more purchase invoices contribute 69.84% of qualifying purchase revenue.

This reinforces the importance of repeat purchasing and customer relationship development.

## 5. RFM Segmentation

### 5.1 Scoring methodology

RFM scoring evaluates customers across three dimensions:

- Recency: How recently the customer purchased.
- Frequency: How often the customer purchased.
- Monetary: How much qualifying purchase revenue the customer generated.

Recency and monetary scores use five-level quantile scoring.

Recency is reverse-scored: a lower recency value receives a higher score.

Frequency uses business-defined thresholds because its distribution contains many tied values:

| Frequency | Score |
|---|---:|
| 1 invoice | 1 |
| 2 invoices | 2 |
| 3–4 invoices | 3 |
| 5–8 invoices | 4 |
| 9+ invoices | 5 |

The three scores are combined into an RFM total ranging from 3 to 15.

### 5.2 Business-facing segments

Six mutually exclusive segments are defined using ordered RFM conditions.

| Segment | Customers | Population share | Revenue | Revenue share |
|---|---:|---:|---:|---:|
| Champions | 1,254 | 21.43% | £11,555,689.88 | 67.71% |
| Loyal customers | 603 | 10.30% | £1,742,374.26 | 10.21% |
| Recent high-value | 168 | 2.87% | £529,704.44 | 3.10% |
| At-risk valuable | 782 | 13.36% | £1,698,154.20 | 9.95% |
| Hibernating | 1,352 | 23.10% | £347,790.42 | 2.04% |
| Other customers | 1,693 | 28.93% | £1,193,565.52 | 6.99% |

### 5.3 Segment interpretation

**Champions**

These customers are recent, frequent, and high-value purchasers. They represent 21.43% of customers but contribute 67.71% of qualifying purchase revenue.

**Loyal customers**

These customers demonstrate relatively frequent purchasing and meaningful monetary value, although their RFM scores do not meet all Champion criteria.

**Recent high-value**

These customers have recently purchased and demonstrate relatively high monetary value, but their purchasing frequency is comparatively lower.

**At-risk valuable**

These customers have relatively high recency and meaningful historical frequency or monetary value. Their inactivity makes them candidates for re-engagement.

**Hibernating**

These customers have high recency, low frequency, and low monetary scores.

**Other customers**

This segment contains customers who do not meet the conditions of the other five segments.

## 6. K-Means Clustering

### 6.1 Feature engineering

K-Means uses three customer-level features:

- Recency in its original scale.
- Log-transformed frequency: `log1p(frequency)`.
- Log-transformed monetary: `log1p(monetary)`.

The features are standardized using `StandardScaler`.

Customer IDs and supplementary profiling metrics such as purchase lines and unique products are excluded from clustering.

### 6.2 Model selection

Candidate cluster counts from K=2 through K=10 are evaluated using inertia and silhouette scores.

| K | Inertia | Silhouette score |
|---:|---:|---:|
| 2 | 8,854.55 | 0.4183 |
| 3 | 5,698.14 | 0.4015 |
| 4 | 4,458.06 | 0.3614 |
| 5 | 3,631.42 | 0.3645 |
| 6 | 3,071.22 | 0.3481 |
| 7 | 2,729.98 | 0.3357 |
| 8 | 2,466.09 | 0.3156 |
| 9 | 2,282.52 | 0.3106 |
| 10 | 2,131.14 | 0.2997 |

K=2 achieves the highest silhouette score, but produces a broader segmentation with less business differentiation.

K=4 is selected as a practical compromise between cluster separation, behavioral differentiation, and business interpretability. It is not claimed to be the mathematical optimum.

### 6.3 Cluster profiles

| Cluster | Customers | Population share | Median recency | Median frequency | Median monetary | Revenue share |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 936 | 15.99% | 18 | 15 | £6,135.50 | 70.83% |
| 1 | 1,635 | 27.94% | 458 | 1 | £330.12 | 4.95% |
| 2 | 1,871 | 31.97% | 57 | 5 | £1,572.55 | 20.71% |
| 3 | 1,410 | 24.09% | 71 | 2 | £372.51 | 3.51% |

The clusters are interpreted as:

- **Cluster 0 — High-value frequent purchasers:** Recently active customers with high purchasing frequency and monetary value.
- **Cluster 1 — Long-inactive low-frequency customers:** Customers with very high recency and low purchasing frequency.
- **Cluster 2 — Active established repeat purchasers:** Customers with relatively recent activity and established purchasing behavior.
- **Cluster 3 — Recent low-frequency purchasers:** Customers with relatively recent activity but limited purchasing frequency and monetary value.

### 6.4 Cluster evaluation

The K=4 silhouette score is 0.3614.

Sample-level silhouette analysis shows:

| Cluster | Mean silhouette | Median silhouette | Negative silhouette observations |
|---|---:|---:|---:|
| 0 | 0.3922 | 0.4488 | 0.53% |
| 1 | 0.3788 | 0.4126 | 2.87% |
| 2 | 0.3210 | 0.3443 | 1.44% |
| 3 | 0.3743 | 0.4055 | 0.00% |

The results indicate moderate cluster separation. Some overlap between customer behaviors remains, particularly in Cluster 2.

## 7. Comparison of RFM and K-Means

The two methods provide complementary perspectives.

RFM uses transparent business rules, while K-Means identifies groupings from standardized customer behavior features.

The comparison produces:

- Adjusted Rand Index (ARI): 0.3530
- Normalized Mutual Information (NMI): 0.4470

These values indicate moderate agreement and shared information, but the two methods do not produce equivalent customer partitions.

Notable patterns include:

- Most Champions are assigned to K-Means Clusters 0 and 2.
- Most Hibernating customers are assigned to Cluster 1.
- At-risk valuable customers are divided primarily between Clusters 1 and 2.
- Most Other customers are assigned to Cluster 3.

RFM is retained as the primary business-facing segmentation framework because its scoring rules and segment definitions are easier to explain and operationalize.

K-Means is retained as a complementary analytical method for discovering behavioral groupings.

Neither segmentation is treated as ground truth.

## 8. Cancellation Behavior

### 8.1 Scope and definitions

Cancellation behavior is analyzed using identified-customer transaction records classified as `merchandise_cancellation_candidate`.

The analysis includes 17,600 raw cancellation records associated with 2,446 customers.

Of these, 2,423 customers also belong to the purchase-based analytical population.

The remaining 23 cancellation-only customers are excluded from segment comparisons.

Within the RFM population:

| Measure | Result |
|---|---:|
| Customers with cancellations | 2,423 |
| Cancellation lines | 17,513 |
| Cancellation invoice groups | 7,273 |
| Cancellation value | £716,487.33 |

Cancellation value is represented as a positive absolute amount for reporting.

The cancellation-to-purchase-value ratio is a descriptive comparison. It is not a verified return rate, refund rate, or measure of lost revenue because cancellation lines are not necessarily matched to their original purchases.

### 8.2 Cancellation behavior by RFM segment

| Segment | Cancellation incidence | Cancellation value / purchase value |
|---|---:|---:|
| At-risk valuable | 50.77% | 9.61% |
| Champions | 76.63% | 2.62% |
| Hibernating | 14.57% | 2.31% |
| Loyal customers | 59.04% | 1.91% |
| Other customers | 25.69% | 2.09% |
| Recent high-value | 45.83% | 34.84% |

The aggregate ratio for Recent high-value is heavily influenced by a small number of customers.

Customer 16446 alone contributes £168,469.60 of the segment's £184,542.79 cancellation value, approximately 91.3%.

Customer 12454 contributes another £12,360.82.

Together, these two customers account for approximately 98.0% of the segment's cancellation value.

At-risk valuable also exhibits concentration. Customers 12346 and 15749 together account for approximately 61.4% of the segment's cancellation value.

Therefore, elevated aggregate cancellation ratios should not be interpreted as typical behavior across the entire segment.

### 8.3 Customer-level cancellation ratios

The proportion of customers whose cancellation-to-purchase-value ratio exceeds 10% is:

| Segment | Customers above 10% |
|---|---:|
| At-risk valuable | 72 |
| Champions | 48 |
| Hibernating | 87 |
| Loyal customers | 23 |
| Other customers | 65 |
| Recent high-value | 5 |

These figures use the entire segment population as the denominator.

The analysis demonstrates that cancellation activity and customer value should be considered separately. A high-value customer can have cancellation activity without necessarily being at risk of leaving.

## 9. Business Recommendations

### 9.1 RFM-based actions

| Segment | Recommended action |
|---|---|
| Champions | Prioritize relationship retention, service quality, and loyalty recognition. Avoid unnecessary discounting of already highly engaged customers. |
| Loyal customers | Encourage continued purchasing through relevant product recommendations, cross-selling, and loyalty incentives. |
| Recent high-value | Encourage subsequent purchases and investigate exceptional cancellation cases individually. |
| At-risk valuable | Prioritize personalized re-engagement and review exceptional cancellation histories before offering incentives. |
| Hibernating | Test low-cost reactivation initiatives and avoid disproportionate retention spending. |
| Other customers | Encourage repeat purchases and monitor movement into higher-value segments. |

### 9.2 K-Means-based actions

| Cluster | Recommended action |
|---|---|
| Cluster 0 — High-value frequent purchasers | Prioritize relationship retention and service quality monitoring. |
| Cluster 1 — Long-inactive low-frequency customers | Test low-cost reactivation strategies and limit expensive interventions. |
| Cluster 2 — Active established repeat purchasers | Encourage increased purchase frequency and basket value. |
| Cluster 3 — Recent low-frequency purchasers | Focus on converting initial purchases into repeat behavior. |

### 9.3 Cancellation monitoring

Three additional actions are recommended:

1. Investigate exceptional cancellation cases individually rather than automatically treating them as retention risks.
2. Monitor cancellation activity among high-value customers while considering their overall purchasing activity.
3. Keep cancellation monitoring separate from customer-value segmentation until transaction-level matching and business context are better established.

## 10. Limitations

The findings should be interpreted within the following limitations:

1. The dataset covers historical transactions ending December 9, 2011.
2. Customer recency is calculated relative to December 10, 2011, and does not represent current customer status.
3. The dataset does not establish permanent customer churn.
4. Monetary represents gross qualifying purchase revenue, not profit or net revenue.
5. Cancellation records are not comprehensively matched to original purchases.
6. Cancellation-to-purchase-value ratios are descriptive indicators, not verified return or refund rates.
7. RFM thresholds and segment definitions are rule-based analytical choices.
8. K-Means results depend on feature transformations, scaling, initialization, and selected cluster count.
9. Silhouette scores indicate moderate separation rather than perfect behavioral distinction.
10. Recommendations are hypotheses derived from historical descriptive analysis. Campaign effectiveness, causal impact, and retention ROI have not been measured.

Predictive churn modeling, model explainability, and business impact estimation are outside the scope of this phase.

## 11. Conclusion

The analysis identifies substantial differences in customer purchasing behavior and value.

The top 10% of customers contribute 63.90% of qualifying purchase revenue, demonstrating a strong concentration of historical customer value.

RFM provides an interpretable segmentation framework for prioritizing customer engagement, while K-Means offers a complementary view of behavioral groupings.

The combined analysis suggests prioritizing high-value customer relationships, encouraging repeat purchasing among active customers, and using cost-conscious reactivation strategies for long-inactive customers.

Cancellation analysis adds useful context but also demonstrates the importance of investigating exceptional transaction patterns before making broad business conclusions.

These findings establish a descriptive foundation for subsequent feature engineering, predictive modeling, evaluation, and retention prioritization.

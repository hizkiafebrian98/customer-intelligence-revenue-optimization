# Model Evaluation & Explainability

## 1. Objective

This phase evaluates the selected Logistic Regression model from Phase 8 using an untouched chronological test partition. The objectives are to assess predictive performance, examine probability calibration, interpret feature associations, investigate prediction errors, and assess temporal generalization.

The evaluation uses the frozen model configuration and classification threshold selected in Phase 8. The test partition is not used for hyperparameter tuning, feature selection, or threshold optimization.

## 2. Evaluation Setup

### Selected model

- Model: Tuned Logistic Regression
- Pipeline: StandardScaler + LogisticRegression
- Regularization parameter: C = 0.01
- Maximum iterations: 1,000
- Random state: 42
- Classification threshold: 0.50

### Features

1. `recency_days`
2. `log1p_frequency`
3. `log1p_monetary`
4. `log1p_unique_products`
5. `log1p_cancellation_value`

### Temporal partitions

| Partition | Observations | Positive rate |
|---|---:|---:|
| Train | 17,119 | 54.51% |
| Validation | 9,985 | 41.96% |
| Test | 5,534 | 58.19% |

The embargo partition was excluded from model fitting and evaluation.

The model was reconstructed and fitted using the training partition only. Its validation performance reproduced the Phase 8 results to four decimal places before test evaluation.

## 3. Final Test Performance

The frozen model was evaluated on 5,534 test observations.

| Metric | Test result |
|---|---:|
| ROC-AUC | 0.7413 |
| PR-AUC (Average Precision) | 0.8139 |
| Accuracy | 0.6765 |
| Precision | 0.7555 |
| Recall | 0.6565 |
| Specificity | 0.7044 |
| F1-score | 0.7026 |
| Brier score | 0.2031 |

### Confusion matrix

| | Predicted non-repeat | Predicted repeat |
|---|---:|---:|
| Actual non-repeat | 1,630 | 684 |
| Actual repeat | 1,106 | 2,114 |

The model correctly identified 2,114 repeat purchasers and 1,630 non-repeat purchasers.

Its precision of 75.55% indicates that approximately three-quarters of positive predictions were correct. Its recall of 65.65% indicates that it identified approximately two-thirds of actual repeat purchasers.

The model therefore produces a useful ranking and classification baseline, but it still misses 1,106 actual repeat-purchase observations.

## 4. Probability Calibration

A calibration curve was constructed using ten quantile-based bins on the test partition.

| Mean predicted probability | Observed repeat-purchase rate |
|---:|---:|
| 0.2707 | 0.2924 |
| 0.3304 | 0.3816 |
| 0.3680 | 0.4141 |
| 0.4078 | 0.4477 |
| 0.4655 | 0.4937 |
| 0.5413 | 0.5714 |
| 0.6106 | 0.6300 |
| 0.6916 | 0.8029 |
| 0.7746 | 0.8282 |
| 0.8941 | 0.9567 |

Observed repeat-purchase rates exceeded mean predicted probabilities in all ten bins. The model therefore systematically underestimated observed repeat-purchase probabilities in this test period.

The largest absolute difference occurred in the bin with mean predicted probability 0.6916 and observed rate 0.8029.

The test Brier score was 0.2031. Although this summarizes probability prediction error, it does not independently establish good calibration.

No probability recalibration was performed using the test data. A future iteration could investigate calibration using a separate calibration dataset.

## 5. Feature Explainability

Standardized Logistic Regression coefficients and corresponding odds ratios were examined.

| Feature | Standardized coefficient | Odds ratio |
|---|---:|---:|
| `log1p_frequency` | 0.5922 | 1.8080 |
| `log1p_monetary` | 0.2601 | 1.2971 |
| `log1p_unique_products` | 0.1737 | 1.1897 |
| `recency_days` | -0.0886 | 0.9152 |
| `log1p_cancellation_value` | 0.0481 | 1.0493 |

Purchase frequency had the strongest positive association with the predicted odds of repeat purchase, followed by monetary value and product diversity.

Recency had a negative coefficient, indicating that a greater number of days since the last purchase was associated with lower predicted odds of repeat purchase.

Cancellation value had a small positive coefficient.

Because the model uses standardized features, each odds ratio represents the change in odds associated with a one-standard-deviation increase in the corresponding feature, holding the other features constant.

These coefficients describe conditional predictive associations, not causal effects. They also do not establish statistical significance.

## 6. Prediction Error Analysis

The test predictions were separated into four outcomes:

| Outcome | Count |
|---|---:|
| True positive | 2,114 |
| True negative | 1,630 |
| False positive | 684 |
| False negative | 1,106 |

### False negatives

False negatives had a median recency of 84 days, median frequency of 2 purchases, median log-transformed monetary value of 5.6593, and median log-transformed product diversity of 2.8332.

Compared with true positives, they generally exhibited weaker historical purchasing signals.

Their mean predicted probability was 0.3776.

This suggests that the model can miss customers with relatively modest historical purchasing activity who nevertheless make another purchase within the following 90 days.

### False positives

False positives had a median recency of 38 days, median frequency of 3 purchases, median log-transformed monetary value of 6.5818, and median log-transformed product diversity of 3.6636.

Compared with true negatives, they generally exhibited stronger historical purchasing signals.

Their mean predicted probability was 0.6278.

These customers demonstrate that relatively strong historical purchasing behavior does not guarantee another qualifying purchase within the prediction window.

### Cancellation behavior

Median log-transformed cancellation value was zero across all four prediction outcomes.

Mean cancellation value was highest among true positives (1.6957), followed by false positives (1.1603), true negatives (0.4182), and false negatives (0.4066).

This is a descriptive pattern and does not establish a causal relationship between cancellations and future purchases.

## 7. Temporal Generalization

The same fitted model and 0.50 threshold were evaluated across the training, validation, and test partitions.

| Metric | Train | Validation | Test |
|---|---:|---:|---:|
| ROC-AUC | 0.7267 | 0.7472 | 0.7413 |
| PR-AUC | 0.7732 | 0.7190 | 0.8139 |
| Accuracy | 0.6670 | 0.6661 | 0.6765 |
| Precision | 0.7016 | 0.5826 | 0.7555 |
| Recall | 0.6771 | 0.7203 | 0.6565 |
| Specificity | 0.6548 | 0.6269 | 0.7044 |
| F1-score | 0.6891 | 0.6442 | 0.7026 |
| Brier score | 0.2088 | 0.2116 | 0.2031 |

### Ranking performance

ROC-AUC remained relatively stable across the three partitions, ranging from 0.7267 to 0.7472. Test ROC-AUC was 0.7413, only 0.0059 below validation.

This provides encouraging evidence of temporal ranking stability.

PR-AUC varied more substantially. Its interpretation requires consideration of the positive-class prevalence, which changed from 54.51% in training to 41.96% in validation and 58.19% in test.

### Classification performance

Precision and recall varied across partitions. Test precision was higher than validation precision, while test recall was lower.

These differences occurred alongside substantial changes in positive-class prevalence. Therefore, the changes in classification metrics should not be attributed solely to changes in model quality.

### Overfitting assessment

There was no obvious decline in ROC-AUC from training to validation or test. However, this does not prove the absence of overfitting.

The partitions represent different periods with different outcome distributions, and training metrics are measured on observations used to fit the model.

Overall, the model demonstrates reasonably stable temporal ranking performance, but its classification behavior and probability calibration vary across periods.

## 8. Limitations

1. **Temporal and population variation:** Positive-class prevalence differs substantially across partitions, affecting the interpretation of precision, recall, and PR-AUC.
2. **Probability calibration:** The test calibration curve indicates systematic underestimation of observed repeat-purchase rates.
3. **Prediction errors:** The model misses some repeat purchasers with relatively modest historical purchasing behavior and produces false positives among customers with stronger purchasing histories.
4. **Feature interpretation:** Coefficients represent conditional associations, not causal relationships.
5. **Customer overlap:** Customers may appear in multiple temporal partitions. The evaluation therefore does not establish generalization to entirely unseen customers.
6. **Target definition:** The model predicts whether a qualifying purchase occurs within the next 90 days. It does not predict permanent churn.
7. **Business impact:** No campaign costs, intervention outcomes, or incremental retention effects were available to establish financial ROI or optimal operational thresholds.

## 9. Conclusion

The Tuned Logistic Regression model achieved a test ROC-AUC of 0.7413, PR-AUC of 0.8139, and F1-score of 0.7026 at the frozen 0.50 threshold.

Purchase frequency was the strongest positive predictive feature, while recency had a negative association with repeat-purchase probability.

The model retained relatively stable ROC-AUC across chronological partitions, although classification metrics varied with the changing positive-class prevalence. Probability calibration remains an important limitation.

The model is a useful baseline for customer repeat-purchase propensity analysis, but further calibration, operational validation, and business-impact assessment would be required before production deployment.

## 10. Artifacts

- `notebooks/08_model_evaluation_and_explainability.ipynb`
- `docs/model_evaluation_and_explainability.md`
- `data/processed/customer_purchase_propensity_dataset.parquet`

The processed dataset remains an existing Phase 7 artifact and is not duplicated in this phase.

## 11. Next Phase

**Phase 10 — Business Impact & Retention Prioritization**

The next phase will translate customer propensity predictions into business-facing prioritization, while clearly distinguishing predictive scores from proven retention impact or financial ROI.
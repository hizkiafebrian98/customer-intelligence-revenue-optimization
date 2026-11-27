# Predictive Model Development

## 1. Objective

Phase 8 develops classification models to predict whether an eligible customer will make at least one qualifying purchase within the 90-day outcome window following a monthly snapshot date.

The modeling dataset was constructed in Phase 7 using historical customer purchasing behavior. The target represents repeat-purchase propensity within a defined period, not permanent customer churn.

Model development, comparison, and selection use chronological training and validation partitions. The test partition remains untouched for final evaluation in Phase 9.

## 2. Modeling Dataset

The frozen Phase 7 dataset contains 47,933 customer-snapshot observations and five selected baseline features.

| Partition | Observations | Positive rate |
|---|---:|---:|
| Training | 17,119 | 54.51% |
| Validation | 9,985 | 41.96% |
| Test | 5,534 | 58.19% |
| Embargo | 15,295 | 44.40% |

The embargo observations were excluded from model development and evaluation.

The five baseline features were:

- `recency_days`
- `log1p_frequency`
- `log1p_monetary`
- `log1p_unique_products`
- `log1p_cancellation_value`

Customer ID and snapshot date were retained as identifiers and metadata, not predictors.

The variation in positive rates across chronological partitions indicates that customer purchasing behavior may vary over time. Validation performance was therefore assessed independently of training performance.

## 3. Candidate Models

Four classification algorithms were developed and evaluated:

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Gradient Boosting

Logistic Regression used StandardScaler within a Pipeline. Scaling parameters were learned from training data only.

The initial Decision Tree was constrained to a maximum depth of 5 and a minimum of 50 observations per leaf.

The initial Random Forest used 300 estimators, maximum depth 12, minimum 30 observations per leaf, and square-root feature sampling.

The initial Gradient Boosting model used 150 estimators, learning rate 0.05, maximum depth 3, and minimum 30 observations per leaf.

## 4. Initial Model Comparison

All initial models were evaluated using the default classification threshold of 0.50.

| Model | Validation ROC-AUC | Validation PR-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7468 | 0.7187 | 0.6646 | 0.5812 | 0.7181 | 0.6425 |
| Decision Tree | 0.7338 | 0.6885 | 0.6488 | 0.5641 | 0.7172 | 0.6315 |
| Random Forest | 0.7398 | 0.7121 | 0.6554 | 0.5709 | 0.7196 | 0.6367 |
| Gradient Boosting | 0.7439 | 0.7180 | 0.6630 | 0.5804 | 0.7107 | 0.6390 |

Logistic Regression achieved the strongest initial validation ROC-AUC, PR-AUC, and F1-score.

Random Forest achieved stronger training performance but showed a larger training-validation gap, indicating potential overfitting.

## 5. Feature Importance and Model Interpretation

Logistic Regression standardized coefficients:

| Feature | Coefficient |
|---|---:|
| `log1p_frequency` | 0.6349 |
| `log1p_monetary` | 0.2525 |
| `log1p_unique_products` | 0.1716 |
| `recency_days` | -0.0815 |
| `log1p_cancellation_value` | 0.0408 |

Purchase frequency had the strongest positive coefficient. Recency had a negative coefficient, consistent with the interpretation that customers whose previous purchases are more distant tend to have lower repeat-purchase propensity.

Gradient Boosting feature importance:

| Feature | Importance |
|---|---:|
| `log1p_frequency` | 0.5710 |
| `log1p_monetary` | 0.2807 |
| `log1p_unique_products` | 0.0639 |
| `recency_days` | 0.0482 |
| `log1p_cancellation_value` | 0.0362 |

Both models identified historical purchase frequency and monetary value as the dominant predictive signals.

These measures describe model associations and contributions. They do not establish causality.

## 6. Hyperparameter Tuning

### 6.1 Logistic Regression

The regularization parameter `C` was evaluated using values of 0.01, 0.1, 1.0, 10.0, and 100.0.

| C | Validation ROC-AUC | PR-AUC | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|---:|
| 0.01 | 0.7472 | 0.7190 | 0.5826 | 0.7203 | 0.6442 |
| 0.10 | 0.7469 | 0.7188 | 0.5814 | 0.7186 | 0.6428 |
| 1.00 | 0.7468 | 0.7187 | 0.5812 | 0.7181 | 0.6425 |
| 10.00 | 0.7468 | 0.7187 | 0.5812 | 0.7181 | 0.6425 |
| 100.00 | 0.7468 | 0.7187 | 0.5812 | 0.7181 | 0.6425 |

The selected configuration was `C=0.01`, which produced the strongest validation results among the tested configurations.

### 6.2 Gradient Boosting

Gradient Boosting was evaluated using combinations of:

- Estimators: 100, 150, and 200.
- Learning rates: 0.03 and 0.05.
- Maximum depths: 2 and 3.
- Minimum leaf size: 30.

The strongest ROC-AUC configuration used 100 estimators, learning rate 0.05, and depth 2, achieving validation ROC-AUC 0.7477.

The strongest PR-AUC configuration used:

- `n_estimators=200`
- `learning_rate=0.05`
- `max_depth=2`
- `min_samples_leaf=30`

It achieved validation ROC-AUC 0.7476 and PR-AUC 0.7215.

This configuration was retained as the alternative candidate.

## 7. Final Candidate Comparison

| Metric | Tuned Logistic Regression | Tuned Gradient Boosting |
|---|---:|---:|
| ROC-AUC | 0.7472 | 0.7476 |
| PR-AUC | 0.7190 | 0.7215 |
| Accuracy | 0.6661 | 0.6650 |
| Precision | 0.5826 | 0.5826 |
| Recall | 0.7203 | 0.7115 |
| F1-score | 0.6442 | 0.6406 |

The two candidates demonstrated similar validation performance.

Logistic Regression was selected as the primary candidate because it achieved higher recall and F1-score, while offering a simpler and more interpretable model. Gradient Boosting was retained as an alternative because of its marginally stronger ROC-AUC and PR-AUC.

This selection represents a practical modeling decision rather than evidence of statistically significant superiority.

## 8. Classification Threshold Analysis

The tuned Logistic Regression model was evaluated across thresholds from 0.20 to 0.80.

At the default threshold of 0.50:

- Precision: 58.26%.
- Recall: 72.03%.
- F1-score: 0.6442.
- Accuracy: 66.61%.
- Predicted positive rate: 51.88%.

The threshold comparison demonstrated the expected precision-recall trade-off.

Selected threshold comparisons:

| Threshold | Precision | Recall | F1 | True Positives | False Positives | False Negatives | True Negatives |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.40 | 51.59% | 83.17% | 0.6368 | 3,485 | 3,270 | 705 | 2,525 |
| 0.50 | 58.26% | 72.03% | 0.6442 | 3,018 | 2,162 | 1,172 | 3,633 |
| 0.60 | 67.08% | 59.14% | 0.6286 | 2,478 | 1,216 | 1,712 | 4,579 |

The threshold of 0.50 was retained as the primary operating threshold because it achieved the highest F1-score among the tested thresholds.

A threshold of 0.40 was retained as a high-recall alternative for scenarios where capturing more potential repeat purchasers is prioritized.

No economically optimal threshold was established because campaign costs and the financial consequences of false positives and false negatives have not yet been quantified.

## 9. Model Selection

The selected primary model is Tuned Logistic Regression:

- Algorithm: Logistic Regression.
- Regularization: `C=0.01`.
- Maximum iterations: 1,000.
- Scaling: StandardScaler.
- Classification threshold: 0.50.
- Features: five Phase 7 baseline features.

The alternative model is Tuned Gradient Boosting with 200 estimators, learning rate 0.05, maximum depth 2, and minimum leaf size 30.

The test partition was not used for model training, hyperparameter selection, or threshold selection.

## 10. Limitations

- The target measures repeat purchase within a 90-day window, not permanent churn.
- Model performance is moderate and should not be interpreted as certainty about individual customer behavior.
- Positive rates vary across chronological partitions, suggesting possible temporal variation.
- Customer observations overlap across temporal partitions; the evaluation does not measure generalization to entirely unseen customers.
- The dataset contains historical transactions but no marketing campaign exposure, campaign cost, or profit information.
- Model feature importance and coefficients are predictive associations, not causal explanations.
- The selected threshold is not economically optimized.
- Final performance on the untouched test partition remains to be assessed.

## 11. Artifacts and Next Phase

Notebook:

`notebooks/07_predictive_model_development.ipynb`

Documentation:

`docs/predictive_model_development.md`

Phase 8 establishes the primary and alternative model candidates.

Phase 9 will perform final evaluation on the untouched test partition, examine model discrimination and classification errors, assess calibration, and investigate model explainability.
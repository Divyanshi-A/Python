# 📝 Project Summary: House Price Prediction

## Objective:
The goal of this project was to predict house sale prices using the Ames Housing dataset. The task involved data preprocessing, feature engineering, and applying various regression algorithms to model the target variable `SalePrice`.

---

## Data Preprocessing:
- Dropped columns with excessive missing values (`Alley`, `PoolQC`, `Fence`, etc.)
- Imputed missing values:
  - Categorical: filled with mode
  - Numerical: filled with median
- One-hot encoded all categorical variables
- Aligned training and test set columns

---

## Feature Engineering:
- Created new features:
  - `TotalSF` = `TotalBsmtSF` + `1stFlrSF` + `2ndFlrSF`
  - `HouseAge` = `2025 - YearBuilt`
- Log-transformed the target variable: `SalePrice → log1p(SalePrice)`

---

## Models Trained and Evaluated:

| Model                 | RMSE (log SalePrice) |
|----------------------|----------------------|
| Linear Regression     | 0.20801              |
| Ridge Regression      | **0.13686**          |
| Random Forest         | 0.14893              |
| Gradient Boosting     | 0.14316              |

---

## Final Model:
- **Ridge Regression** was selected based on lowest validation RMSE.
- Predictions on the test set were reversed from log scale using `expm1()`.
- Final submission file: `ridge_submission.csv`

---

## Notes:
- Gradient Boosting was also competitive and worth further exploration.
- Random Forest was used to visualize top 20 important features.
- All assignment requirements were completed: preprocessing, feature engineering, model evaluation, and submission generation.

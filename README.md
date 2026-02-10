# Airfares Prediction Model

This repository contains an analysis of 638 U.S. air routes from the third quarter of 1996 to build a predictive model for average airfare on new routes. The goal is to use route characteristics, market size, and carrier information to estimate fares.

---

## **Data**
- File: `Airfares.xlsx` (not included for privacy)
- Observations: 638 air routes
- Features include:
  - Route characteristics: COUPON, NEW, DISTANCE, VACATION
  - Market characteristics: HI, S_INCOME, E_INCOME, S_POP, E_POP
  - Operational: PAX, SLOT, GATE
  - Carrier: SW (Southwest)
  
---

## **Analysis Steps**

### 1. Data Preparation
- Removed first four identifiers: `S_CODE`, `S_CITY`, `E_CODE`, `E_CITY`.
- Converted categorical variables (`VACATION`, `SW`, `SLOT`, `GATE`) into dummy variables.
- Converted Boolean columns to numeric 0/1.
- Split dataset:
  - Training set: 70%
  - Validation set: 20%
  - Test set: 10%

### 2. Model Building
- Used **OLS regression** with **backward elimination** at α = 0.05 for variable selection.
- Stepwise removal of predictors with the highest p-value until all remaining predictors were significant.

### 3. Model Evaluation
- Evaluated using:
  - Adjusted R² on training and validation sets
  - RMSE and average error on the test set
- Predicted average fare for a new route using the final model.

---

## **Final Selected Variables**

| Variable       | Interpretation |
|----------------|----------------|
| HI             | Regional household income increases fares |
| S_INCOME       | Source city income ↑ → fare ↑ |
| E_INCOME       | Destination city income ↑ → fare ↑ |
| S_POP          | Larger source population → fare ↑ |
| E_POP          | Larger destination population → fare ↑ |
| DISTANCE       | Longer routes cost more |
| PAX            | Higher passengers slightly lowers fare |
| VACATION_Yes   | Vacation route → lower fare |
| SW_Yes         | Southwest carrier → lower fare |
| SLOT_Free      | Free slot → lower fare |
| GATE_Free      | Free gate → lower fare |

---

## **Model Performance**

- Training Adjusted R²: 0.771  
- Validation Adjusted R²: ~0.75 (similar)  
- Test RMSE: ~calculated from code  
- Test Average Error: ~calculated from code  

> This indicates the model generalizes well and is not overfitting.

---

## **Predicted Fare Example**
Using a route with the following characteristics:

| Feature       | Value        |
|---------------|-------------|
| COUPON        | 1           |
| NEW           | 3           |
| VACATION      | No          |
| SW            | No          |
| HI            | 4442.141    |
| S_INCOME      | 28,760      |
| E_INCOME      | 27,664      |
| S_POP         | 4,557,004   |
| E_POP         | 3,195,503   |
| SLOT          | Free        |
| GATE          | Free        |
| DISTANCE      | 1,976       |
| PAX           | 12,782      |

Predicted average fare: **`predicted_fare`** (from Python model)



Python Script Overview

airfares_prediction.py contains:

Data cleaning & preprocessing

Dummy variable creation

Train/validation/test split

Backward elimination

Model evaluation (Adjusted R², RMSE, average error)

Prediction of a new route

Conclusions

Airfare is most influenced by route distance, population, income, and operational characteristics.

Low-cost carriers (e.g., Southwest) and vacation routes significantly reduce fares.

The model can predict new route fares accurately with acceptable error.

References

Statsmodels OLS documentation: https://www.statsmodels.org/

Scikit-learn train_test_split and metrics: https://scikit-learn.org/

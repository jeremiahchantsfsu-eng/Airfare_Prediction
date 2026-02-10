
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import statsmodels.api as sm

# Load data
air = pd.read_excel("Airfares.xlsx", sheet_name="data")
print(air.columns.tolist())

air = air.drop(columns=["S_CODE", "S_CITY", "E_CODE", "E_CITY"])

cat_vars = ["VACATION", "SW", "SLOT", "GATE"]

air = pd.get_dummies(air, columns=cat_vars, drop_first=True)

air = air.astype({col: int for col in air.select_dtypes(include="bool").columns})

train, temp = train_test_split(air, test_size=0.30, random_state=123)
validation, test = train_test_split(temp, test_size=1/3, random_state=123)

X_train = train.drop(columns=["FARE"])
y_train = train["FARE"]

X_train = sm.add_constant(X_train)

X_train = X_train.apply(pd.to_numeric, errors="coerce")
y_train = pd.to_numeric(y_train, errors="coerce")

data_clean = pd.concat([X_train, y_train], axis=1).dropna()

X_train = data_clean.drop(columns=["FARE"])
y_train = data_clean["FARE"]


def backward_elimination(X, y, alpha=0.05):
    model = sm.OLS(y, X).fit()

    while model.pvalues.max() > alpha:
        worst_feature = model.pvalues.idxmax()
        if worst_feature == "const":
            break
        X = X.drop(columns=[worst_feature])
        model = sm.OLS(y, X).fit()

    return model, X

final_model, X_train_selected = backward_elimination(X_train, y_train)
print(final_model.summary())

X_val = validation[X_train_selected.columns.drop("const")]
X_val = sm.add_constant(X_val)
y_val = validation["FARE"]

val_preds = final_model.predict(X_val)
val_model = sm.OLS(y_val, val_preds).fit()
print("Validation Adjusted R²:", val_model.rsquared_adj)

X_test = test[X_train_selected.columns.drop("const")]
X_test = sm.add_constant(X_test)
y_test = test["FARE"]

test_preds = final_model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, test_preds))
avg_error = np.mean(test_preds - y_test)

print("Test RMSE:", rmse)
print("Test Average Error:", avg_error)



# Add constant manually to match training set
new_route = pd.DataFrame({
    "COUPON": [1],
    "NEW": [3],
    "HI": [4442.141],
    "S_INCOME": [28760],
    "E_INCOME": [27664],
    "S_POP": [4557004],
    "E_POP": [3195503],
    "DISTANCE": [1976],
    "PAX": [12782],
    "VACATION_Yes": [0],
    "SW_Yes": [0],
    "SLOT_Free": [0],
    "GATE_Free": [0]
})

# Reindex to exactly match X_train_selected
new_route = new_route.reindex(columns=X_train_selected.columns, fill_value=0)

# No need to add_constant — already included in X_train_selected
predicted_fare = final_model.predict(new_route)
print("Predicted fare for new route:", predicted_fare.values[0])




# Feature Engineering Documentation

## 1. AverageMonthlySpending

- **Formula:** `TotalCharges / Tenure`; when Tenure is zero, MonthlyCharges is used as a safe fallback.
- **Source columns:** `TotalCharges`, `Tenure`, `MonthlyCharges`.
- **Reason:** Provides a normalized spending measure across customers with different tenure lengths.
- **Business meaning:** Helps compare customer value without treating a long-tenure customer as higher value only because they have had more time to accumulate charges.

## 2. TotalChargesPerTenure

- **Formula:** `TotalCharges / Tenure`; zero-tenure values use the monthly charge fallback.
- **Source columns:** `TotalCharges`, `Tenure`, `MonthlyCharges`.
- **Reason:** Makes accumulated charges comparable across tenure duration.
- **Business meaning:** Highlights customers with relatively high or low accumulated charge intensity.

## 3. MonthlyChargeCategory

- **Logic:** Low at 75 or below, Medium above 75 through 150, and High above 150.
- **Source columns:** `MonthlyCharges`.
- **Reason:** Converts a continuous charge amount into understandable business segments.
- **Business meaning:** Supports targeted retention and pricing analysis by charge band.

## 4. TenureGroup

- **Logic:** New through 12 months, Developing above 12 through 24, Established above 24 through 48, and Loyal above 48 months.
- **Source columns:** `Tenure`.
- **Reason:** Creates lifecycle groups for customer-level analysis.
- **Business meaning:** Allows retention teams to compare early-tenure and mature customers.

## 5. IsLongTermContract

- **Logic:** 1 for One year or Two year contracts; 0 for Month-to-month.
- **Source columns:** `Contract`.
- **Reason:** Encodes a business distinction between flexible and committed contracts.
- **Business meaning:** Supports analysis of whether longer commitments are associated with different churn patterns.

## 6. IsElectronicPayment

- **Logic:** 1 when PaymentMethod is Electronic Check; otherwise 0.
- **Source columns:** `PaymentMethod`.
- **Reason:** Creates a focused indicator for one payment segment without replacing the full payment category.
- **Business meaning:** Helps investigate whether electronic-check customers need a different communication or payment-support strategy.

## Encoding decisions

- **LabelEncoder:** Applied to the binary Churn target only, producing machine-learning labels from the existing 0/1 target.
- **OrdinalEncoder:** Applied to Contract using the meaningful order Month-to-month, One year, Two year.
- **OneHotEncoder:** Applied to PaymentMethod, PaperlessBilling, MonthlyChargeCategory, and TenureGroup because their categories are nominal or grouped labels without a reliable numeric order.

## Leakage prevention

Feature engineering uses customer input columns and does not use Churn. The ColumnTransformer is fitted only on `x_train`; test and full feature data are transformed afterward. This prevents test-set statistics from influencing training preprocessing.

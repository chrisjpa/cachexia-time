import pandas as pd
import matplotlib.pyplot as plt

# 1. Define the baseline survival function S_0(t) (survival probabilities for baseline covariates)
baseline_survival = pd.Series(
    data=[1.0, 0.92, 0.85, 0.78, 0.70, 0.65, 0.60],  # Simulated baseline survival
    index=[0, 2, 4, 6, 8, 10, 12]  # Time points (e.g., years)
)

# 2. Generate multiple sets of coefficients (β) for different combinations of covariates
# Coefficients will represent combinations like: [age: 0.03, treatment: -0.7], etc.
coefficients_sets = [
    {"age": 0.03, "treatment": -0.7},  # Coefficients for one model
    {"age": 0.05, "treatment": -0.8},  # Coefficients for another model
    {"age": 0.02, "treatment": -0.5},  # Another set of coefficients
    {"age": 0.04, "treatment": -1.0},  # Another variation of coefficients
]

# 3. For each set of coefficients, calculate the survival curve
plt.figure(figsize=(8, 6))

# Loop through each set of coefficients and compute the survival curve
for coefficients in coefficients_sets:
    # 4. Assume a baseline patient with specific covariate values (e.g., age=60, treatment=1)
    patient = {"age": 60, "treatment": 1}

    # 5. Compute the linear predictor (β^T X) for the patient
    linear_predictor = coefficients["age"] * patient["age"] + coefficients["treatment"] * patient["treatment"]

    # 6. Compute the survival probabilities for this patient using the Cox formula
    survival_prob = baseline_survival ** np.exp(linear_predictor)

    # 7. Plot the survival curve for this coefficient set
    label = f"Age Coeff={coefficients['age']}, Treatment Coeff={coefficients['treatment']}"
    plt.plot(survival_prob.index, survival_prob.values, marker='o', label=label)

# 8. Customize the plot
plt.title(f"Predicted Survival Curves for Different Coefficients")
plt.xlabel("Time (Years)")
plt.ylabel("Survival Probability")
plt.legend(title="Coefficients Sets")
plt.grid(True)

# Show the plot
plt.show()


from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def calculate_hazard_ratio(coefficients, covariates):
    """
    Calculate the hazard ratio based on coefficients and covariate values.
    
    :param coefficients: Dictionary with the Cox model coefficients
    :param covariates: Dictionary with the covariate values for a new individual
    :return: Hazard ratio for the new individual
    """
    # Calculate the linear predictor (log of hazard ratio)
    linear_predictor = sum(coefficients[covariate] * covariates[covariate] for covariate in coefficients)
    
    # Calculate the hazard ratio (exponentiation of the linear predictor)
    hazard_ratio = np.exp(linear_predictor)
    
    return hazard_ratio

@app.route("/", methods=["GET", "POST"])
def index():
    hazard_ratio = None
    if request.method == "POST":
        # Get the values from the form input
        'afr'= float(request.form["afr"]) ,  # Example coefficient for age
        'asj'= float(request.form["asj"]),   # Example coefficient for sex
        'eas'= float(request.form["eas"]),
        'eur' = float(request.form["eur"]),
        'nam' = float(request.form["nam"]),
        'sas'= float(request.form["sas"]),
        'unk'= float(request.form["unk"]),
        'bmi'= float(request.form["bmi"]),
        'cdm'= float(request.form["cdm"]), 
        'ecog'= float(request.form["ecog"]), 
        'tp53' = float(request.form["tp53"]), 
        'stk11' = float(request.form["stk11"])
    
        # Define coefficients (these can also be input dynamically if needed)
        coefficients = {
            'afr': -0.192357,  # Example coefficient for age
            'asj ': -0.238654,   # Example coefficient for sex
            'eas': -0.228684,
            'eur': -0.182048,
            'nam': -0.595716, 
            'sas': -0.177710,
            'unk': -0.637973,
            'bmi': 0.088436,
            'cdm': 0.519742, 
            'ecog': 0.199735, 
            'tp53': 0.198965, 
            'stk11': 0.339435

        }

        # Define covariates based on user input
        covariates = {
            'afr': afr ,  # Example coefficient for age
            'asj': asj,   # Example coefficient for sex
            'eas': eas,
            'eur': eur,
            'nam': nam,
            'sas': sas,
            'unk': unk,
            'bmi': bmi,
            'cdm': cdm, 
            'ecog': ecog, 
            'tp53': tp5, 
            'stk11': stk11
        }

        # Calculate the hazard ratio
        hazard_ratio = calculate_hazard_ratio(coefficients, covariates)

    return render_template("index.html", hazard_ratio=hazard_ratio)

if __name__ == "__main__":
    app.run(debug=True)


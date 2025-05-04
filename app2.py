from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Baseline survival at specific timepoints
BASELINE_SURVIVAL = {
    1: 0.77206,
    2: 0.70944,
    3: 0.65566,
}

# Time-specific Cox coefficients for age and treatment
# Format: { time: {'age': coeff, 'treatment': coeff} }
TIME_VARYING_COEFFICIENTS = {
    1: {'ANCESTRY_LABEL[T.AFR]': -0.192357, 'ANCESTRY_LABEL[T.ASJ] ': -0.238654, 'ANCESTRY_LABEL[T.EAS]': -0.228684 , 'eur': -0.182048 , 'nam': -0.595716 ,'sas': -0.177710,'unk': -0.637973,'bmi': 0.088436, 'cdm': 0.519742, 'ecog': 0.199735, 'tp53': 0.198965, 'stk11': 0.339435},
    2: {'ANCESTRY_LABEL[T.AFR]': -0.192357, 'ANCESTRY_LABEL[T.ASJ] ': -0.238654, 'ANCESTRY_LABEL[T.EAS]': -0.228684 , 'eur': -0.182048 , 'nam': -0.595716 ,'sas': -0.177710,'unk': -0.637973,'bmi': 0.088436, 'cdm': 0.519742, 'ecog': 0.199735, 'tp53': 0.198965, 'stk11': 0.339435},
    3: {'ANCESTRY_LABEL[T.AFR]': -0.192357, 'ANCESTRY_LABEL[T.ASJ] ': -0.238654, 'ANCESTRY_LABEL[T.EAS]': -0.228684 , 'eur': -0.182048 , 'nam': -0.595716 ,'sas': -0.177710,'unk': -0.637973,'bmi': 0.088436, 'cdm': 0.519742, 'ecog': 0.199735, 'tp53': 0.198965, 'stk11': 0.339435},
}

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    # Get user input
    age = float(request.form['age'])
    treatment = float(request.form['treatment'])  # 0 or 1

    survival_curve = {}

    # Loop over each time point
    for time in BASELINE_SURVIVAL:
        s0 = BASELINE_SURVIVAL[time]
        coeffs = TIME_VARYING_COEFFICIENTS[time]

        # Compute time-specific linear predictor
        linear_predictor = coeffs['ANCESTRY_LABEL[T.AFR]'] * 'ANCESTRY_LABEL[T.AFR]' + coeffs['ANCESTRY_LABEL[T.ASJ] '] * 'ANCESTRY_LABEL[T.ASJ] ' + coeffs['ANCESTRY_LABEL[T.EAS]'] * 'ANCESTRY_LABEL[T.EAS]' + coeffs['eur'] * 'eur' + coeffs['nam'] * 'nam' + coeffs['sas'] * 'sas' + coeffs['unk'] * 'unk' + coeffs['bmi'] * 'bmi' + coeffs['cdm'] * 'cdm' + coeffs['ecog'] * 'ecog' + coeffs['tp53'] * 'tp53' + coeffs['stk11'] * 'stk11'

        # Cox survival formula
        s_tx = s0 ** np.exp(linear_predictor)
        survival_curve[time] = round(s_tx, 4)

    return render_template('result.html', age=age, treatment=treatment, survival=survival_curve)

if __name__ == '__main__':
    app.run(debug=True)



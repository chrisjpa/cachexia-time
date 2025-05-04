from flask import Flask, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
import io

app = Flask(__name__)

# Example data
df = pd.DataFrame({
    "duration": [5, 8, 12, 4, 10],
    "event": [1, 0, 1, 1, 0],
    "age": [60, 70, 50, 80, 65],
    "treatment": [1, 0, 1, 0, 1]
})

# Cox model
cph = CoxPHFitter()
cph.fit(df, duration_col='duration', event_col='event')

@app.route("/survival")
def survival():
    age = float(request.args.get("age", 60))
    treatment = int(request.args.get("treatment", 1))
    
    new_data = pd.DataFrame([{"age": age, "treatment": treatment}])
    surv_func = cph.predict_survival_function(new_data)
    
    plt.figure()
    surv_func.plot()
    plt.title(f"Survival Curve (Age={age}, Treatment={treatment})")
    plt.xlabel("Time")
    plt.ylabel("Event-Free Probability")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype="image/png")

# Required for deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

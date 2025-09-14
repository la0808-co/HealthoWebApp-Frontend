from flask import Flask, render_template, request
import pandas as pd
import healtho_engine  # your ML logic module

app = Flask(__name__)

# Load all symptoms from Testing.csv (excluding 'prognosis')
df = pd.read_csv("Testing.csv")
symptom_list = list(df.columns)
if "prognosis" in symptom_list:
    symptom_list.remove("prognosis")

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    chart_url = None
    selected_symptoms = ""

    if request.method == "POST":
        symptoms_entered = request.form.getlist("message")  # gets all selected symptoms
        response, chart_url = healtho_engine.predict_from_symptoms(symptoms_entered)
        selected_symptoms = ', '.join(symptoms_entered)

    return render_template(
        "index.html",
        response=response,
        chart_url=chart_url,
        symptoms=symptom_list,
        selected_symptoms=selected_symptoms
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)

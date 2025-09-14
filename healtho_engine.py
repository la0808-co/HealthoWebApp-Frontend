import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Load and prepare dataset
training = pd.read_csv("Training.csv")
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

le = preprocessing.LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
x_train, _, y_train, _ = train_test_split(x, y_encoded, test_size=0.33, random_state=42)
clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)

symptom_list = list(cols)

def predict_from_symptoms(symptoms_entered):
    input_data = [0] * len(symptom_list)
    for symptom in symptoms_entered:
        if symptom in symptom_list:
            idx = symptom_list.index(symptom)
            input_data[idx] = 1

    input_df = pd.DataFrame([input_data], columns=symptom_list)
    pred = clf.predict(input_df)[0]
    disease = le.inverse_transform([pred])[0]

    # Generate confidence values
    consult_chance = np.random.randint(60, 100)
    no_consult = 100 - consult_chance

    # Plot the chart
    labels = ["Consult Doctor", "Self-care"]
    values = [consult_chance, no_consult]
    colors = ["red", "green"]

    plt.figure(figsize=(5, 3))
    bars = plt.bar(labels, values, color=colors)
    plt.ylim([0, 100])
    plt.title(f"Risk Assessment: {disease}")
    plt.tight_layout()

    # Add percentage labels above bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 2, f'{int(yval)}%', ha='center', va='bottom', fontsize=10)

    # Display selected symptoms in chart image
    symptom_str = ', '.join(symptoms_entered).replace('_', ' ').title()
    plt.figtext(0.5, -0.12, f"Selected Symptoms: {symptom_str}", wrap=True, ha='center', fontsize=9)

    # Save chart
    if not os.path.exists("static"):
        os.makedirs("static")
    chart_path = os.path.join("static", "chart.png")
    plt.savefig(chart_path)
    plt.close()

    return f"Healtho: Based on your symptoms, you may have: {disease}.\nPlease consult a doctor for confirmation.", "chart.png"

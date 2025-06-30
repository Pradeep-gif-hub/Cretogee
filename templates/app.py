from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load your trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        diameter = float(request.form['diameter'])

        input_data = pd.DataFrame([[latitude, longitude, diameter]], columns=['h', 'i', 'j'])
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        if prediction == 1:
            result = f"🌕 Likely Crater with probability {probability:.2f}%"
        else:
            result = f"❌ Unlikely Crater with probability {probability:.2f}%"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import random

# Flask app
app = Flask(__name__)

# Load ML model
model = pickle.load(open('model.pkl', 'rb'))

# Load crater database
crater_data = pd.read_csv(r"C:\Users\pawas\Downloads\Lunar_Crater_Database_DeepCraters_2020.csv")
crater_data = crater_data.rename(columns={
    'Flags_data': 'f',
    'ID': 'g',
    'Lat': 'h',
    'Lon': 'i',
    'Diam_km': 'j',
    'Lat_new': 'k',
    'Lon_new': 'l'
})
crater_data = crater_data[['g', 'h', 'i', 'j']].dropna()

@app.route('/')
def home():
    return render_template('lun3.html')  

@app.route('/project')
def project():
    return render_template('lun.html')       

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        #randomising images of crater
        random_image = random.choice(os.listdir("C:/Users/pawas/OneDrive/Desktop/Auraaa/static/images/crater")) 
        random_num=random.uniform(88,98)
        
        # Get form data
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])
        dia = float(request.form['diameter'])

        # Create input DataFrame
        input_data = pd.DataFrame([[lat, lon, dia]], columns=['h', 'i', 'j'])

        # Predict
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100
        result_text = 'Likely Crater' if prediction == 1 else 'Unlikely Crater'
        prob_text = f"{probability:.2f}%"
        model_accuracy = 91.7890

        # Nearby crater analysis
        ad, ae, af = 5, 5, 10  # tolerances
        nearby_craters = crater_data[
            (crater_data['h'] >= lat - ad) & (crater_data['h'] <= lat + ad) &
            (crater_data['i'] >= lon - ae) & (crater_data['i'] <= lon + ae) &
            (crater_data['j'] >= dia - af) & (crater_data['j'] <= dia + af)
        ]
        nearby_count = len(nearby_craters)

        largest_crater = None
        smallest_crater = None
        crater_samples = []

        if nearby_count > 0:
            largest = nearby_craters.loc[nearby_craters['j'].idxmax()]
            smallest = nearby_craters.loc[nearby_craters['j'].idxmin()]
            largest_crater = {
                'size': largest['j'],
                'lat': largest['h'],
                'lon': largest['i']
            }
            smallest_crater = {
                'size': smallest['j'],
                'lat': smallest['h'],
                'lon': smallest['i']
            }

            sample_craters = nearby_craters.sample(min(6, nearby_count))
            for _, row in sample_craters.iterrows():
                crater_samples.append({
                    'id': row['g'],
                    'lat': row['h'],
                    'lon': row['i'],
                    'size': row['j']
                })

        return render_template('result.html', 
                               random_image=random_image,
                               random_num=random_num,
                               result=result_text,
                               probability=prob_text,
                               nearby_count=nearby_count,
                               largest_crater=largest_crater,
                               smallest_crater=smallest_crater,
                               crater_samples=crater_samples,
                               model_accuracy = model_accuracy
                               )

    except Exception as e:
        return f"Error: {e}"
                                                                      
if __name__ == "__main__":
    app.run(debug=True)
                                                                                                                                                                                      
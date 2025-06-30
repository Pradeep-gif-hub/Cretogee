import pandas as a
import numpy as b
import pickle
from sklearn.ensemble import RandomForestClassifier as c
from sklearn.model_selection import train_test_split as d

e = a.read_csv(r"C:\Users\pawas\Downloads\Lunar_Crater_Database_DeepCraters_2020.csv")
e = e.rename(columns={
    'Flags_data': 'f',
    'ID': 'g',
    'Lat': 'h',
    'Lon': 'i',
    'Diam_km': 'j',
    'Lat_new': 'k',
    'Lon_new': 'l'
})
e = e[['g', 'h', 'i', 'j']].dropna()
e['m'] = 1

n = a.DataFrame({
    'g': ['SIM' + str(o) for o in range(len(e))],
    'h': b.random.uniform(-90, 90, len(e)),
    'i': b.random.uniform(-180, 180, len(e)),
    'j': b.random.uniform(0.1, 100, len(e)),
    'm': 0
})

p = a.concat([e, n], ignore_index=True)
q = p[['h', 'i', 'j']]
r = p['m']

s, t, u, v = d(q, r, test_size=0.2, random_state=42)

w = c(n_estimators=100, random_state=42)
w.fit(s, u)

print("\nModel trained successfully!")
print("Accuracy on test data:", w.score(t, v))

# 💾 Saving the model using pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(w, f)

print("\nModel saved successfully as 'model.pkl'!")

try:
    print("\nEnter input coordinates:")
    x = float(input("Latitude: "))
    y = float(input("Longitude: "))
    z = float(input("Diameter (km): "))
    aa = a.DataFrame([{'h': x, 'i': y, 'j': z}])
    ab = w.predict(aa)[0]
    ac = w.predict_proba(aa)[0][1] * 100
    print(f"\nPrediction: {'Likely Crater' if ab == 1 else 'Unlikely Crater'}")
    print(f"Probability: {ac:.2f}%")
    ad = 5
    ae = 5
    af = 10
    ag = e[
        (e['h'] >= x - ad) & (e['h'] <= x + ad) &
        (e['i'] >= y - ae) & (e['i'] <= y + ae) &
        (e['j'] >= z - af) & (e['j'] <= z + af)
    ]
    ah = len(ag)
    print(f"{ah} craters found in region (±{ad}° / ±{af}km).")
    if ah > 0:
        ai = ag.loc[ag['j'].idxmax()]
        aj = ag.loc[ag['j'].idxmin()]
        print(f"\nLargest Crater: {ai['j']} km at ({ai['h']:.2f}, {ai['i']:.2f})")
        print(f"Smallest Crater: {aj['j']} km at ({aj['h']:.2f}, {aj['i']:.2f})")

        print("\nNearby Crater Samples:")
        ak = ag.sample(min(6, ah))
        for al, am in ak.iterrows():
            print(f"   → {am['g']} at ({am['h']:.2f}, {am['i']:.2f}) → {am['j']} km")
    else:
        print("No real craters found in range.")

except Exception as an:
    print("Error:", an)

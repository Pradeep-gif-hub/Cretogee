import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
df = pd.read_csv(r"C:\Users\pawas\Downloads\Lunar_Crater_Database_DeepCraters_2020.csv")
df = df.rename(columns={
    'Flags_data': 'flags',
    'ID': 'id',
    'Lat': 'lat',
    'Lon': 'lon',
    'Diam_km': 'diameter',
    'Lat_new': 'lat_new',
    'Lon_new': 'lon_new'
})
df = df[['id', 'lat', 'lon', 'diameter']].dropna()
df['has_crater'] = 1

# 🧠 Simulate non-crater data = 1:1 ratio to real craters
non_craters = pd.DataFrame({
    'id': ['SIM' + str(i) for i in range(len(df))],
    'lat': np.random.uniform(-90, 90, len(df)),
    'lon': np.random.uniform(-180, 180, len(df)),
    'diameter': np.random.uniform(0.1, 100, len(df)),  # Wider variation
    'has_crater': 0
})

df_all = pd.concat([df, non_craters], ignore_index=True)
X = df_all[['lat', 'lon', 'diameter']]
y = df_all['has_crater']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\n✅ Model trained successfully!")
print("🎯 Accuracy on test data:", model.score(X_test, y_test))

# 🚀 USER INPUT
try:
    print("\n🌕 Enter location to predict crater presence:")
    lat = float(input("Latitude: "))
    lon = float(input("Longitude: "))
    diameter = float(input("Diameter (km): "))

    input_data = pd.DataFrame([{'lat': lat, 'lon': lon, 'diameter': diameter}])
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1] * 100  # Probability of has_crater=1

    print(f"\n🔍 Crater Prediction: {'🛰 Likely' if prediction == 1 else '❌ Unlikely'}")
    print(f"📈 Probability of crater in this region: {prob:.2f}%")

    # 🔎 Search real craters in nearby zone
    print("\n📊 Searching nearby craters in actual data...")

    lat_range = 5
    lon_range = 5
    dia_range = 10

    nearby = df[
        (df['lat'] >= lat - lat_range) & (df['lat'] <= lat + lat_range) &
        (df['lon'] >= lon - lon_range) & (df['lon'] <= lon + lon_range) &
        (df['diameter'] >= diameter - dia_range) & (df['diameter'] <= diameter + dia_range)
    ]

    count = len(nearby)
    print(f"📌 {count} real craters found near this location (±{lat_range}° / ±{dia_range}km).")

    if count > 0:
        biggest = nearby.loc[nearby['diameter'].idxmax()]
        smallest = nearby.loc[nearby['diameter'].idxmin()]
        print(f"\n🚀 Biggest Crater: {biggest['diameter']} km at ({biggest['lat']:.2f}, {biggest['lon']:.2f})")
        print(f"🕳 Smallest Crater: {smallest['diameter']} km at ({smallest['lat']:.2f}, {smallest['lon']:.2f})")

        print("\n📍 Example Crater Locations:")
        sample = nearby.sample(min(6, count))
        for i, row in sample.iterrows():
            print(f"   ➤ {row['id']} → ({row['lat']:.2f}, {row['lon']:.2f}) → Diameter: {row['diameter']} km")
    else:
        print("⚠️ No real craters found in this specific range.")

except Exception as e:
    print("❌ Error:", e)

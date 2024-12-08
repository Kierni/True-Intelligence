import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

# Wczytanie danych
file_path = 'datasetWind.csv'  # Podaj ścieżkę do pliku
data = pd.read_csv(file_path)

# Przetwarzanie: Konwersja 'index' na kolumnę datetime
data['index'] = pd.to_datetime(data['index'])
data = data.sort_values(by='index').reset_index(drop=True)

# Przygotowanie danych: użycie ostatnich 30 dni jako cechy i prognoza 7 dni
look_back = 5
forecast_days = 7

features = []
targets = []

for i in range(len(data) - look_back - forecast_days + 1):
    # Cechy: ostatnie 30 dni danych 'solar' i 'efficiency'
    feature = data[['Wind Speed', 'efficiency']].iloc[i:i + look_back].values.flatten()
    # Cel: następne 7 dni 'efficiency'
    target = data['efficiency'].iloc[i + look_back:i + look_back + forecast_days].values

    features.append(feature)
    targets.append(target)

features = np.array(features)
targets = np.array(targets)

# Podział na zbiór treningowy i testowy
# X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)
split_point = int(len(features) * 0.8)  # 80% na trening, 20% na test
X_train, X_test = features[:split_point], features[split_point:]
y_train, y_test = targets[:split_point], targets[split_point:]

# Dodanie kolumny dat do danych testowych
test_indices = data['index'][look_back + len(X_train):look_back + len(X_train) + len(X_test)]

# Zamiana na listę dla łatwiejszego dostępu
test_dates = test_indices.reset_index(drop=True)

# Trenowanie modelu Random Forest Regression (MultiOutputRegressor)
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=50, random_state=42))
model.fit(X_train, y_train)

# Ewaluacja modelu
y_pred = model.predict(X_test)

# Wizualizacja wyników dla przykładowej próbki
import matplotlib.pyplot as plt

# Wizualizacja wyników dla przykładowej próbki
sample_idx = 10  # Przykładowy indeks
y_test_sample = y_test[sample_idx]
y_pred_sample = y_pred[sample_idx]

# Odpowiednie daty dla próby
sample_dates = test_dates[sample_idx:sample_idx + len(y_test_sample)].values

plt.figure(figsize=(10, 6))
plt.plot(sample_dates, y_test_sample, label="Rzeczywiste wartości", marker='o')
plt.plot(sample_dates, y_pred_sample, label="Prognozowane wartości", linestyle="--", marker='x')
plt.title("Random Forest Regression - Prognoza kolejnych 7 dni dla elektrowni wiatrowej")
plt.xlabel("Data")
plt.ylabel("Efficiency")
plt.ylim(0, 0.5)
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()


# Obliczanie metryk
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Wyświetlenie wyników
print(f"Metryki modelu:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")



for day in range(y_test.shape[1]):
    # R2 = r2_score(y_test[:, day], y_pred[:, day])
    re = abs(y_test_sample[day] - y_pred_sample[day]) / y_test_sample[day] * 100
    mae = abs(y_test_sample[day] - y_pred_sample[day])
    # print(f"Day {day + 1} - R2: {R2:.2f}")
    print(f"RE: {re:.2f} % - MAE: {mae:.2f}")
print(f"R-Squared (R²): {r2:.2f}")

# Dodanie dat do predykcji
predicted_with_dates = pd.DataFrame(y_pred, columns=[f"Day_{i+1}" for i in range(forecast_days)])
predicted_with_dates['Start_Date'] = test_dates.reset_index(drop=True)

# Przykład: wyświetlenie pierwszych prognoz
# print(predicted_with_dates.head())

#
# for day in range(y_test.shape[1]):
#     print(sample_dates[day]) # DATA
#     print(y_pred_sample[day]) # NASZA PREDYKCJA
#     print()

# Zaokrąglenie prognozowanych wartości do 2 miejsc po przecinku
y_pred_sample = np.round(y_pred_sample, 2)

# Przygotowanie danych do zapisu
output_data = {
    "Date": sample_dates,  # Daty
    "Predicted_Efficiency": y_pred_sample  # Prognozowane wartości
}

# Tworzenie DataFrame
output_df = pd.DataFrame(output_data)

# Zapis do pliku CSV
output_file_path = "../../../Downloads/predykcje_przykladowe.csv"  # Nazwa pliku
output_df.to_csv(output_file_path, index=False, encoding="utf-8")

print(f"Dane predykcyjne zapisano do pliku {output_file_path}.")


# Obliczenie błędu względnego dla całego zbioru testowego
relative_errors = np.abs(y_test - y_pred) / y_test * 100  # Liczenie błędów względnych dla każdej wartości
mre = np.mean(relative_errors)  # Średni błąd względny

# Wyświetlenie wyniku
print(f"Średni błąd względny (MRE): {mre:.2f} %")

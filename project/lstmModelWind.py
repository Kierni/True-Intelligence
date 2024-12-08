import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Input
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Załaduj dane
data = pd.read_csv('datasetWind.csv')

# Przygotowanie danych: pobieramy obie kolumny (solar i efficiency)
data_values = data[['Wind Speed', 'efficiency']].values

# Podział na dane treningowe i testowe
train_size = int(len(data_values) * 0.8)
train_data = data_values[:train_size]
test_data = data_values[train_size:]

# Normalizacja danych
scaler = MinMaxScaler(feature_range=(0, 1))

# Dopasowanie skalera tylko do danych treningowych
train_scaled = scaler.fit_transform(train_data)

# Przekształcenie danych testowych za pomocą istniejącego skalera
test_scaled = scaler.transform(test_data)

# Tworzenie sekwencji treningowych i testowych
sequence_length = 7

def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        # Tworzymy sekwencję 7 dni z danych solar i efficiency
        feature = data[i:i+sequence_length, :]  # (7 dni, 2 zmienne: solar, efficiency)
        target = data[i+sequence_length:i+sequence_length+7, 1]  # (7 dni, tylko 'efficiency')

        # Sprawdzamy, czy target ma odpowiednią długość (7 dni)
        if target.shape[0] == 7:
            X.append(feature)
            y.append(target)

    # Debugowanie: Sprawdzamy finalny kształt
    print(f"Final X shape: {len(X)}, Final y shape: {len(y)}")
    return np.array(X), np.array(y)

# Tworzenie sekwencji
X_train, y_train = create_sequences(train_scaled, sequence_length)
X_test, y_test = create_sequences(test_scaled, sequence_length)

# Definicja wejścia
inputs = Input(shape=(X_train.shape[1], X_train.shape[2]))

# Architektura modelu
x = LSTM(50, return_sequences=True)(inputs)
x = LSTM(50)(x)
outputs = Dense(7)(x)  # Wyjście na 7 dni do przodu (prognoza efektywności)

# Kompilacja modelu
model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='mean_squared_error')

# Trenowanie
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Przewidywania modelu
predictions = model.predict(X_test)

# Przygotowanie pełnych przewidywań, z dodaniem zerowej kolumny dla 'solar'
predictions_full = np.hstack((predictions[:, 0].reshape(-1, 1), predictions[:, 1].reshape(-1, 1)))

# Sprawdzenie kształtu predictions_full
print("Kształt predictions_full:", predictions_full.shape)  # Powinno być (296, 2)

# Odwrotna transformacja przewidywań
predictions_original = scaler.inverse_transform(predictions_full)

# Przygotowanie pełnych danych rzeczywistych, z dodaniem zerowej kolumny dla 'solar'
y_test_full = np.hstack((y_test[:, 0].reshape(-1, 1), y_test[:, 1].reshape(-1, 1)))

# Odwrotna transformacja danych rzeczywistych
y_test_original = scaler.inverse_transform(y_test_full)

# Oblicz długości danych do wykresu
prediction_length = len(predictions_original)  # długość przewidywań
test_length = len(y_test_original)  # długość rzeczywistych danych testowych

# Sprawdzamy długości, aby upewnić się, że pasują do siebie
print(f"Length of predictions: {prediction_length}")
print(f"Length of actual test data: {test_length}")

# Zakres osi X (dla testu i predykcji) powinien być ten sam
x_range = data.index[train_size + sequence_length:train_size + sequence_length + prediction_length]

# Wizualizacja wyników
plt.figure(figsize=(12, 6))
plt.plot(x_range, y_test_original[:prediction_length, 1], label='Rzeczywiste wartości', color='blue')  # Tylko 'efficiency'
plt.plot(x_range, predictions_original[:, 1], label='Przewidywane wartości', color='red', linestyle='dashed')  # Tylko 'efficiency'


plt.title('Rzeczywiste vs Przewidywane wartości efektywności')
plt.xlabel('Indeks')
plt.ylabel('Efektywność')
plt.ylim(0, 0.5)
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.show()




# Obliczanie metryk
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

# Wyświetlanie wyników
print(f"Metryki modelu:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R-Squared (R²): {r2:.2f}")

# Obliczenie błędu względnego dla całego zbioru testowego
relative_errors = np.abs(y_test_original - predictions_original) / y_test_original * 100  # Liczenie błędów względnych dla każdej wartości
mre = np.mean(relative_errors)  # Średni błąd względny

# Wyświetlenie wyniku
print(f"Średni błąd względny (MRE): {mre:.2f} %")

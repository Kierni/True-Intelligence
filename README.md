#  Analiza Planetarnej Efektywności Produkcji Energii Odnawialnej w Celu Lepszego Zarządzania Zasobami Energetycznymi

## Opis Projektu

Celem projektu jest prognozowanie efektywności odnawialnych źródeł energi w postaci energi słonecznej oraz wiatrowej na podstawie danych historycznych dotyczących prędkości wiatru oraz promieniowania słonecznego. Projekt wykorzystuje dwa różne modele uczenia maszynowego:

1. **Random Forest Regressor** – model oparty na algorytmie lasu losowego do regresji wielokrotnej.
2. **Model LSTM (Long Short-Term Memory)** – model sieci neuronowej zaprojektowany do przetwarzania sekwencji czasowych.

Oba modele zostały zastosowane w celu porównania efektywności ich działania.

Projekt obejmuje etapy od analizy zbiorów danych, czyli  wczytania i przetworzenia danych, poprzez trenowanie modeli, aż po ich ewaluację i wizualizację wyników.

## Technologie i Biblioteki

Projekt został zrealizowany przy użyciu następujących technologii i bibliotek:

- **Python 3.8+**
- **Pandas** – manipulacja danymi
- **NumPy** – obliczenia numeryczne
- **Scikit-learn** – modele uczenia maszynowego i metryki ewaluacyjne
- **TensorFlow/Keras** – modele sieci neuronowych
- **Matplotlib** – wizualizacja danych

## Struktura Danych

Dane używane w projekcie znajdują się w pliku CSV (`datasetWind.csv` lub `dataset.csv`) i zawierają następujące kolumny:

Dla datasetWind.csv
- **index** – znacznik czasu (data i czas)
- **QQ** – prędkość wiatru
- **efficiency** – efektywność elektrowni wiatrowej
Dla dataset.csv 
- - **index** – znacznik czasu (data i czas)
-  **QQ** – promieniowanie słoneczne
- **efficiency** – efektywność elektrowni słonecznej




# Analiza Planetarnej Efektywności Produkcji Energii Odnawialnej w Celu Lepszego Zarządzania Zasobami Energetycznymi


## Opis Projektu

Celem projektu jest analiza planetarnej efektywności produkcji energii odnawialnej na podstawie danych historycznych dotyczących prędkości wiatru oraz innych istotnych parametrów. Projekt wykorzystuje dwa różne modele uczenia maszynowego:

1. **Random Forest Regressor** – model oparty na algorytmie lasu losowego do regresji wielokrotnej.
2. **Model LSTM (Long Short-Term Memory)** – model sieci neuronowej zaprojektowany do przetwarzania sekwencji czasowych.

Projekt obejmuje etapy od wczytania i przetworzenia danych, poprzez trenowanie modeli, aż po ich ewaluację i wizualizację wyników.

## Technologie i Biblioteki

Projekt został zrealizowany przy użyciu następujących technologii i bibliotek:

- **Python 3.8+**
- **Pandas** – manipulacja danymi
- **NumPy** – obliczenia numeryczne
- **Scikit-learn** – modele uczenia maszynowego i metryki ewaluacyjne
- **TensorFlow/Keras** – modele sieci neuronowych
- **Matplotlib** – wizualizacja danych

## Opis Danych Użytych w Modelu

Do budowy modelu wykorzystano trzy zestawy danych, które różniły się zakresem czasowym i charakterem pomiarów. Oto szczegółowy opis:

### 1. Dane z ENTSO-E (European Network of Transmission System Operators for Electricity)

**Źródło:** ENTSO-E Transparency Platform

a) **Produkcja energii elektrycznej z podziałem na rodzaje źródeł energii**

- **Opis:** Dane o produkcji energii były dostępne w rozdzielczości godzinowej.
- **Zawartość:** Obejmowały różne źródła energii, w tym energię wiatrową i solarną, które zostały wyodrębnione do dalszej analizy.

b) **Maksymalna moc sieci energetycznej z podziałem na rodzaje źródeł energii**

- **Opis:** Dane o maksymalnych możliwościach generacyjnych były dostępne w rozdzielczości rocznej.
- **Zawartość:** Zawierały informacje o potencjalnych zdolnościach produkcyjnych energii dla różnych źródeł, w tym energii wiatrowej i solarnej.

---

### 2. Dane meteorologiczne z E-OBS

**Źródło:** E-OBS Climate Data

- **Opis:** Dane meteorologiczne dotyczące promieniowania słonecznego i prędkości wiatru były dostępne w rozdzielczości dziennej.
- **Proces:** Informacje zostały uzyskane przez interpolację połączenia danych naziemnych i satelitarnych na siatkę geograficzną o rozdzielczości 1° (jeden stopień geograficzny).

---
### Proces Agregacji Danych

W celu ujednolicenia danych i przygotowania ich do modelowania, przeprowadzono następujące kroki:

1. **Agregacja danych o produkcji energii**

   - **Opis:** Godzinowe dane o produkcji energii (z ENTSO-E) zostały uśrednione do wartości dziennych, aby dopasować je do rozdzielczości danych meteorologicznych.

2. **Obliczenie "efektywności" produkcji**

   - **Opis:** Wartości dziennej produkcji energii dla źródeł solarnych i wiatrowych zostały podzielone przez maksymalną dzienną moc sieci energetycznej (uzyskaną z danych ENTSO-E).
   - **Wynik:** Wynik tego podziału, nazwany "efektywnością", reprezentuje względną wydajność produkcji w odniesieniu do maksymalnego potencjału generacyjnego.

3. **Podział na dwa zestawy danych**

   - **Dane solarne (`datasetSolar`):**
     - **Zawartość:**
       - Efektywność produkcji energii solarnej
       - Odpowiednie wartości promieniowania słonecznego (z E-OBS)
   
   - **Dane wiatrowe (`datasetWind`):**
     - **Zawartość:**
       - Efektywność produkcji energii wiatrowej
       - Odpowiednie wartości prędkości wiatru (z E-OBS)

---

### Przekazanie Danych do Modeli

Tak przygotowane dane, podzielone na dwa zestawy (solar i wiatr), zostały wykorzystane jako dane wejściowe do modeli analitycznych. Proces agregacji i normalizacji umożliwił analizę efektywności produkcji energii w zależności od warunków atmosferycznych oraz ocenę potencjalnych trendów i zależności w danych.


### Wizualiacja frontendu z backendem:
**Wywołanie komendy w katalogu project:  docker-compose up --build**

**Frontend wyświetli się pod adresem http://127.0.0.1:5000/** .
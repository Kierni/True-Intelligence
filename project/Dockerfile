# Użyj oficjalnego obrazu Python jako bazowego
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY app /app
COPY requirements.txt /app

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "app.py"]

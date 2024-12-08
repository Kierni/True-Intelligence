import numpy as np
import pandas as pd
from netCDF4 import Dataset

# Otwórz pliki NetCDF
nc_file = Dataset('qq_ens_mean_0.1deg_reg_2011-2024_v30.0e.nc', 'r')
nc_file_wind = Dataset('fg_ens_mean_0.1deg_reg_2011-2024_v30.0e.nc', 'r')

# Odczytaj zmienne współrzędnych
latitudes = nc_file.variables['latitude'][:]
longitudes = nc_file.variables['longitude'][:]
time = nc_file.variables['time'][:]  # Czas w formacie numerycznym
qq = nc_file.variables['qq']  # Zmienna do analizy (promieniowanie słoneczne)
fg = nc_file_wind.variables['fg']  # Zmienna do analizy (prędkość wiatru)

# Docelowe współrzędne
target_lat = 52.0  # Podaj szerokość geograficzną
target_lon = 20.0  # Podaj długość geograficzną

# Znajdź najbliższe indeksy dla współrzędnych
lat_idx = np.abs(latitudes - target_lat).argmin()
lon_idx = np.abs(longitudes - target_lon).argmin()

# Odczytaj wszystkie wartości zmiennej 'qq' i 'fg' dla danej lokalizacji i wszystkich czasów
qq_values = qq[:, lat_idx, lon_idx]
fg_values = fg[:, lat_idx, lon_idx]

# Odczytaj informacje o czasie i przekształć do formatu dat
# Sprawdź, czy dane o czasie zawierają atrybuty, np. units (CF-1.6)
time_units = nc_file.variables['time'].units
calendar = nc_file.variables['time'].calendar if hasattr(nc_file.variables['time'], 'calendar') else 'gregorian'

# Użyj biblioteki pandas lub cftime do przekształcenia czasu na czytelny format
import cftime
dates = cftime.num2date(time, units=time_units, calendar=calendar)

# Utwórz DataFrame dla QQ
df_qq = pd.DataFrame({
    'Date': dates,
    'QQ': qq_values
})

# Utwórz DataFrame dla FG
df_fg = pd.DataFrame({
    'Date': dates,
    'Wind Speed': fg_values
})

# Zapisz dane do plików CSV
csv_filename_qq = 'qq_data_for_location.csv'
csv_filename_fg = 'fg_data_for_location.csv'

df_qq.to_csv(csv_filename_qq, index=False)
df_fg.to_csv(csv_filename_fg, index=False)

print(f"Dane QQ zapisano do pliku: {csv_filename_qq}")
print(f"Dane FG zapisano do pliku: {csv_filename_fg}")

# Zamknij pliki NetCDF
nc_file.close()
nc_file_wind.close()

# Wyświetlenie zakresu współrzędnych geograficznych
print("Zakres szerokości geograficznej (latitude):", latitudes.min(), "-", latitudes.max())
print("Zakres długości geograficznej (longitude):", longitudes.min(), "-", longitudes.max())

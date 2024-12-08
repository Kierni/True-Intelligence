from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Wczytaj dane
data = pd.DataFrame({
    'Date': ['2023-09-02', '2023-09-03', '2023-09-04', '2023-09-05', '2023-09-06', '2023-09-07', '2023-09-08'],
    'Predicted_Efficiency': [0.21, 0.19, 0.15, 0.16, 0.22, 0.18, 0.2]
})
data_second = pd.DataFrame({
    'Date': ['2022-08-13', '2022-08-14', '2022-08-15', '2022-08-16', '2022-08-17', '2022-08-18', '2022-08-19'],
    'Predicted_Efficiency': [0.15, 0.2, 0.23, 0.22, 0.22, 0.2, 0.21]
})
@app.route('/data')
def get_data():
    # Przygotowanie danych w formacie JSON
    json_data = {
        'labels': data['Date'].tolist(),
        'values': data['Predicted_Efficiency'].tolist()
    }
    return jsonify(json_data)
@app.route('/data_second')
def get_data_second():
    json_data = {
        'labels': data_second['Date'].tolist(),
        'values': data_second['Predicted_Efficiency'].tolist()
    }
    return jsonify(json_data)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

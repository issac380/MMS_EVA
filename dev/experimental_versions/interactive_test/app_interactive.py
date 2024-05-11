from flask import Flask, jsonify, render_template
from load import get_data  # Assuming start() in load.py is correctly setup to return JSON-friendly data

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the HTML page with the Plotly graph
    return render_template('index.html')

@app.route('/data')
def data():
    # Fetch data using the function from load.py
    plot_data = get_data()
    # Prepare JSON data (ensure the time and values are in a list format if necessary)
    json_data = {key: {'time': value['time'].tolist(), 'values': value['values'].tolist()} for key, value in plot_data.items()}
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)

import matplotlib
matplotlib.use('Agg')  # Ensure to use 'Agg' backend before other imports that might set different backend

# Import necessary packages
from flask import Flask, render_template
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

# Import the function from load.py
from load import start

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    # Get the figure and axes from load.py's start function
    probe = '3'
    start_date  = '2020-07-11'
    end_date    = '2020-07-12'
    fig, ax = start(probe, start_date, end_date)

    # Convert plot to image
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)

    # Return image data
    return output.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)

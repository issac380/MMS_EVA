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

# Generate the plot once and store the image data
fig, ax = start()
output = io.BytesIO()
FigureCanvas(fig).print_png(output)
plt.close(fig)
plot_data = output.getvalue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    # Serve the same plot image data for each request
    return plot_data, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)

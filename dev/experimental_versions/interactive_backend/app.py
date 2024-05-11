from flask import Flask, render_template, request
import io
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvas
import matplotlib.pyplot as plt
from load import start
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    # Get parameters from URL
    probe = request.args.get('probe', '1')  # default probe to 1 if not specified
    start_date = request.args.get('start_date', '2020-07-11')  # provide default dates
    end_date = request.args.get('end_date', '2020-07-12')

    # Get the figure from the load function
    fig, ax = start(probe, start_date, end_date)

    # Convert plot to image
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)

    # Return image data
    return output.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)

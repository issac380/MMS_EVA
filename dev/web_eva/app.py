import io
from flask import Flask, render_template, request, send_file, redirect, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from load import start
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

plot_data = None

def preload_plot_data():
    global plot_data
    print("Preloading plot data...")
    probe, begin, end = "3", "2020-7-11", "2020-7-12"
    fig, ax = start(probe, begin, end)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    plot_data = output.getvalue()
    print("Plot data preloaded at", datetime.datetime.now())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_constant_plot')
def view_constant_plot():
    return render_template('constant_plot.html')

@app.route('/constant_plot_image')
def constant_plot_image():
    if plot_data:
        return send_file(io.BytesIO(plot_data), mimetype='image/png', as_attachment=False)
    else:
        return "Plot data not loaded yet, please try again later."


@app.route('/view_dynamic_plot')
def view_dynamic_plot():
    probe = request.args.get('probe', default='1')
    start_date = request.args.get('start_date', default='2020-07-11')
    end_date = request.args.get('end_date', default='2020-07-12')
    return render_template('dynamic_plot.html', probe=probe, start_date=start_date, end_date=end_date)

@app.route('/generate_dynamic_plot')
def generate_dynamic_plot():
    probe = request.args.get('probe', default='1')
    start_date = request.args.get('start_date', default='2020-07-11')
    end_date = request.args.get('end_date', default='2020-07-12')
    fig, ax = start(probe, start_date, end_date)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    return send_file(io.BytesIO(output.getvalue()), mimetype='image/png')

@app.route('/update_constant_plot', methods=['POST'])
def update_constant_plot():
    probe = request.form['probe']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    print(f"Updated plot for Probe: {probe}, From: {start_time}, To: {end_time}")
    
    return redirect(url_for('view_constant_plot'))

"""
@app.route('/dynamic_plot')
def dynamic_plot():
    probe = request.args.get('probe', '3')
    start_date = request.args.get('start_date', '2020-07-11')
    end_date = request.args.get('end_date', '2020-07-12')

    fig, ax = start(probe, start_date, end_date)  # Use start with parameters
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)
    return output.getvalue(), 200, {'Content-Type': 'image/png'}
"""

if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(preload_plot_data, 'cron', hour=0, minute=0)
    scheduler.start()
    preload_plot_data()
    app.run(debug=True)

import sys
import datetime
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QSizePolicy
from pyspedas import mms
import pytplot as pt

class MyWindow(QMainWindow):
    start_time = None
    
    end_time = None

    zooms = []

    def __init__(self, data):
        super().__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QGridLayout(centralWidget)

        self.figure, self.axes = pt.tplot(data, return_plot_objects=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 1, 0, 1, 9)  # Add the canvas to the second row

        self.cursor = Cursor(self.axes[1], horizOn=False, vertOn=True, color='green', linewidth=2.0)

        self.label = QLabel("Start Time: None" + "\n" + "End Time: None")
        layout.addWidget(self.label, 2, 0, 2, 9)  # Add the label to the third row

        # Add the buttons to the layout
        self.zoom_sel_button = QPushButton("Zoom Selection")
        self.export_sel_button = QPushButton("Export Selection")
        self.clear_sel_button = QPushButton("Clear Selection")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        self.move_left_button = QPushButton("Move Left")
        self.move_right_button = QPushButton("Move Right")
        self.undo_button = QPushButton("Undo")

        self.zoom_sel_button.clicked.connect(self.zoom_selection)
        self.export_sel_button.clicked.connect(self.export_selection)
        self.clear_sel_button.clicked.connect(self.clear_selection)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.move_left_button.clicked.connect(self.move_left)
        self.move_right_button.clicked.connect(self.move_right)
        self.undo_button.clicked.connect(self.undo)

        self.zoom_sel_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.export_sel_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.clear_sel_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.zoom_in_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.zoom_out_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.move_left_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.move_right_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.undo_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        layout.addWidget(self.zoom_sel_button, 0, 0, 1, 3)
        layout.addWidget(self.export_sel_button, 0, 3, 1, 3)
        layout.addWidget(self.clear_sel_button, 0, 6, 1, 3)
        layout.addWidget(self.undo_button, 4, 7, 1, 1)
        layout.addWidget(self.zoom_in_button, 3, 7, 1, 1)
        layout.addWidget(self.zoom_out_button, 5, 7, 1, 1)
        layout.addWidget(self.move_left_button, 4, 6, 1, 1)
        layout.addWidget(self.move_right_button, 4, 8, 1, 1)
        self.canvas.mpl_connect('button_press_event', self.onClick)

        self.show()

    def onClick(self, event):
        decimal_value = event.xdata
        if decimal_value:
            days = int(decimal_value)
            fraction_of_day = decimal_value - days
            date = datetime.datetime(1970, 1, 1) + datetime.timedelta(days=days)
            seconds = int(fraction_of_day * 86400)

            # Add the time to the date
            fraction = datetime.timedelta(seconds=seconds)

            formatted_date = (date + fraction).strftime('%Y-%m-%d %H:%M:%S')

            if self.start_time == None and self.end_time == None:
                self.start_time = (formatted_date, decimal_value)
                self.label.setText("Start Time: " + self.start_time[0] + "\nEnd Time: None")
                for line in self.axes[1].get_lines():
                    if line.get_color() == 'r' and line.get_linestyle() == '--':
                        line.remove()
                self.axes[1].axvline(x=decimal_value, color='r', linestyle='--')
            elif self.end_time == None:
                self.start_time, self.end_time = min([(formatted_date, decimal_value), self.start_time], key=lambda t: t[0]), max([(formatted_date, decimal_value), self.start_time], key=lambda t: t[0])
                self.label.setText("Start Time: " + self.start_time[0] + "\nEnd Time: " + self.end_time[0])
                self.axes[1].axvline(x=decimal_value, color='r', linestyle='--')
            else:
                self.start_time, self.end_time = (formatted_date, decimal_value), None
                self.label.setText("Start Time: " + self.start_time[0] + "\nEnd Time: None")
                for line in self.axes[1].get_lines():
                    if line.get_color() == 'r' and line.get_linestyle() == '--':
                        line.remove()
                self.axes[1].axvline(x=decimal_value, color='r', linestyle='--')

    def export_selection(self):
        print("exporting selection")
        if self.start_time is not None and self.end_time is not None:
            time_diff = (datetime.datetime.strptime(self.end_time[0], '%Y-%m-%d %H:%M:%S') -
                        datetime.datetime.strptime(self.start_time[0], '%Y-%m-%d %H:%M:%S'))
            print("======================================================")
            print("Exporting Time Selection")
            print(f"Start Time: {self.start_time[0]} (Epoch Time: {self.start_time[1]})")
            print(f"End Time: {self.end_time[0]} (Epoch Time: {self.end_time[1]})")
            print(f"Interval: {time_diff} (Epoch Time: {self.end_time[1] - self.start_time[1]})")
            print("======================================================")

    def zoom_selection(self):
        print("zoom in pressed")
        xlim = self.axes[0].get_xlim()
        if xlim is not None and self.start_time is not None and self.end_time is not None:
            self.zooms += [xlim]
            self.change_view(self.start_time[1], self.end_time[1])
    
    def zoom_in(self):
        print("zoom in pressed")
        xlim = self.axes[0].get_xlim()
        if xlim is not None:
            self.zooms += [xlim]
            x_range = abs(xlim[0] - xlim[1])
            self.change_view(xlim[0] + x_range/10, xlim[1] - x_range/10)

    def zoom_out(self):
        print("zoom out pressed")
        xlim = self.axes[0].get_xlim()
        if xlim is not None:
            self.zooms += [xlim]
            x_range = abs(xlim[0] - xlim[1])
            self.change_view(xlim[0] - x_range/10, xlim[1] + x_range/10)

    def move_left(self):
        print("move left pressed")
        xlim = self.axes[0].get_xlim()
        if xlim is not None:
            self.zooms += [xlim]
            x_range = abs(xlim[0] - xlim[1])
            self.change_view(xlim[0] - x_range/10, xlim[1] - x_range/10)

    def move_right(self):
        print("move right pressed")
        xlim = self.axes[0].get_xlim()
        if xlim is not None:
            self.zooms += [xlim]
            x_range = abs(xlim[0] - xlim[1])
            self.change_view(xlim[0] + x_range/10, xlim[1] + x_range/10)

    def undo(self):
        print("undo pressed")
        if self.zooms != []:
            new_xlim = self.zooms.pop()
            self.axes[1].set_xlim(new_xlim)
            self.canvas.draw()

    def clear_selection(self):
        for line in self.axes[1].get_lines():
            if line.get_color() == 'r' and line.get_linestyle() == '--':
                line.remove()
        self.start_time = self.end_time = None
        self.label.setText(("Start Time: None" + "\n" + "End Time: None"))

    def change_view(self, left, right):
        self.axes[1].set_xlim((left, right))
        self.canvas.draw()

def main_function(data):
    app = QApplication(sys.argv)
    window = MyWindow(data)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main_function()

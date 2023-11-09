import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import tplot_main

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        self.setWindowTitle("EVA")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        lbl_stime = QLabel('Start Date')
        ent_stime = QLineEdit()

        lbl_etime = QLabel('End Date')
        ent_etime = QLineEdit()

        lbl_probe = QLabel('Probe Num')
        ent_probe = QLineEdit()

        btn_ABS = QPushButton('Load ABS')
        btn_ABS.clicked.connect(lambda: tplot_main.main_function(probe=ent_probe.text(), 
                                                                 start_date=ent_stime.text(), 
                                                                 end_date=ent_etime.text()))

        btn_Load = QPushButton('Load Data')
        btn_Load.clicked.connect(lambda: print('Under construction.'))

        btn_Add = QPushButton('Add')
        btn_Add.clicked.connect(lambda: print('Under construction.'))

        btn_Edit = QPushButton('Edit')
        btn_Edit.clicked.connect(lambda: print('Under construction.'))

        btn_Exit = QPushButton('Exit')
        btn_Exit.clicked.connect(self.client_exit)

        layout.addWidget(lbl_stime)
        layout.addWidget(ent_stime)

        layout.addWidget(lbl_etime)
        layout.addWidget(ent_etime)

        layout.addWidget(lbl_probe)
        layout.addWidget(ent_probe)

        layout.addWidget(btn_ABS)
        layout.addWidget(btn_Load)
        layout.addWidget(btn_Add)
        layout.addWidget(btn_Edit)
        layout.addWidget(btn_Exit)

    def client_exit(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

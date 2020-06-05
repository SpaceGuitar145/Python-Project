import sys
import time
from time import sleep

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer, QRunnable, QThreadPool, pyqtSlot
from PyQt5.QtGui import QMovie, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLabel, QWidget, QFileDialog
from pneumoniadetect import global_test, global_predict, modelsDir
import threading


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(540, 250, 600, 750)
        self.setWindowTitle("PneumoniaDetectorPro")
        self.setWindowIcon(QIcon("corona.ico"))
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #3a6186")
        self.dir_name = ''

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(0.6)
        self.frame.setFixedSize(205, 600)
        self.frame.setStyleSheet("background-color: #254059")

        self.corona = QLabel(self)
        corona_img = QPixmap('corona.png')
        self.corona.setPixmap(corona_img.scaled(50, 50))
        self.corona.setGeometry(10, 10, 50, 50)
        self.corona.setStyleSheet("background-color: #254059;")

        self.corona_title = QLabel(self)
        self.corona_title.setText('Pneumonia')
        self.corona_title.setGeometry(70, 15, 130, 20)
        self.corona_title.setFont(QFont('Courier New', 13, weight=QFont.Bold))
        self.corona_title.setStyleSheet('background-color: #254059;')

        self.corona_title = QLabel(self)
        self.corona_title.setText('Detector PRO')
        self.corona_title.setGeometry(70, 35, 130, 15)
        self.corona_title.setFont(QFont('Courier New', 13, weight=QFont.Bold))
        self.corona_title.setStyleSheet('background-color: #254059;')

        self.button_predict = QPushButton(self)
        self.button_predict.setGeometry(10, 420, 185, 50)
        self.button_predict.setIcon(QIcon('predict.png'))
        self.button_predict.setFont(QFont('Roboto', 15))
        self.button_predict.setIconSize(QSize(25, 25))
        self.button_predict.setStyleSheet("background-color: #254059;")
        self.button_predict.setText("Predict")

        self.button_test = QPushButton(self)
        self.button_test.setGeometry(10, 480, 185, 50)
        self.button_test.setIcon(QIcon('test.png'))
        self.button_test.setFont(QFont('Roboto', 15))
        self.button_test.setIconSize(QSize(32, 32))
        self.button_test.setStyleSheet("background-color: #254059;")
        self.button_test.setText("Test")

        self.button_about = QPushButton(self)
        self.button_about.setGeometry(10, 540, 185, 50)
        self.button_about.setIcon(QIcon('about.png'))
        self.button_about.setFont(QFont('Roboto', 15))
        self.button_about.setIconSize(QSize(25, 25))
        self.button_about.setStyleSheet("background-color: #254059;")
        self.button_about.setText("About us")

        self.pneumonia_info = QLabel(self)
        self.pneumonia_info.setWordWrap(True)
        self.pneumonia_info.setText('Pneumonia is an infection that inflames the air sacs in one or both lungs. The '
                                    'air sacs may fill with fluid or pus (purulent material), causing cough with '
                                    'phlegm or pus, fever, chills, and difficulty breathing. A variety of organisms, '
                                    'including bacteria, viruses and fungi, can cause pneumonia. Pneumonia can range '
                                    'in seriousness from mild to life-threatening. It is most serious for infants and '
                                    'young children, people older than age 65, and people with health problems or '
                                    'weakened immune systems.')
        self.pneumonia_info.setGeometry(10, 90, 190, 310)
        self.pneumonia_info.setFont(QFont('Roboto', 10.5))
        self.pneumonia_info.setStyleSheet('background-color: #254059;')
        self.pneumonia_info.setAlignment(QtCore.Qt.AlignCenter)

        self.greetings = QLabel(self)
        self.greetings.setWordWrap(True)
        self.greetings.setText(
            'Welcome to the most "accurate" pneumonia detector ever! \n Choose an option and enjoy our app!')
        self.greetings.setGeometry(210, 30, 700, 100)
        self.greetings.setFont(QFont('Roboto', 15))
        self.greetings.setStyleSheet('background-color: #3a6186')
        self.greetings.setAlignment(QtCore.Qt.AlignCenter)

        self.virus_label = QLabel(self)
        self.movie = QMovie(self)
        self.movie2 = QMovie(self)
        self.movie.setFileName('neponel.gif')
        self.movie.setScaledSize(QSize(400, 400))
        self.virus_label.setGeometry(355, 130, 400, 400)
        self.virus_label.setMovie(self.movie)
        self.movie.start()

        self.graph_test = QLabel(self)
        self.graph_test.setGeometry(215, 10, 675, 580)
        self.graph_test.setStyleSheet('background-color: #254059')
        self.graph_test.hide()

        self.statistic_predict = QLabel(self)
        self.statistic_predict.setGeometry(690, 10, 200, 400)
        self.statistic_predict.setStyleSheet('background-color: #254059')
        self.statistic_predict.hide()

        self.thread_pool = QThreadPool()

        self.button_test.clicked.connect(self.button_test_clicked)
        self.button_predict.clicked.connect(self.button_predict_clicked)

        self.show()

    def button_test_clicked(self):
        self.dir_name = QFileDialog.getExistingDirectory(self, 'Select directory') + '/'
        self.virus_label.hide()
        global_test(modelsDir, self.dir_name)
        graph = QPixmap('test_stat.png')
        self.graph_test.setPixmap(graph.scaled(675, 580))
        self.graph_test.show()

    def button_predict_clicked(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select directory') + '/'
        self.virus_label.hide()
        global_predict(modelsDir, dir_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

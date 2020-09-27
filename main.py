import sys
import os
from functools import partial
from os.path import expanduser
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMovie, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLabel, QFileDialog, QTableWidget, \
    QTableWidgetItem, QAbstractItemView
from pneumoniaDetect import PneumoniaDetect


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.frame = QFrame(self)

        self.virusIco = QLabel(self)
        self.virusTitle = QLabel(self)
        self.greetings = QLabel(self)
        self.pneumoniaInfo = QLabel(self)
        self.loading = QLabel(self)
        self.movieLabel = QLabel(self)
        self.testStat = QLabel(self)
        self.predictStat = QLabel(self)
        self.about = QLabel(self)

        self.testButton = QPushButton(self)
        self.predictButton = QPushButton(self)
        self.aboutButton = QPushButton(self)
        self.refreshButton = QPushButton(self)

        self.movie = QMovie(self)

        self.tableWidget = QTableWidget()

        self.modelsDir = os.getcwd() + "/pneumonia/models"
        self.assetsDir = os.getcwd() + "/assets/"

        self.window()

    def window(self):
        self.setGeometry(540, 250, 600, 750)
        self.setWindowTitle("Pneumonia Detector")
        self.setWindowIcon(QIcon(self.assetsDir + "corona.ico"))
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #3a6186")
        self.sidePanel()
        self.createUI()
        self.invokes()

    def createUI(self):
        self.icons(self.virusIco, self.assetsDir + "corona.png", 50, (10, 50), "background-color: #254059;")
        self.virusIco.show()
        self.labels(self.virusTitle, "Pneumonia\nDetector", (70, 15, 130, 30),
                    QFont("Courier New", 13, weight=QFont.Bold), "background-color: #254059;")
        self.virusTitle.show()
        self.labels(self.pneumoniaInfo, "Pneumonia is an infection that inflames the air sacs in one or both lungs. The"
                                        " air sacs may fill with fluid or pus (purulent material), causing cough with "
                                        "phlegm or pus, fever, chills, and difficulty breathing. A variety of "
                                        "organisms, including bacteria, viruses and fungi, can cause pneumonia. "
                                        "Pneumonia can range in seriousness from mild to life-threatening. It is most "
                                        "serious for infants and young children, people older than age 65, and people "
                                        "with health problems or weakened immune systems.", (10, 90, 190, 310),
                    QFont("Roboto", 10), "background-color: #254059;", Qt.AlignCenter)
        self.pneumoniaInfo.show()
        self.labels(self.greetings, "Welcome to the pneumonia detector! \n Choose an option and enjoy our app!",
                    (210, 30, 700, 100), QFont("Courier", 15, weight=QFont.Bold), "background-color: #3a6186",
                    Qt.AlignCenter)
        self.greetings.show()
        self.labels(self.loading, "Loading...", (450, 110, 400, 400), QFont("Courier", 30, weight=QFont.Bold),
                    "background-color: #3a6186", hide=True)
        self.labels(self.testStat, "", (215, 10, 675, 580), QFont("Courier", 30, weight=QFont.Bold),
                    "background-color: #254059", hide=True)
        self.labels(self.predictStat, "", (690, 10, 200, 400), QFont("Courier", 30, weight=QFont.Bold),
                    "background-color: #254059", hide=True)
        self.labels(self.about, "This app gives only chances of disease, it's not a medical conclusions. If you "
                                "get more than 35% in case you input a good photo, then you you should see a "
                                "doctor. If you choose a test option, you must to give a directory which consist "
                                "of 2 directories,'NORMAL' and 'PNEUMONIA', this command tests the "
                                "app(works not so fast). To use the predict button you must give a directory "
                                "consist of '.jpg' or '.jpeg'. The example photos are given below.",
                    (210, 0, 600, 250), QFont("Courier", 15, weight=QFont.Bold), "background-color: #3a6186",
                    hide=True)

        self.buttons(self.testButton, "Test", QIcon(self.assetsDir + "test.png"), QSize(32, 32), QFont("Roboto", 15),
                     (10, 480, 185, 50), "background-color: #254059;")
        self.testButton.show()
        self.buttons(self.predictButton, "Predict", QIcon(self.assetsDir + "predict.png"), QSize(25, 25),
                     QFont("Roboto", 15), (10, 420, 185, 50), "background-color: #254059;")
        self.predictButton.show()
        self.buttons(self.aboutButton, "About", QIcon(self.assetsDir + "about.png"), QSize(25, 25), QFont("Roboto", 15),
                     (10, 540, 185, 50), "background-color: #254059;", hide=False)
        self.aboutButton.show()
        self.buttons(self.refreshButton, "Refresh", QIcon(self.assetsDir + "refresh.png"), QSize(25, 25),
                     QFont("Roboto", 15), (10, 540, 185, 50), "background-color: #254059;", hide=True)

        self.movieStart(self.movieLabel, self.movie, self.assetsDir + "neponel.gif", QSize(400, 400),
                        (355, 130, 400, 400))

    def invokes(self):
        self.testButton.clicked.connect(partial(self.buttonClicked, self.testButton))
        self.predictButton.clicked.connect(partial(self.buttonClicked, self.predictButton))
        self.refreshButton.clicked.connect(partial(self.buttonClicked, self.refreshButton))
        self.aboutButton.clicked.connect(partial(self.buttonClicked, self.aboutButton))

    def sidePanel(self):
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(1)
        self.frame.setFixedSize(205, 600)
        self.frame.setStyleSheet("background-color: #254059")

    @staticmethod
    def icons(labelObject, title, scale, geometry, backColor):
        labelObject.setPixmap(QPixmap(title).scaled(scale, scale))
        labelObject.setGeometry(geometry[0], geometry[0], geometry[1], geometry[1])
        labelObject.setStyleSheet(backColor)

    @staticmethod
    def labels(labelObject, text, geometry, font, backColor, alignment=None, hide=False):
        labelObject.setWordWrap(True)
        labelObject.setText(text)
        labelObject.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        labelObject.setFont(font)
        labelObject.setStyleSheet(backColor)
        if alignment:
            labelObject.setAlignment(alignment)
        if hide:
            labelObject.hide()

    @staticmethod
    def buttons(buttonObject, text, icon, icoSize, font, geometry, backColor, hide=False):
        buttonObject.setText(text)
        buttonObject.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        buttonObject.setIcon(icon)
        buttonObject.setIconSize(icoSize)
        buttonObject.setFont(font)
        buttonObject.setStyleSheet(backColor)
        if hide:
            buttonObject.hide()

    def buttonClicked(self, buttonObject):
        self.greetings.hide()
        self.movieLabel.hide()
        self.testButton.hide()
        self.predictButton.hide()
        self.aboutButton.hide()
        if buttonObject == self.testButton:
            imagesDir = QFileDialog.getExistingDirectory(self, "Select directory", expanduser("~"),
                                                         QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)+"/"
            self.refreshButton.show()
            self.refreshButton.setEnabled(False)
            self.loading.show()
            self.repaint()
            pd = PneumoniaDetect(self.modelsDir, imagesDir)
            pd.modelsTest()
            graph = QPixmap("test_stat.png")
            self.testStat.setPixmap(graph.scaled(675, 580))
            self.testStat.show()
            self.refreshButton.setEnabled(True)
            self.repaint()
        elif buttonObject == self.predictButton:
            imagesDir = QFileDialog.getExistingDirectory(self, "Select directory", expanduser("~"),
                                                         QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)+"/"
            self.loading.show()
            self.repaint()
            pd = PneumoniaDetect(self.modelsDir, imagesDir)
            result = pd.modelsPrediction()
            self.tableWidget = QTableWidget()
            self.tableWidget.setWindowTitle("Pneumonia probability")
            self.tableWidget.setStyleSheet("background-color: #3a6186")
            self.tableWidget.setGeometry(745, 250, 695, 600)
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(result))

            j = 0
            for i in result:
                self.tableWidget.setItem(j, 0, QTableWidgetItem(i))
                self.tableWidget.setItem(j, 1, QTableWidgetItem((str(result[i])[:6]) + "%"))
                j += 1

            self.tableWidget.setHorizontalHeaderLabels(["Image title", "Probability"])
            self.tableWidget.setColumnWidth(0, 300)
            self.tableWidget.setColumnWidth(1, 100)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.show()
            self.createUI()
        elif buttonObject == self.aboutButton:
            self.about.show()
            self.refreshButton.show()
            self.refreshButton.setEnabled(False)
            self.repaint()
            self.refreshButton.setEnabled(True)
            self.repaint()
        elif buttonObject == self.refreshButton:
            self.createUI()

    @staticmethod
    def movieStart(labelObject, movieObject, title, movieSize, geometry):
        movieObject.setFileName(title)
        movieObject.setScaledSize(movieSize)
        labelObject.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        labelObject.setMovie(movieObject)
        movieObject.start()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
sys.exit(app.exec())

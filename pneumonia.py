import sys
from os.path import expanduser
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLabel, QFileDialog, QTableWidget, \
    QTableWidgetItem, QAbstractItemView
from pneumoniadetect import modelsTest, modelsDir, modelsPrediction


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(540, 250, 600, 750)
        self.setWindowTitle("Pneumonia Detector")
        self.setWindowIcon(QIcon("corona.ico"))
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #3a6186")
        self.dir_name = ''

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(1)
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

        self.andrei_name = QLabel(self)
        self.andrei_name.setText("Andrei Shpakouski")
        self.andrei_name.setFont(QFont("Courier", 20, weight=QFont.Bold))
        self.andrei_name.setGeometry(215, 20, 300, 30)
        self.andrei_name.setStyleSheet("background-color: #3a6186")
        self.andrei_name.hide()

        self.andrei_role = QLabel(self)
        self.andrei_role.setText("Role:")
        self.andrei_role.setFont(QFont("Courier", 15, weight=QFont.Bold))
        self.andrei_role.setGeometry(215, 60, 55, 20)
        self.andrei_role.setStyleSheet("background-color: #3a6186")
        self.andrei_role.hide()

        self.andrei_role_fact = QLabel(self)
        self.andrei_role_fact.setText("Backend & Frontend")
        self.andrei_role_fact.setFont(QFont("Courier", 12))
        self.andrei_role_fact.setGeometry(280, 62, 250, 20)
        self.andrei_role_fact.setStyleSheet("background-color: #3a6186")
        self.andrei_role_fact.hide()

        self.andrei_imp = QLabel(self)
        self.andrei_imp.setText("Introduces:")
        self.andrei_imp.setFont(QFont("Courier", 14, weight=QFont.Bold))
        self.andrei_imp.setGeometry(215, 90, 122, 20)
        self.andrei_imp.setStyleSheet("background-color: #3a6186")
        self.andrei_imp.hide()

        self.andrei_imp_facts1 = QLabel(self)
        self.andrei_imp_facts1.setText("- Created modelsTest and modelsPrediction functions")
        self.andrei_imp_facts1.setGeometry(342, 93, 497, 15)
        self.andrei_imp_facts1.setFont(QFont("Courier", 12))
        self.andrei_imp_facts1.setStyleSheet("background-color: #3a6186;")
        self.andrei_imp_facts1.hide()

        self.andrei_imp_facts2 = QLabel(self)
        self.andrei_imp_facts2.setText("- Configured test and predict functions for GUI needs")
        self.andrei_imp_facts2.setGeometry(342, 110, 510, 15)
        self.andrei_imp_facts2.setFont(QFont("Courier", 12))
        self.andrei_imp_facts2.setStyleSheet("background-color: #3a6186;")
        self.andrei_imp_facts2.hide()

        self.andrei_imp_facts3 = QLabel(self)
        self.andrei_imp_facts3.setWordWrap(True)
        self.andrei_imp_facts3.setText("- Added and taught MobileNetV2 and VGG16 models")
        self.andrei_imp_facts3.setGeometry(342, 127, 550, 15)
        self.andrei_imp_facts3.setFont(QFont("Courier", 12))
        self.andrei_imp_facts3.setStyleSheet("background-color: #3a6186;")
        self.andrei_imp_facts3.hide()

        self.vova_name = QLabel(self)
        self.vova_name.setText("Volodymyr Mamedov")
        self.vova_name.setFont(QFont("Courier", 20, weight=QFont.Bold))
        self.vova_name.setGeometry(215, 167, 300, 30)
        self.vova_name.setStyleSheet("background-color: #3a6186")
        self.vova_name.hide()

        self.vova_role = QLabel(self)
        self.vova_role.setText("Role:")
        self.vova_role.setFont(QFont("Courier", 15, weight=QFont.Bold))
        self.vova_role.setGeometry(215, 207, 55, 20)
        self.vova_role.setStyleSheet("background-color: #3a6186")
        self.vova_role.hide()

        self.vova_role_fact = QLabel(self)
        self.vova_role_fact.setText("Backend")
        self.vova_role_fact.setFont(QFont("Courier", 12))
        self.vova_role_fact.setGeometry(280, 209, 250, 20)
        self.vova_role_fact.setStyleSheet("background-color: #3a6186")
        self.vova_role_fact.hide()

        self.vova_imp = QLabel(self)
        self.vova_imp.setText("Introduces:")
        self.vova_imp.setFont(QFont("Courier", 14, weight=QFont.Bold))
        self.vova_imp.setGeometry(215, 237, 122, 20)
        self.vova_imp.setStyleSheet("background-color: #3a6186")
        self.vova_imp.hide()

        self.vova_imp_facts1 = QLabel(self)
        self.vova_imp_facts1.setText("- Added and taught DenseNet201 and InceptionV3 models")
        self.vova_imp_facts1.setGeometry(342, 240, 497, 15)
        self.vova_imp_facts1.setFont(QFont("Courier", 12))
        self.vova_imp_facts1.setStyleSheet("background-color: #3a6186;")
        self.vova_imp_facts1.hide()

        self.vova_imp_facts2 = QLabel(self)
        self.vova_imp_facts2.setText("- Help to create modelsPrediction and modelsTest functions")
        self.vova_imp_facts2.setGeometry(342, 257, 550, 15)
        self.vova_imp_facts2.setFont(QFont("Courier", 12))
        self.vova_imp_facts2.setStyleSheet("background-color: #3a6186;")
        self.vova_imp_facts2.hide()

        self.vova_imp_facts3 = QLabel(self)
        self.vova_imp_facts3.setWordWrap(True)
        self.vova_imp_facts3.setText("- Optimized functions work for the processor")
        self.vova_imp_facts3.setGeometry(342, 274, 550, 15)
        self.vova_imp_facts3.setFont(QFont("Courier", 12))
        self.vova_imp_facts3.setStyleSheet("background-color: #3a6186;")
        self.vova_imp_facts3.hide()

        self.valera_name = QLabel(self)
        self.valera_name.setText("Valerii Bahrov")
        self.valera_name.setFont(QFont("Courier", 20, weight=QFont.Bold))
        self.valera_name.setGeometry(215, 314, 300, 30)
        self.valera_name.setStyleSheet("background-color: #3a6186")
        self.valera_name.hide()

        self.valera_role = QLabel(self)
        self.valera_role.setText("Role:")
        self.valera_role.setFont(QFont('Courier', 15, weight=QFont.Bold))
        self.valera_role.setGeometry(215, 354, 55, 20)
        self.valera_role.setStyleSheet("background-color: #3a6186")
        self.valera_role.hide()

        self.valera_role_fact = QLabel(self)
        self.valera_role_fact.setText("Frontend")
        self.valera_role_fact.setFont(QFont("Courier", 12))
        self.valera_role_fact.setGeometry(280, 356, 250, 20)
        self.valera_role_fact.setStyleSheet("background-color: #3a6186")
        self.valera_role_fact.hide()

        self.valera_imp = QLabel(self)
        self.valera_imp.setText("Introduces:")
        self.valera_imp.setFont(QFont("Courier", 14, weight=QFont.Bold))
        self.valera_imp.setGeometry(215, 384, 122, 20)
        self.valera_imp.setStyleSheet("background-color: #3a6186")
        self.valera_imp.hide()

        self.valera_imp_facts1 = QLabel(self)
        self.valera_imp_facts1.setText("- Created most of the GUI")
        self.valera_imp_facts1.setGeometry(342, 387, 497, 15)
        self.valera_imp_facts1.setFont(QFont('Courier', 12))
        self.valera_imp_facts1.setStyleSheet("background-color: #3a6186;")
        self.valera_imp_facts1.hide()

        self.valera_imp_facts2 = QLabel(self)
        self.valera_imp_facts2.setText("- Help to configure predict and test function for GUI needs")
        self.valera_imp_facts2.setGeometry(342, 404, 510, 15)
        self.valera_imp_facts2.setFont(QFont("Courier", 12))
        self.valera_imp_facts2.setStyleSheet("background-color: #3a6186;")
        self.valera_imp_facts2.hide()

        self.valera_imp_facts3 = QLabel(self)
        self.valera_imp_facts3.setWordWrap(True)
        self.valera_imp_facts3.setText("- Introduced predict and test function to GUI")
        self.valera_imp_facts3.setGeometry(342, 421, 550, 15)
        self.valera_imp_facts3.setFont(QFont("Courier", 12))
        self.valera_imp_facts3.setStyleSheet("background-color: #3a6186;")
        self.valera_imp_facts3.hide()

        self.button_refresh = QPushButton(self)
        self.button_refresh.setGeometry(10, 540, 185, 50)
        self.button_refresh.setIcon(QIcon("refresh.png"))
        self.button_refresh.setFont(QFont("Roboto", 15))
        self.button_refresh.setIconSize(QSize(25, 25))
        self.button_refresh.setStyleSheet("background-color: #254059;")
        self.button_refresh.setText("Refresh")
        self.button_refresh.hide()

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
        self.pneumonia_info.setFont(QFont("Roboto", 10))
        self.pneumonia_info.setStyleSheet("background-color: #254059;")
        self.pneumonia_info.setAlignment(QtCore.Qt.AlignCenter)

        self.greetings = QLabel(self)
        self.greetings.setWordWrap(True)
        self.greetings.setText(
            'Welcome to the pneumonia detector! \n Choose an option and enjoy our app!')
        self.greetings.setGeometry(210, 30, 700, 100)
        self.greetings.setFont(QFont("Courier", 15, weight=QFont.Bold))
        self.greetings.setStyleSheet("background-color: #3a6186")
        self.greetings.setAlignment(QtCore.Qt.AlignCenter)

        self.virus_label = QLabel(self)
        self.movie = QMovie(self)
        self.movie.setFileName("neponel.gif")
        self.movie.setScaledSize(QSize(400, 400))
        self.virus_label.setGeometry(355, 130, 400, 400)
        self.virus_label.setMovie(self.movie)
        self.movie.start()

        self.loading_label = QLabel(self)
        self.loading_label.setGeometry(450, 110, 400, 400)
        self.loading_label.setText("Loading...")
        self.loading_label.setFont(QFont("Courier", 30, weight=QFont.Bold))
        self.loading_label.hide()

        self.graph_test = QLabel(self)
        self.graph_test.setGeometry(215, 10, 675, 580)
        self.graph_test.setStyleSheet("background-color: #254059")
        self.graph_test.hide()

        self.statistic_predict = QLabel(self)
        self.statistic_predict.setGeometry(690, 10, 200, 400)
        self.statistic_predict.setStyleSheet("background-color: #254059")
        self.statistic_predict.hide()

        self.tableWidget = QTableWidget()

        self.button_test.clicked.connect(self.button_test_clicked)
        self.button_predict.clicked.connect(self.button_predict_clicked)
        self.button_refresh.clicked.connect(self.button_refresh_clicked)
        self.button_about.clicked.connect(self.button_about_clicked)

        self.show()

    def button_about_clicked(self):

        self.greetings.hide()
        self.virus_label.hide()
        self.button_about.hide()
        self.button_predict.hide()
        self.button_test.hide()
        self.button_refresh.show()

        self.andrei_name.show()
        self.andrei_role.show()
        self.andrei_role_fact.show()
        self.andrei_imp.show()
        self.andrei_imp_facts1.show()
        self.andrei_imp_facts2.show()
        self.andrei_imp_facts3.show()

        self.vova_name.show()
        self.vova_role.show()
        self.vova_role_fact.show()
        self.vova_imp.show()
        self.vova_imp_facts1.show()
        self.vova_imp_facts2.show()
        self.vova_imp_facts3.show()

        self.valera_name.show()
        self.valera_role.show()
        self.valera_role_fact.show()
        self.valera_imp.show()
        self.valera_imp_facts1.show()
        self.valera_imp_facts2.show()
        self.valera_imp_facts3.show()

    def button_refresh_clicked(self):

        self.greetings.show()
        self.button_refresh.hide()
        self.tableWidget.hide()
        self.button_test.show()
        self.button_predict.show()
        self.button_about.show()
        self.graph_test.hide()
        self.loading_label.hide()
        self.virus_label.show()

        self.andrei_name.hide()
        self.andrei_role.hide()
        self.andrei_role_fact.hide()
        self.andrei_imp.hide()
        self.andrei_imp_facts1.hide()
        self.andrei_imp_facts2.hide()
        self.andrei_imp_facts3.hide()

        self.vova_name.hide()
        self.vova_role.hide()
        self.vova_role_fact.hide()
        self.vova_imp.hide()
        self.vova_imp_facts1.hide()
        self.vova_imp_facts2.hide()
        self.vova_imp_facts3.hide()

        self.valera_name.hide()
        self.valera_role.hide()
        self.valera_role_fact.hide()
        self.valera_imp.hide()
        self.valera_imp_facts1.hide()
        self.valera_imp_facts2.hide()
        self.valera_imp_facts3.hide()

    def button_test_clicked(self):

        self.dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select directory",
            expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog) + "/"

        self.greetings.hide()
        self.button_test.hide()
        self.button_predict.hide()
        self.button_about.hide()
        self.button_refresh.show()
        self.virus_label.hide()
        self.loading_label.show()
        self.button_refresh.setEnabled(False)
        self.repaint()

        modelsTest(modelsDir, self.dir_name)
        graph = QPixmap("test_stat.png")
        self.graph_test.setPixmap(graph.scaled(675, 580))
        self.graph_test.show()
        self.button_refresh.setEnabled(True)
        self.repaint()

    def button_predict_clicked(self):

        self.dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select directory",
            expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog) + "/"

        self.greetings.hide()
        self.button_test.hide()
        self.button_predict.hide()
        self.button_about.hide()
        self.button_refresh.show()
        self.virus_label.hide()
        self.loading_label.show()
        self.button_refresh.setEnabled(False)
        self.repaint()

        result = modelsPrediction(modelsDir, self.dir_name)

        self.virus_label.hide()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(result))
        print(result)
        j = 0
        for i in result:
            j += 1
            self.tableWidget.setItem(j, 0, QTableWidgetItem(i))
            self.tableWidget.setItem(j, 1, QTableWidgetItem((str(result[i])[:6]) + "%"))

        self.tableWidget.setMaximumSize(695, 600)
        self.tableWidget.setMinimumSize(695, 600)
        self.tableWidget.move(745, 213)
        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.show()

        self.button_refresh.setEnabled(True)
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

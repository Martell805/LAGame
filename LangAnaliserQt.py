import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from MW import Ui_MainWindow


class LAG(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.choose_btn.clicked.connect(self.choose)
        self.start_btn.clicked.connect(self.start)
        self.shub_btn.clicked.connect(self.hub_start)

    def choose(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать программу', '', '*.lvl')[0]
        file = open('lvlname.data', 'w')
        file.write(fname)
        file.close()

    def start(self):
        import LAGame

    def hub_start(self):
        fname = 'levels/hub.lvl'
        file = open('lvlname.data', 'w')
        file.write(fname)
        file.close()
        import LAGame


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LAG()
    ex.show()
    sys.exit(app.exec_())

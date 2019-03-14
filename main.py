import os
import sys
from math import factorial
from random import randint
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngine import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWebChannel import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        '''  Create webbrowser frame '''
        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)  # centralize
        self.browser.load(QUrl.fromLocalFile(os.getcwd() + "/static/index.html"))  # open .html located in static)

        '''  Create webchannel to communicate between pyqt and js '''
        self.web = WebClass(self)  # must be instance of QObject!
        self.channel = QWebChannel(self)
        self.channel.registerObject("server", self.web)  # register object. check the static/qtconnector.js file
        self.browser.page().setWebChannel(self.channel)  # set channel to page

        self.mainToolBar = QToolBar(self)
        self.addToolBar(self.mainToolBar)
        randBtn = QPushButton("Случайное число", self)
        self.mainToolBar.addWidget(randBtn)
        randBtn.clicked.connect(lambda: self.web.value_changed.emit(randint(1, 100000)))

        directJSBtn = QPushButton("Прямой вызов JS", self)
        self.mainToolBar.addWidget(directJSBtn)
        directJSBtn.clicked.connect(lambda: self.browser.page().runJavaScript("alert('Я вызвана напрямую из Qt!');"))


class WebClass(QObject):
    value_changed = Signal(int)
    factorial_changed = Signal(int)
    @Slot()
    def calledFromJs(self):
        QMessageBox.information(self.parent(), "calledFromJs", "I'm called by js!")

    @Slot(str)
    def calledFromJsWithArg(self, arg):
        QMessageBox.information(self.parent(),
                                "calledFromJsWithArg",
                                "Привет, я — метод Qt, вызванный из js, мой аргумент — {}".format(arg))

    @Slot(int)
    def factorial(self, value):
        f = factorial(value)
        self.factorial_changed.emit(f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("PyQt-JS")
    window.showMaximized()
    sys.exit(app.exec_())

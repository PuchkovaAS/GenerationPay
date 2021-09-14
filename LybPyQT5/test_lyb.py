# -*- coding: cp1251 -*-
import sys

import widgets.db_path as button
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

f = open('style/darksource.stylesheet', 'r')
style = f.read()


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.setStyleSheet(style)

        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        self.btn = button.SimpleDBPath(mainwin=self)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.btn)

        central_widget.setLayout(main_layout)

    def test_btn(self):
        print(32)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = Main_Window()
    root.showMaximized()
    sys.exit(app.exec_())

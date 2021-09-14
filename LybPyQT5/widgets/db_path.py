import firebirdsql
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QFileDialog

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.line_text import LineText


class SimpleDBPath(QWidget):
    my_signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, mainwin):
        super().__init__()
        self.mainwin = mainwin

        layout: QGridLayout = QGridLayout()
        self.btn = SimpleBtn(label='...', width=30, height=30, click_func=self.openBD)
        self.btn_open = SimpleBtn(label='open', width=50, height=30, click_func=self.open_database)

        self.line_text = LineText(text='', placeholder='path_bd', min_width=150)
        self.line_server = LineText(text='127.0.0.1', placeholder='ip_address', min_width=150)

        layout.addWidget(self.line_text, 0, 0, 1, 2)
        layout.addWidget(self.btn, 0, 3, 1, 1)
        layout.addWidget(self.line_server, 2, 0, 1, 2)
        layout.addWidget(self.btn_open, 2, 3, 1, 1)

        self.setLayout(layout)

    def open_database(self):
        self.mainwin.con = None
        try:
            con = firebirdsql.connect(
                host=self.line_server.text(),
                database=self.line_text.text(),
                port=3050,
                user='sysdba',
                password='masterkey',
                charset='utf8'
            )
            con.close()
            self.my_signal.emit(self.line_text.text(), self.line_server.text())
        except Exception as e:
            QMessageBox().warning(self, "Ошибка", str(e.__str__()) + '\n Ошибка подлючения к базе', QMessageBox.Ok,
                                  QMessageBox.Ok)

    def openBD(self):

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть Базу', "", "GDB (*.GDB)", options=options)
        self.BD = path

        if path == '':
            return
        self.line_text.setText(self.BD)

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu

style_good = 'border: 1px solid #2196F3'
style_warning = 'border: 1px solid #f44336;'


class InfoLabel(QtWidgets.QLabel):
    doubleClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(style_good)

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.doubleClicked.emit()
        # QtWidgets.QLabel.mousePressEvent(self, QMouseEvent)
        QtWidgets.QLabel.mouseDoubleClickEvent(self, QMouseEvent)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clear = contextMenu.addAction("Удалить")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clear:
            self.setStyleSheet(style_warning)
            self.setText('Не найден')


class SimpleLabel(QtWidgets.QLabel):
    def __init__(self, text=None, WordWrap=None):
        super().__init__()
        if text is not None: self.setText(text)
        if WordWrap is not None: self.setWordWrap(WordWrap)

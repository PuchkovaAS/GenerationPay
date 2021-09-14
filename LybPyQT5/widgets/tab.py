from PyQt5.QtWidgets import QWidget, QGridLayout


class LibTab(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)


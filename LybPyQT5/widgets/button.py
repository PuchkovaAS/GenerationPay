from PyQt5.QtWidgets import QPushButton


class SimpleBtn(QPushButton):
    def __init__(self, label='', click_func=None, height=None, width=None):
        super().__init__()

        if height is not None: self.setFixedHeight(height)
        if width is not None: self.setFixedWidth(width)

        self.setText(label)
        if click_func is not None:
            self.clicked.connect(click_func)

from PyQt5.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
    def __init__(self, label='', click_func=None, value=None):
        super().__init__()
        self.setText(label)
        if click_func is not None:
            self.clicked.connect(click_func)
        if value is not None: self.setChecked(value)

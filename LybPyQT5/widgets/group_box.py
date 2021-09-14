from PyQt5.QtWidgets import QGroupBox


class GroupBox(QGroupBox):
    def __init__(self, name=None, layout=None):
        super().__init__(name)
        if layout is not None: self.setLayout(layout)


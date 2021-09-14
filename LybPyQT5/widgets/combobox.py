from PyQt5.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self, name=None, layout=None, line=None):
        super().__init__(name)

        for text in line:
            self.addItem(text)

        if layout is not None: self.setLayout(layout)


from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QLabel


class SpinBox(QSpinBox):
    def __init__(self, max=None, min=None, value=None, height=None, width=None, change_func=None):
        super().__init__()
        if max is not None: self.setMaximum(max)
        if min is not None: self.setMinimum(min)
        if value is not None: self.setValue(value)

        if height is not None: self.setFixedHeight(height)
        if width is not None: self.setFixedWidth(height)

        if change_func is not None: self.valueChanged.connect(change_func)


class SpinBoxText(QWidget):
    def __init__(self, label=None, max=None, min=None, value=None, height=None, width=None, change_func=None):
        super().__init__()
        layout: QGridLayout = QGridLayout()
        self.spin_box = QSpinBox()
        self.label = QLabel(label)

        if max is not None: self.spin_box.setMaximum(max)
        if min is not None: self.spin_box.setMinimum(min)
        if value is not None: self.spin_box.setValue(value)

        if height is not None: self.spin_box.setFixedHeight(height)
        if width is not None: self.spin_box.setFixedWidth(height)

        if change_func is not None: self.spin_box.valueChanged.connect(change_func)

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.spin_box, 0, 1)
        self.setLayout(layout)

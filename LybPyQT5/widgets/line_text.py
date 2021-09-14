from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel


class LineText(QLineEdit):
    def __init__(self, text=None, placeholder=None, tooltip=None, height=None, width=None, min_width=None, func_text_change=None):
        super().__init__()

        if height is not None: self.setFixedHeight(height)
        if width is not None: self.setFixedWidth(height)
        if min_width is not None: self.setMinimumWidth(min_width)

        if placeholder is not None: self.setPlaceholderText(placeholder)
        if tooltip is not None: self.setToolTip(tooltip)
        if text is not None: self.setText(text)
        if func_text_change is not None: self.textChanged.connect(func_text_change)


class LineLabel(QWidget):
    def __init__(self, label=None, number=None):
        super().__init__()
        main_layout = QHBoxLayout()
        self.line_edit = QLineEdit(number)
        validator = QIntValidator()
        self.line_edit.setValidator(validator)
        self.line_edit.setMaximumHeight(35)
        main_layout.addWidget(QLabel(label))
        main_layout.addWidget(self.line_edit)

        self.setLayout(main_layout)

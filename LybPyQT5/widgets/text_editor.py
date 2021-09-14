from PyQt5.QtWidgets import QTextEdit


class TextEditor(QTextEdit):
    def __init__(self, text=None, placeholder=None, tooltip=None, height=None, width=None, objectName=None):
        super().__init__(objectName=objectName)
        if height is not None: self.setFixedHeight(height)
        if width is not None: self.setFixedWidth(height)

        if placeholder is not None: self.setPlaceholderText(placeholder)
        if tooltip is not None: self.setToolTip(tooltip)
        if text is not None: self.setText(text)


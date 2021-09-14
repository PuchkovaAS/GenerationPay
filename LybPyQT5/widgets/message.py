from PyQt5.QtWidgets import QMessageBox


class Message(QMessageBox):
    def __init__(self, msgbtn=None, detailed_text=None, text=None, info_text=None, title=None, count_btn=1,
                 icon=QMessageBox.Information):
        super().__init__()

        self.setIcon(icon)

        if text:
            self.setText(text)

        if info_text:
            self.setInformativeText(info_text)

        if title:
            self.setWindowTitle(title)

        if detailed_text:
            self.setDetailedText(detailed_text)

        if count_btn == 1:
            self.setStandardButtons(QMessageBox.Ok)
        elif count_btn == 2:
            self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if msgbtn:
            self.buttonClicked.connect(msgbtn)

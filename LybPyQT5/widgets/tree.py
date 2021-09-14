from PyQt5.QtWidgets import QTreeWidget, QHeaderView


class SimpleTree(QTreeWidget):
    def __init__(self, header=[], count_column=None, click_func=None, height=None, width=None):
        super().__init__()

        if height is not None: self.setFixedHeight(height)
        if width is not None: self.setFixedWidth(height)

        if count_column is not None: self.setColumnCount(count_column)
        self.setHeaderLabels(header)

        myQHeaderView = self.header()
        myQHeaderView.setStretchLastSection(True)
        for column in range(count_column):
            myQHeaderView.setSectionResizeMode(column, QHeaderView.Stretch)

        self.setDropIndicatorShown(True)

        if click_func is not None:
            self.itemClicked.connect(click_func)

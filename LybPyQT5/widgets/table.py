from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QKeySequence, QPainter, QDrag
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QMenu, QApplication, QLabel, QHeaderView, \
    QAbstractScrollArea, QTableView


class TableWidgetCustom(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)  # Выделяет всю строку

    def dropEvent(self, event):
        md = event.mimeData().text()

        # row and column where it comes from
        row = self.indexAt(event.pos()).row()
        column = self.indexAt(event.pos()).column()
        self.setItem(row, column, QTableWidgetItem(md))

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy()
        elif event.matches(QKeySequence.Paste):
            self.insert()
        elif event.matches(QKeySequence.Delete):
            self.delete()
        else:
            QTableWidget.keyPressEvent(self, event)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clear = contextMenu.addAction("Очистить")
        delete_empty = contextMenu.addAction("Удалить пустые")
        add_empty = contextMenu.addAction("Добавить строку")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clear:
            self.clear_table()
        elif action == delete_empty:
            self.delete_empty()
        elif action == add_empty:
            self.add_empty()

    def add_empty(self):
        self.setRowCount(self.rowCount() + 1)
        for col in range(self.columnCount()):
            self.setItem(self.rowCount() - 1, col, QTableWidgetItem(''))

    def clear_table(self):
        self.setItem(0, 0, QTableWidgetItem(''))
        self.setRowCount(1)

    def delete_empty(self):
        text = self.get_data(0, 0, self.rowCount() - 1, self.columnCount() - 1)
        stroka = '\t' * (self.columnCount())

        self.setRowCount(0)
        rows = text.split('\n')
        new_row = [row for row in rows if row != stroka]
        self.insetr_data(new_row)

    def get_data(self, index_row, index_col, count_row, count_col):
        text = []
        for row in range(index_row, count_row + 1):
            for col in range(index_col, count_col + 1):
                item = self.item(row, col)
                if item:
                    text.append(item.text())
                text.append('\t')
            text.append('\n')
        return ''.join(text)

    def insetr_data(self, rows):
        # if self.rowCount() < len(rows) + index_row:
        #     self.setRowCount(len(rows) - 1 + index_row)
        #
        # for in_row, row in enumerate(rows):
        #     for in_col, col in enumerate(row.split('\t')):
        #         if col == '':
        #             continue
        #         item = self.item(index_row + in_row, index_col + in_col)
        #         if item is not None:
        #             item.setText(col)
        #         else:
        #             self.setItem(index_row + in_row, index_col + in_col, QTableWidgetItem(col))
        #
        # self.resizeRowsToContents()
        try:
            self.setRowCount(len(rows) - 1)
            for in_row, row in enumerate(rows):
                for in_col, col in enumerate(row.split('\t')):
                    if col == '':
                        continue
                    item = self.item(in_row, in_col)
                    if item is not None:
                        item.setText(col)
                    else:
                        self.setItem(in_row, in_col, QTableWidgetItem(col))

            self.resizeRowsToContents()
        except:
            pass

    def delete(self):
        try:
            selection = self.selectionModel()
            indexes = selection.selectedIndexes()
            if len(indexes) < 1:
                # No row selected
                return

            for idx in indexes:
                row = idx.row()
                col = idx.column()
                self.setItem(row, col, QTableWidgetItem(''))
        except:
            pass

    def insert(self):
        try:
            selection = self.selectionModel()
            indexes = selection.selectedIndexes()
            if len(indexes) < 1:
                index_row = 0
                index_col = 0
            else:
                index_row = indexes[0].row()
                index_col = indexes[0].column()

            rows = QApplication.clipboard().text().split('\n')
            if self.rowCount() < len(rows) + indexes[0].row():
                self.setRowCount(len(rows) - 1 + indexes[0].row())

            for in_row, row in enumerate(rows):
                for in_col, col in enumerate(row.split('\t')):
                    if col == '':
                        continue
                    item = self.item(index_row + in_row, index_col + in_col)
                    if item is not None:
                        item.setText(col)
                    else:
                        self.setItem(index_row + in_row, index_col + in_col, QTableWidgetItem(col))

            self.resizeRowsToContents()
        except:
            pass

    def copy(self):
        try:
            selection = self.selectionModel()
            indexes = selection.selectedIndexes()
            if len(indexes) < 1:
                # No row selected
                return

            text = ''
            for idx in indexes:
                row = idx.row()
                col = idx.column()
                item = self.item(row, col)
                if item:
                    text += item.text()
                text += '\t'
                if col == indexes[-1].column():
                    text += '\n'
            QApplication.clipboard().setText(text)
        except:
            pass


class TableWidgetCustomDrag(TableWidgetCustom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        # self.viewport().setAcceptDrops(True)
        # self.setDragEnabled(False)
        # self.setDragDropOverwriteMode(False)
        # self.setDropIndicatorShown(True)

        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event):
        md = event.mimeData().text()
        row = self.indexAt(event.pos()).row()
        column = self.indexAt(event.pos()).column()
        self.setItem(row, column, QTableWidgetItem(md))
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()


class TableWidgetCustomDrop(TableWidgetCustom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        self.setAcceptDrops(False)
        # self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.setDragEnabled(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        row = self.indexAt(self.drag_start_position).row()
        collumn = self.indexAt(self.drag_start_position).column()
        mimedata.setText(self.item(row, collumn).text())
        drag.setMimeData(mimedata)
        item = QLabel(self.item(row, collumn).text())
        item.adjustSize()

        # item.setFixedSize(100,50)
        pixmap = QtWidgets.QWidget.grab(item)
        # pixmap = QPixmap(self.size())

        painter = QPainter(pixmap)
        painter.drawPixmap(item.rect(), item.grab())
        painter.end()
        drag.setPixmap(pixmap)
        # drag.setHotSpot(event.pos())
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        # drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)


class TableSimple(TableWidgetCustom):
    def __init__(self, name):
        super().__init__()
        self.setColumnCount(len(name))  # Устанавливаем три колонки
        self.setRowCount(1)  # и одну строку в таблице
        self.setHorizontalHeaderLabels(name)
        header = self.horizontalHeader()
        for index in range(len(name)):
            header.setSectionResizeMode(index, QHeaderView.Stretch)  # Stretch)
        self.setWordWrap(True)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


class TableView(QTableView):
    def __init__(self, click_func=None):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.setWordWrap(True)
        if click_func is not None: self.clicked.connect(click_func)


class TableWidget(QTableWidget):
    def __init__(self, columns=None):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setColumnCount(columns)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.setWordWrap(True)
        self.horizontalHeader().setStretchLastSection(True)
        header = self.horizontalHeader()
        for colunm in range(columns):
            header.setSectionResizeMode(colunm, QHeaderView.ResizeToContents)  # Stretch)

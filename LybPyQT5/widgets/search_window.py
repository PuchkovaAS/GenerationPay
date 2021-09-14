from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.label import style_good
from main import resource_path


class SearchWindow(QWidget):

    def __init__(self, pages, current_row, prefix):
        super().__init__()
        self.prefix = prefix
        self.main_id = self.get_main_id(pages=pages)

        self.setWindowTitle('Кадры')
        self.setWindowIcon(QIcon(resource_path('resources/main_ico.png')))
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(['Кадры'])
        self.pages = pages
        self.current_row = current_row
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tree)

        self.importData()

        self.setLayout(layout)

        # self.tree.selectionModel().selectionChanged.connect(self.onSelectionChanged)
        self.btn = SimpleBtn(label="Принять", click_func=self.buttonClicked)

        self.tree.doubleClicked.connect(self.buttonClicked)
        # self.btn.setFixedSize(80, 30)
        layout.addWidget(self.btn)

        self.tree.collapseAll()
        self.setLayout(layout)

        self.setMinimumHeight(500)
        self.setMinimumWidth(600)

    def get_main_id(self, pages, name='Root//Кадры'):
        if self.prefix != '':
            name = f'Root//{self.prefix}'
        return pages.pages_dict_name[name][0]

    def buttonClicked(self):
        item = self.tree.currentItem()
        val = "//" + item.data(0, 0)
        while item.parent():
            item = item.parent()
            val = "//" + item.data(0, 0) + val


        self.current_row.label.setText(f'{self.pages.pages_dict_SQL[self.main_id].NAME}{val}')
        self.current_row.label.setStyleSheet(style_good)
        self.close()

    def importData(self):
        self.add_tree(parent=self.tree, id=self.main_id)

    def add_tree(self, parent, id):
        for child_id in self.pages.parent_dict[id]:
            evklass = self.pages.pages_dict_primarily[child_id]
            child = QtWidgets.QTreeWidgetItem(parent)
            child.setText(0, evklass.NAME)
            self.add_tree(parent=child, id=evklass.ID)

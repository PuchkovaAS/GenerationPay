# -*- coding: cp1251 -*-
import json
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QFileDialog, QApplication, QMessageBox

from LybPyQT5 import data_class
from LybPyQT5.widgets.button import SimpleBtn
from LybPyQT5.widgets.combobox import ComboBox
from LybPyQT5.widgets.label import InfoLabel
from LybPyQT5.widgets.line_text import LineText
from LybPyQT5.widgets.message import Message
from LybPyQT5.widgets.table import TableSimple

import qrcode
from jinja2 import FileSystemLoader, Environment
import pdfkit as pdf


class Settings:
    def __init__(self, settings_file="resource/setting.json"):
        with open(settings_file, "r", encoding="utf-8") as read_file:
            self.__dict__.update(json.load(read_file))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # base_path = os.path.abspath("/image/")
    return os.path.join(base_path, relative_path)


class Main_Window(QMainWindow):
    def __init__(self):
        # init class QMainWindow
        super().__init__()
        self.read_settings()
        self.initGUI()

    def read_style(self):
        f = open(self.setting.style_path, 'r')
        return f.read()

    def read_settings(self):
        self.setting = Settings()

    def initGUI(self):
        self.setStyleSheet(self.read_style())
        self.setWindowIcon(QIcon(resource_path(self.setting.path_png)))
        # self.setMinimumWidth(1000)
        self.setWindowTitle("Генератор квитанций")
        self.setMinimumHeight(800)
        self.table = TableSimple(["Учащиеся"])
        main_layout = QGridLayout()
        central_widget = QWidget(self)  # Создаём центральный виджет

        mounth = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                  'Ноябрь', 'Декабрь']

        self.combo_month = ComboBox(line=mounth)

        self.Year = LineText(text='2021', tooltip='Год обучения')
        self.Group = LineText(text='Малышок 1', tooltip='Группа')
        self.Summ_Rub = LineText(text='800', tooltip='рублей')
        self.Summ_Koop = LineText(text='00', tooltip='копеек')

        main_layout.addWidget(self.table, 0, 0, 20, 1)
        main_layout.addWidget(InfoLabel('Месяц'), 0, 11, 1, 2)
        main_layout.addWidget(self.combo_month, 1, 11, 1, 2)
        main_layout.addWidget(InfoLabel('Год'), 0, 13, 1, 2)
        main_layout.addWidget(self.Year, 1, 13, 1, 2)
        main_layout.addWidget(InfoLabel('Группа'), 2, 11, 1, 4)
        main_layout.addWidget(self.Group, 3, 11, 1, 4)
        #
        main_layout.addWidget(InfoLabel('Сумма'), 4, 11, 1, 4)
        main_layout.addWidget(self.Summ_Rub, 5, 11, 1, 2)
        main_layout.addWidget(self.Summ_Koop, 5, 13, 1, 2)

        forming_button = SimpleBtn(label="Сформировать", click_func=self.forming)

        main_layout.addWidget(forming_button, 13, 11, 1, 4)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

    def forming(self):
        Rub = self.Summ_Rub.text()
        Cop = self.Summ_Koop.text()
        group = self.Group.text()

        data = f"за {self.combo_month.currentText().lower()} {self.Year.text()}г."

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить pdf", "", "pdf (*.pdf)", options=options)

        if fileName == '':
            return

        if fileName.find('.pdf') == -1:
            fileName += '.pdf'

        env = Environment(loader=FileSystemLoader(self.setting.path_resourse))
        template_table = env.get_template(self.setting.path_table_shablon)
        env1 = Environment(loader=FileSystemLoader(self.setting.path_resourse))
        template_shablon = env1.get_template(self.setting.path_shablon)

        with open(self.setting.path_intermediate, "w", encoding='windows-1251') as f:
            row = 0
            list_html = []
            list_child = [self.table.item(row, 0).text() for row in range(self.table.rowCount())]
            for name in list_child:
                data_all = data_class.Data_html(name, Rub, Cop, group, data, setting=self.setting)

                qr = qrcode.QRCode(
                    version=1,
                    box_size=15,
                    border=5,
                )
                qr_data = f"""ST00012|Name={self.setting.Name}|PersonalAcc={self.setting.PersonalAcc}|BankName={self.setting.BankName}|BIC={self.setting.BIC}|CorrespAcc={self.setting.CorrespAcc}|PayeeINN={self.setting.PayeeINN}|KPP={self.setting.KPP}|LASTNAME={data_all.name}|payerAddress={self.setting.payerAddress}|Purpose={self.setting.Purpose} {data_all.data.upper()}|CBC={self.setting.CBC}|OKTMO={self.setting.OKTMO}|Sum={data_all.Rub}{data_all.Cop}"""

                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                img.save(f'{self.setting.path_image}/{row}.png')
                data_all.set_pict(f'{self.setting.path_imageHTML}/{row}')
                list_html.append(str(template_table.render(data=data_all)))
                row += 1

            f.write(template_shablon.render(table=list_html))

        with open(fileName, 'w') as f:
            options = {
                "enable-local-file-access": None
            }
            config = pdf.configuration(wkhtmltopdf=self.setting.path_wkhtmltopdf)
            try:
                pdf.from_file(self.setting.path_intermediate, fileName, configuration=config, options=options)
                new_mess = Message(title="Сообщение", text="Сгенерирован успешно", icon=QMessageBox.Information)

            except Exception as e:
                print(e)
                new_mess = Message(title="Сообщение", text=e, icon=QMessageBox.Warning)
            retval = new_mess.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = Main_Window()
    root.show()
    sys.exit(app.exec_())

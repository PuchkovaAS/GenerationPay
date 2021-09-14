class Data_html():
    """docstring for Data_html"""

    def __init__(self, name="Пучкова Анастасия Сергеевна", Rub="800", Cop="00", group="1\"", data="за октябрь 2019г.", setting=None):
        self.setting = setting
        self.name = name
        self.Rub = str(Rub)
        self.Cop = str(Cop)
        list_data = group.split(' ')
        if len(list_data) == 1:
            list_data.append('')

        self.data = list_data[1] + " " + data
        self.pict = ''

        self.organiz = list_data[0]

    def set_pict(self, pict):
        self.pict = pict

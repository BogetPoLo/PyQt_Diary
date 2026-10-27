from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QTableWidgetItem

from Data_File import DateBase


class ConnectingLinkAddClass:
    """Класс является связующим звеном для main и data и реализует методы для AddClass"""

    def __init__(self, interface, mes):
        self.interface = interface
        self.mes = mes
        self.db = DateBase()
        self.res_file = None

    def save_txt_or_csv_file(self):
        self.res_file = self.mes.open_txt_or_csv()

    def Checking_correctness_record(self):
        """Проверка на правильность указанных аргументов"""
        try:
            name_class = self.interface.name_class_line.text()
            if self.interface.type_file_txt.isChecked() or self.interface.type_file_csv.isChecked():  # Проверка,
                # что пользователь нажал на кнопку
                if len(name_class) != 0:
                    if len(name_class) in [2, 3] and ord(name_class[-1].upper()) in range(1040, 1072) and int(
                            name_class[0:-1]) in range(1, 12):  # Проверяет правильность написания имени класса
                        if self.res_file is None:  # Проверка, что пользователь открыл файл
                            self.mes.error_information("Ошибка файла", "Вы не выбрали файл")
                        elif self.res_file is False:  # Проверка, что в класс <= 30 учеников
                            self.mes.error_information("Ошибка класса", "Максимальное количество учеников - 30 человек")
                        else:
                            self.output_new_name_tab(name_class)  # Загружаем имена и номер класса в таблицу
                    else:
                        raise ValueError()  # Ошибка
                else:
                    self.mes.error_information("Ошибка имени класса", "Вы не указали имя класса.")  # Ошибка
            else:
                self.mes.error_information("Ошибка типа файлы", "Вы не выбрали файл txt/csv.")  # Ошибка
        except ValueError:
            self.mes.error_critical("Ошибка имени класса",
                                    "Такого класса не может быть. Можно использовать только буквы русского"
                                    " алфавита от A до Я и цифры от 1 до 11")  # Ошибка

    def output_new_name_tab(self, name_class):
        """Заполняем таблицу именами"""
        """Отчищаем таблицу"""
        self.del_info_table()

        """Количество ячеек"""
        self.interface.table_widget_add.setRowCount(31)
        self.interface.table_widget_add.setColumnCount(1)

        """Заполняем таблицу"""
        item = QTableWidgetItem(name_class)
        self.interface.table_widget_add.setItem(0, 0, item)

        for i, row in enumerate(self.res_file):
            item = QTableWidgetItem(row)
            self.interface.table_widget_add.setItem(i + 1, 0, item)

        """Устанавливаем размер таблицы"""
        self.interface.table_widget_add.setColumnWidth(0, 1400)

        item = self.interface.table_widget_add.item(0, 0)
        item.setBackground(QBrush(QColor(20, 200, 255)))

        """Устанавливаем цвет для ячеек"""
        for i in range(1, 31):
            item = self.interface.table_widget_add.item(i, 0)
            if item is None:
                item = QTableWidgetItem("")
                item.setBackground(QBrush(QColor(153, 230, 255)))
            else:
                item.setBackground(QBrush(QColor(153, 230, 255)))
            self.interface.table_widget_add.setItem(i, 0, item)

    def final_file_upload(self):
        """Загружаем новый класс в бд"""

        if self.interface.table_widget_add.rowCount() == 0:
            self.mes.error_warning("Ошибка вывода", "Надо обязательно проверить таблицу учеников.")
        else:
            name_class = None  # Имя класса
            all_names = []  # фио всех новых учеников

            """Записываем из table_widget_add"""
            for row in range(self.interface.table_widget_add.rowCount()):
                item = self.interface.table_widget_add.item(row, 0)
                if row == 0:
                    name_class = item.text().upper()
                elif item is not None:
                    all_names.append(item.text())

            """Передаём в бд"""
            res = self.db.load_new_class_and_student(name_class, all_names)
            if res is False:  # Проверяем что такого класса нет
                self.mes.error_warning("Ошибка класса", "Такой класса уже существует.")
            else:  # Добавляем новый класс в comboBox
                self.interface.class_combo.addItem(name_class.upper())

    def canceling_new_class(self):
        """Отмена нового класса (убираем галочку с radioButton, удаляем всё из table_widget_add,
         стираем номер класса и можно загрузить класс)"""
        self.interface.type_file_txt.setChecked(False)
        self.interface.type_file_csv.setChecked(False)
        self.interface.open_file_button.setEnabled(True)
        self.interface.name_class_line.clear()
        self.res_file = None  # убираем файл

        self.del_info_table()  # Отчищаем таблицу

    def del_info_table(self):
        """Метод удаляет всё из таблицы"""
        self.interface.table_widget_add.clear()
        self.interface.table_widget_add.setRowCount(0)
        self.interface.table_widget_add.setColumnCount(0)

    def add_one_student(self):
        """Метода добавляет нового ученика в определённый класс"""
        name_st = self.interface.name_student_line.text()
        name_cl = self.interface.ins_name_class_line.text()

        if len(name_cl) == 0:
            self.mes.error_warning("Ошибка класса", "Вы не указали класс")
        elif len(name_st.split()) != 3:  # Проверяем что передали полное фио
            self.mes.error_warning("Ошибка ФИО", "Нужно писать полностью ФИО")
        elif not (all([1 for i in self.db.all_class() if name_cl in i])):  # Проверяем что такой класс есть
            self.mes.error_warning("Ошибка Класса", "Такого класса нет")
        elif any([1 for i in self.db.getting_names(name_cl) if name_st in i]):  # Проверяем что такой ученик существует
            self.mes.error_warning("Ошибка ФИО", "Такой ученик уже существует")
        else:
            self.db.add_new_student_to_sql(name_cl, name_st)  # Загружаем в бд
            self.del_table_diary()

    def new_full_name_student(self):
        """Метод изменяем фио ученика"""
        name_st = self.interface.name_student_line.text()
        name_cl = self.interface.ins_name_class_line.text()
        new_name_st = self.interface.new_student.text()

        if len(name_cl) == 0:
            self.mes.error_warning("Ошибка класса", "Вы не указали класс")
        elif len(name_st.split()) != 3:  # Проверяем что передали полное фио
            self.mes.error_warning("Ошибка ФИО", "Нужно писать полностью ФИО")
        elif len(new_name_st.split()) != 3:  # Проверяем что передали полное старое имя
            self.mes.error_warning("Ошибка ФИО", "Нужно писать полностью ФИО")
        elif not (all([1 for i in self.db.all_class() if name_cl in i])):  # Проверяем что такой класс есть
            self.mes.error_warning("Ошибка Класса", "Такого класса нет")
        elif 1 not in [1 for i in self.db.getting_names(name_cl) if
                       name_st in i]:  # Проверяем что такого ученик существует
            self.mes.error_warning("Ошибка ФИО", "Такого ученика нет")
        else:
            self.db.new_full_name_to_sql(name_cl, new_name_st, name_st)
            self.del_table_diary()

    def del_table_diary(self):
        self.interface.table_widget.clear()
        self.interface.table_widget.clearContents()
        self.interface.table_widget.setRowCount(0)
        self.interface.table_widget.setColumnCount(0)
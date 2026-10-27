import calendar
from datetime import date
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QTableWidgetItem
from Data_File import DateBase


class ConnectingLinkDiary:
    """Класс является связующим звеном для main и data и реализует методы для Diary"""

    def __init__(self, interface, mes):
        self.interface = interface
        self.mes = mes
        self.db = DateBase()
        self.defining_the_days_in_a_month()

    def defining_the_days_in_a_month(self):
        """Определяем количество дней и формируем список дней"""
        now = date.today()
        self.day = now.day
        self.year = now.year
        self.month = now.month
        self.formatted_date = now.strftime("%d.%m.%Y").split(".")
        self.db.old_work_to_sql(self.formatted_date)
        self.determine_type_day(self.year, self.month)
        self.list_mont_year = []  # Список учебных месяцев

        for ye in range(self.year, self.year + 2):
            for mon in range(1, 12 + 1):
                if mon < 10:
                    self.list_mont_year.append(f"{"0" + str(mon)}.{ye}")
                else:
                    self.list_mont_year.append(f"{mon}.{ye}")
        self.list_mont_year = self.list_mont_year[8:17]

    def determine_type_day(self, year, month):
        """Метод определяет выходные, прошедшие дни, будущие дни"""
        self.count_day_now = calendar.monthrange(year, month)  # Определяет дни

        """Определяем выходные - 2, прошедшие дни - 1 и будущие дни - 0"""
        self.sorted_list_day = []
        for d in range(1, self.count_day_now[1] + 1):
            current_date = date(year, month, d)
            if current_date.weekday() >= 5:
                self.sorted_list_day.append(2)
            elif self.year >= year and self.month > month or (self.month == month and d <= int(self.formatted_date[0])):
                self.sorted_list_day.append(1)
            else:
                self.sorted_list_day.append(0)

    def output_name_in_table_widget(self):  # Надо добавить вывод оценок, работ, и цвета под дни и события
        """Метод реализует загрузку имён определённого класса"""
        text = self.interface.class_combo.currentText()
        selected_date = self.interface.data_combo.currentText()

        # Вызови метод determine_type_day и указывай аргументы годы который выбрали
        month, year = selected_date.split(".")
        self.determine_type_day(int(year), int(month))

        self.interface.table_widget.clear()
        if text == "-":  # Полностью удаляет все из таблицы, так как ничего не выбрано
            self.deleting_all_data_from_the_table()  # Полностью удаляем всё из таблицы
        else:  # Заполняет таблицу именами учеников определённого класса
            self.deleting_all_data_from_the_table()  # Полностью удаляем всё их таблицы и заполняем её новыми данными

            heading = ["ФИО"] + [str(i) for i in range(1, self.count_day_now[1] + 1)]
            all_student = self.db.getting_names(text)
            # Сортировка имён по Фамилии, Имени, Отчеству
            all_student = sorted(all_student, key=lambda x: (x[0].split()[0], x[0].split()[1], x[0].split()[2]))

            """Количество столбцов и строк и заголовки"""
            self.interface.table_widget.setRowCount(len(all_student))
            self.interface.table_widget.setColumnCount(len(heading))
            self.interface.table_widget.setHorizontalHeaderLabels(heading)

            """Заполнение таблицы"""
            for i, row in enumerate(all_student):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(val)
                    self.interface.table_widget.setItem(i, j, item)

            """Размер таблицы"""
            self.interface.table_widget.setColumnWidth(0, 200)
            for i in range(1, len(heading)):
                self.interface.table_widget.setColumnWidth(i, 20)

            """Запрашиваем размер таблицы"""
            rows = self.interface.table_widget.rowCount()
            columns = self.interface.table_widget.columnCount()

            for i in range(rows):
                item = self.interface.table_widget.item(i, 0)
                item.setBackground(QBrush(QColor(153, 230, 255)))

            """Запрашиваем и заполняем пропуски"""
            attendance = self.db.getting_attendance(text)
            self.output_text_in_table(attendance, rows)

            """Запрашиваем и заполняем оценки"""
            estimation = self.db.getting_estimation_class(text)
            self.output_text_in_table(estimation, rows)

            cw, iw, lw, hw = self.db.getting_task_class(text)
            self.output_task_in_text_browser(cw, iw, lw, hw)

            for i in range(rows):  # Заполняет поля цветом
                for j in range(1, columns):
                    item = self.interface.table_widget.item(i, j)
                    self.changing_the_color(item, i, j)

    def deleting_all_data_from_the_table(self):
        """Метод полностью удаляет всё их таблицы"""
        self.interface.table_widget.clearContents()
        self.interface.table_widget.setRowCount(0)
        self.interface.table_widget.setColumnCount(0)

    def output_text_in_table(self, values, rows):
        """Функция заполняет таблицу Н-ками и оценками"""
        month, year = self.interface.data_combo.currentText().split(".")  # для проверки месяца и года

        for row in range(rows):
            item = self.interface.table_widget.item(row, 0)
            for full_name in values:
                if item.text() == full_name:
                    for val in values[full_name]:
                        ind, check_mon, check_ye = val[1].split(".")
                        if month == check_mon and year == check_ye:
                            desired_cell = self.interface.table_widget.item(row, int(ind))
                            if desired_cell is not None:
                                res_item = QTableWidgetItem(desired_cell.text() + str(val[0]))
                            else:
                                res_item = QTableWidgetItem(str(val[0]))
                            self.interface.table_widget.setItem(row, int(ind), res_item)

    def output_task_in_text_browser(self, cw, iw, lw, hw):
        """Метод заполняет TextBrowser заданиями для класса"""
        res_html = "<ul>"
        if cw == iw == lw == hw:
            self.interface.output_work.setHtml("""<span style="font-size:30pt;"><b>Ура! Работ нет.</b></span>""")
        else:
            res_html += """<li><span style="color:#DC143C; font-size:15pt;"><b>Контрольные работы</b></span></li>"""
            if cw == []:
                res_html += """<span style="font-size:12pt"><i>Ура, контрольных работ нет!</i></span><br>"""
            else:
                for work in cw:
                    res_html += f"""<span style="font-size:12pt"><i>Дата: {work[1]} Комментарий: {work[0]}
                    </i></span><br>"""

            res_html += """<li><span style="color:#FF8C00; font-size:15pt;"><b>Самостоятельные работы</b>
            </span></li>"""
            if iw == []:
                res_html += """<span style="font-size:12pt"><i>Ура, самостоятельных работ нет!</i></span>"""
            else:
                for work in iw:
                    res_html += f"""<span style="font-size:12pt"><i>Дата: {work[1]} Комментарий: {work[0]}
                    </i></span><br>"""

            res_html += """<li><span style="color:#9400D3; font-size:15pt;"><b>Лабораторные работы</b></span></li>"""
            if lw == []:
                res_html += """<span style="font-size:12pt"><i>Ура, лабораторных работ нет!</i></span>"""
            else:
                for work in lw:
                    res_html += f"""<span style="font-size:12pt"><i>Дата: {work[1]} Комментарий: {work[0]}
                    </i></span><br>"""

            res_html += """<li><span style="color:#008000; font-size:15pt;"><b>Домашние работы</b></span></li>"""
            if hw == []:
                res_html += """<span style="font-size:12pt"><i>Ура, Домашних работ нет!</i></span><br>"""
            else:
                for work in hw:
                    res_html += f"""<span style="font-size:12pt"><i>Дата: {work[1]} Комментарий: {work[0]}
                    </i></span><br>"""

            res_html += "</ul>"

            self.interface.output_work.setHtml(res_html)

    def ind_cell(self, rows, column):
        """Функция получает индексы ячейки в которой один раз нажали мышкой"""
        self.index_rows = rows
        self.index_column = column

    def output_new_estimation_and_write_sql(self):
        """Функция вставляет в таблицу оценку для конкретного ученика и добавляет в базу данных"""

        month, year = self.interface.data_combo.currentText().split(".")
        name_class = self.interface.class_combo.currentText()  # имя класса

        try:
            if ((self.day >= self.index_column and self.month == int(month) and self.year == int(year)) or (
                    self.month > int(month) and self.year >= int(year))) and self.sorted_list_day[
                self.index_column - 1] != 2:  # проверяем, что дата на которую ставят оценку или, уже была или нынешняя
                """Вывод в таблицу"""
                value = self.interface.estimation_spin.value()  # Оценка
                item = self.interface.table_widget.item(self.index_rows, self.index_column)
                if item is not None:
                    sorted_data = "".join(sorted(item.text() + str(value), reverse=True))
                    item = QTableWidgetItem(sorted_data)
                else:
                    item = QTableWidgetItem(str(value))

                name = self.interface.table_widget.item(self.index_rows, 0).text()  # имя ученика
                type_work = self.interface.type_work_estimation_combo.currentText()  # тип работы
                photo_est = self.mes.dialog_photo(type_work, name)  # загружаем фото (если пользователь захочет)

                self.changing_the_color(item, self.index_rows, self.index_column)
                self.interface.table_widget.setItem(self.index_rows, self.index_column, item)

                """Добавление в базу данных"""
                month_year = self.interface.data_combo.currentText()  # месяц и год
                comment = self.interface.comment_estimation_plain.toPlainText()  # Комментарий к оценке
                data_es = f"{self.index_column:02d}.{month_year}"
                self.db.add_estimation_to_sql(value, name, data_es, type_work, name_class, comment, photo_est)
            else:
                self.mes.error_information("Невозможное действие",
                                        "Нельзя устанавливать оценки или Н-ки на выходные или будущий день.")  # Ошибка
        except AttributeError:
            if name_class == "-":
                self.mes.error_critical("Ошибка класса", "Вы не выбрали класс.")  # Ошибка
            else:
                self.mes.error_critical("Недостаточно аргументов",
                                        "Вы не выбрали ячейку, в которую надо вставить оценку или Н-ку.")  # Ошибка

    def output_new_attendance_and_write_sql(self):
        """Функция вставляет в таблицу Н-ки для конкретного ученика и добавляет в базу данных"""
        month, year = self.interface.data_combo.currentText().split(".")
        name_class = self.interface.class_combo.currentText()  # имя класса
        try:
            if ((self.day >= self.index_column and self.month == int(month) and self.year == int(year)) or (
                    self.month > int(month) and self.year >= int(year))) and self.sorted_list_day[
                self.index_column - 1] != 2:  # проверяем, что дата на которую ставят оценку или, уже была или нынешняя
                """Вывод в таблицу"""
                item = self.interface.table_widget.item(self.index_rows, self.index_column)
                if item is not None and "Н" in item.text():
                    self.mes.error_warning("Действие уже выполнено",
                                           "Нельзя выставлять две Н-ки на одну дату для одного ученика")  # Ошибка
                elif item is not None:
                    sorted_data = "".join(sorted(item.text() + "Н", reverse=True))
                    item = QTableWidgetItem(sorted_data)
                else:
                    item = QTableWidgetItem("Н")
                self.changing_the_color(item, self.index_rows, self.index_column)
                self.interface.table_widget.setItem(self.index_rows, self.index_column, item)

                """Добавление в базу данных"""
                name = self.interface.table_widget.item(self.index_rows, 0).text()  # имя ученика
                month_year = self.interface.data_combo.currentText()  # месяц и год
                data_att = f"{self.index_column:02d}.{month_year}"
                self.db.add_new_attendance_to_sql(name, name_class, data_att)
            else:
                self.mes.error_information("Невозможное действие",
                                        "Нельзя устанавливать оценки или Н-ки на выходные или будущий день.")  # Ошибку
        except AttributeError:
            if name_class == "-":
                self.mes.error_critical("Ошибка класса", "Вы не выбрали класс.")  # Ошибка
            else:
                self.mes.error_critical("Недостаточно аргументов",
                                        "Вы не выбрали ячейку, в которую надо вставить оценку или Н-ку.")  # Ошибка

    def output_new_task_and_write_sql(self):
        """Функция записывает новое задание в QBrowserText и добавляет в базу данных"""
        month, year = self.interface.data_combo.currentText().split(".")
        name_class = self.interface.class_combo.currentText()  # номер класса
        try:
            type_work = self.interface.type_work_assignment_combo.currentText()  # тип работы
            comment = self.interface.comment_assignment_plaint.toPlainText()  # комментарий к работе
            day = self.interface.data_line.text()
            data_task = f"{int(day):02d}.{month}.{year}"

            if name_class == "-":  # Проверяем что выбрали класс
                self.mes.error_critical("Ошибка класса", "Вы не выбрали класс.")  # Ошибка
                return 0
            elif int(day) < 0:  # Проверяет что дата не отрицательна
                self.mes.error_warning("Ошибка даты", "День не может быть отрицательным.")  # Ошибка
                return 0
            elif self.sorted_list_day[int(day) - 1] != 0:  # Проверяет, что задание ставиться на будущий день
                self.mes.error_warning("Ошибка даты",
                                       "Нельзя назначать работы на выходные, прошедшие и сегодняшний день.")  # Ошибка
                return 0

            cw, iw, lw, hw = self.db.getting_task_class(name_class)
            # Проверяем, что такой работы не существует
            if type_work == "Контрольная работа" and data_task in [i[-1] for i in cw]:
                self.mes.error_warning("Ошибка назначения", "Такая работа/задание уже существует.")  # Ошибка
            elif type_work == "Самостоятельная работа" and data_task in [i[-1] for i in cw]:
                self.mes.error_warning("Ошибка назначения", "Такая работа/задание уже существует.")  # Ошибка
            elif type_work == "Лабораторная работа" and data_task in [i[-1] for i in cw]:
                self.mes.error_warning("Ошибка назначения", "Такая работа/задание уже существует.")  # Ошибка
            elif type_work == "Домашняя работа" and data_task in [i[-1] for i in cw]:
                self.mes.error_warning("Ошибка назначения", "Такая работа/задание уже существует.")  # Ошибка
            else:
                # Загружаем в бд
                if comment == "":
                    comment = "Отсутствует"
                self.db.add_new_word_to_sql(type_work, comment, data_task, name_class)
                cw, iw, lw, hw = self.db.getting_task_class(name_class)
                self.output_task_in_text_browser(cw, iw, lw, hw)

        except IndexError:
            self.mes.error_warning("Ошибка даты", f"Такого дня не существует в {month} месяце.")  # Ошибку
        except ValueError:
            if name_class == "-":
                self.mes.error_critical("Ошибка класса", "Вы не выбрали класс.")  # Ошибка
            else:
                self.mes.error_warning("Ошибка даты", "Некорректная дата.")  # Ошибку

    def output_info_estimation(self, row, column):
        """Метод должен выводить информацию про оценку ученика"""
        if column == 0:
            return 0
        else:
            item = self.interface.table_widget.item(row, column)
            name = self.interface.table_widget.item(row, 0).text()  # Имя ученика
            name_class = self.interface.class_combo.currentText()  # номер класса
            day = self.interface.table_widget.horizontalHeaderItem(column).text()  # день
            mon_yea = self.interface.data_combo.currentText()  # месяц и код оценки
            date_est = f"{int(day):02d}.{mon_yea}"

            if item is not None and any([1 for score in "2345" if score in item.text()]):
                ests = self.db.getting_estimation_for_student(name_class, name,
                                                              date_est)  # Информация об оценке/ах ученика
                self.mes.output_dialog_estimation(ests)
            else:
                self.mes.error_information("Отсутствует аргумент", "В этой ячейке нет оценки.")

    def changing_the_color(self, item, row, col):
        """Метод заполняет цветами таблицу
        выходные - 2
        прошедшие дни - 1
        будущие дни - 0"""
        if item is None:
            item = QTableWidgetItem("")
            if self.sorted_list_day[col - 1] == 2:
                item.setBackground(QBrush(QColor(200, 255, 200)))
            elif self.sorted_list_day[col - 1] == 0:
                item.setBackground(QBrush(QColor(220, 230, 255)))
            elif self.sorted_list_day[col - 1] == 1:
                item.setBackground(QBrush(QColor(253, 250, 180)))
        elif item is not None:
            if self.sorted_list_day[col - 1] == 2:
                item.setBackground(QBrush(QColor(200, 255, 200)))
            elif self.sorted_list_day[col - 1] == 0:
                item.setBackground(QBrush(QColor(220, 230, 255)))
            elif self.sorted_list_day[col - 1] == 1:
                item.setBackground(QBrush(QColor(253, 250, 180)))
        self.interface.table_widget.setItem(row, col, item)
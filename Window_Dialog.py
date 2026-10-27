import csv

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, \
    QScrollArea, QWidget, QTextBrowser
from PyQt6.QtCore import Qt


class MyMessage:
    def __init__(self, parent):
        self.parent = parent  # Ссылка на родительское окно

    def error_information(self, title, text_error):
        """Информационная ошибка"""
        error_att_est_mes = QMessageBox(self.parent)
        error_att_est_mes.setIcon(QMessageBox.Icon.Information)
        error_att_est_mes.setWindowTitle(title)
        error_att_est_mes.setText(text_error)
        error_att_est_mes.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_att_est_mes.exec()

    def error_critical(self, title, text_error):
        """Критическая ошибка"""
        error_cell_mes = QMessageBox(self.parent)
        error_cell_mes.setIcon(QMessageBox.Icon.Critical)
        error_cell_mes.setWindowTitle(title)
        error_cell_mes.setText(text_error)
        error_cell_mes.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_cell_mes.exec()

    def error_warning(self, title, text_error):
        """Предупреждающая ошибка"""
        error_worth_mes = QMessageBox(self.parent)
        error_worth_mes.setIcon(QMessageBox.Icon.Warning)
        error_worth_mes.setWindowTitle(title)
        error_worth_mes.setText(text_error)
        error_worth_mes.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_worth_mes.exec()

    def output_dialog_estimation(self, ests):
        """Диалог открывается при двойном нажатии на ячейку с оценкой и предлагает посмотреть все оценки за эту дату"""
        my_dialog = QDialog(self.parent)
        my_dialog.setFixedSize(500, 500)
        my_dialog.setWindowTitle("Информация об оценке")

        # Создание основного layout
        main_layout = QVBoxLayout(my_dialog)

        # Создание QScrollArea
        scroll_area = QScrollArea(my_dialog)
        scroll_area.setWidgetResizable(True)

        # Виджет для контента
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)  # отступы у поля

        # Добавление информации об оценках
        for i, est in enumerate(ests):
            score, work_type, comment, photo_data = est

            # Создание виджета для одной оценки
            est_widget = QWidget()
            est_layout = QVBoxLayout(est_widget)
            est_layout.setSpacing(5)

            # Оценка и тип работы
            info_layout = QHBoxLayout()
            label_con = QLabel(f"Оценка {i + 1}:", est_widget)
            label_score = QLabel(f"{score}", est_widget)
            label_work_type = QLabel(f"({work_type})", est_widget)

            info_layout.addWidget(label_con)
            info_layout.addWidget(label_score)
            info_layout.addWidget(label_work_type)
            info_layout.addStretch()

            est_layout.addLayout(info_layout)

            # Комментарий
            if comment:
                label_comment = QTextBrowser(est_widget)
                label_comment.setFixedSize(440, 60)
                label_comment.setText(comment)
                est_layout.addWidget(label_comment)

            # Фотография
            if photo_data:
                pixmap = QPixmap()
                pixmap.loadFromData(photo_data)
                if not pixmap.isNull():
                    # Увеличиваем размер фотографии
                    pixmap = pixmap.scaled(450, 300, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                    photo_label = QLabel(est_widget)
                    photo_label.setPixmap(pixmap)
                    photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    est_layout.addWidget(photo_label)
                else:
                    error_label = QLabel("Не удалось загрузить фотографию.", est_widget)
                    est_layout.addWidget(error_label)
            else:
                no_photo_label = QLabel("Фотография отсутствует.", est_widget)
                est_layout.addWidget(no_photo_label)

            # Разделительная линия
            line = QLabel(est_widget)
            line.setFixedHeight(1)
            line.setStyleSheet("background-color: #CCCCCC; margin-top: 10px; margin-bottom: 10px;")
            est_layout.addWidget(line)

            content_layout.addWidget(est_widget)

        # Установка виджета в QScrollArea
        scroll_area.setWidget(content_widget)

        # Добавление QScrollArea в основной layout
        main_layout.addWidget(scroll_area)

        # Кнопка для закрытия диалога
        close_button = QPushButton("Закрыть", my_dialog)
        close_button.clicked.connect(my_dialog.close)
        close_button.setFixedHeight(30)
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

        my_dialog.exec()

    def dialog_photo(self, type_work, full_name):
        """Диалог предлагает пользователю выбрать фото"""
        dialog_save_photo = QDialog(self.parent)
        dialog_save_photo.setFixedSize(500, 100)
        dialog_save_photo.setWindowTitle("Загрузка фото")
        com_layout = QVBoxLayout(dialog_save_photo)
        lab = QLabel(f"Хотите загрузить фото {type_work} для {full_name}?")
        com_layout.addWidget(lab)

        no_button = QPushButton("Нет", dialog_save_photo)
        yes_button = QPushButton("Да", dialog_save_photo)

        no_button.clicked.connect(dialog_save_photo.reject)
        yes_button.clicked.connect(dialog_save_photo.accept)

        com_layout.addWidget(no_button)
        com_layout.addWidget(yes_button)

        result = dialog_save_photo.exec()

        if result == QDialog.DialogCode.Accepted:
            return self.open_photo(type_work, full_name)
        elif result == QDialog.DialogCode.Rejected:
            return None

    def open_photo(self, type_work, full_name):
        """Открывает диалог выбора файла и сохраняет фотографию в бинарном виде"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Выберите фотографию",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)"
        )

        if file_path:
            with open(file_path, "rb") as file:
                photo = file.read()  # Сохраняем данные в бинарном виде
                return self.test_output_photo(photo, type_work, full_name)
        else:
            return None

    def test_output_photo(self, photo, type_work, full_name):
        """Диалог показывает пользователю какую фотку он загрузил"""
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Просмотр фотографии")

        layout = QVBoxLayout(dialog)

        if photo:
            pixmap = QPixmap()
            pixmap.loadFromData(photo)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(700, 700, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)  # устанавливаем размер изображения
                dialog.setMinimumSize(pixmap.width(), pixmap.height())

                photo_label = QLabel(dialog)
                photo_label.setPixmap(pixmap)
                layout.addWidget(photo_label)
            else:
                error_label = QLabel("Не удалось загрузить фотографию.", dialog)
                layout.addWidget(error_label)

            yes_button = QPushButton("Подтвердить", dialog)
            no_button = QPushButton("Отмена", dialog)

            no_button.clicked.connect(dialog.reject)
            yes_button.clicked.connect(dialog.accept)

            layout.addWidget(yes_button)
            layout.addWidget(no_button)

        else:
            error_label = QLabel("Фотография отсутствует.", dialog)
            layout.addWidget(error_label)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return photo
        elif result == QDialog.DialogCode.Rejected:
            self.dialog_photo(type_work, full_name)

    def open_txt_or_csv(self):
        """Открытие диалога для выбора фала"""
        if self.parent.type_file_txt.isChecked():
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Открыть файл",
                "",
                "Text Files (*.txt);;All Files (*)"
            )

            if file_path:
                self.parent.open_file_button.setEnabled(False)

                """ФИО учеников должны быть записаны через ;"""
                with open(file_path, mode="r", encoding="utf-8") as f:
                    res_list = []

                    line = f.readline()
                    while line:
                        for word in line.split(";"):
                            if word not in res_list and word != "\n":
                                res_list.append(word)
                        line = f.readline()

                if len(res_list) <= 30:
                    return sorted(res_list, key=lambda x: (x.split()[0], x.split()[1], x.split()[2]))
                return False
            return None

        elif self.parent.type_file_csv.isChecked():
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Открыть файл",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )

            if file_path:
                self.parent.open_file_button.setEnabled(False)

                """ФИО учеников должны быть записаны через ;"""
                res_list = []
                with open(file_path, mode="r", encoding="utf-8") as f:
                    line = csv.reader(f, delimiter=";")

                    for row in line:
                        row = " ".join(row)
                        if row not in res_list:
                            res_list.append(row)

                if len(res_list) <= 30:
                    return sorted(res_list, key=lambda x: (x.split()[0], x.split()[1], x.split()[2]))
                return False
            return None
        else:
            self.error_critical("Ошибка типа файлы", "Вы не выбрали файл txt/csv.")
            return None

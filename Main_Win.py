from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QHBoxLayout, QTableWidget, QVBoxLayout, \
    QGroupBox, QFormLayout, QSpinBox, QComboBox, QPushButton, QPlainTextEdit, QRadioButton, QLineEdit, \
    QTextBrowser
from Data_File import DateBase
from Control_Diary import ConnectingLinkDiary
from Contral_Add_Class import ConnectingLinkAddClass
from Window_Dialog import MyMessage
from Contol_help import setup_help_tab


class ApplicationInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DateBase()
        self.mes = MyMessage(self)
        self.con_link_diary = ConnectingLinkDiary(self, self.mes)
        self.con_link_add_cl = ConnectingLinkAddClass(self, self.mes)
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 100, 1000, 700)
        self.setWindowTitle("Электронный дневник")

        # Центральный виджет с вкладками для дневника
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # --- Вкладка "Дневник" ---
        self.tab_diary = QWidget()
        self.setup_diary_tab()
        self.tab_widget.addTab(self.tab_diary, "Дневник")

        # --- Вкладка "Добавление нового класса" ---
        self.tab_add_class = QWidget()
        self.setup_add_class_tab()
        self.tab_widget.addTab(self.tab_add_class, "Добавление/Изменение нового класса")

        # --- Вкладка "Помощь" ---
        self.tab_help = QWidget()
        self.setup_help_tab()
        self.tab_widget.addTab(self.tab_help, "Помощь")

    def setup_diary_tab(self):
        """Метод создаёт интерфейс для вкладки 'Дневник'"""
        # Основной компоновщик для вкладки "Дневник"
        layout_diary = QHBoxLayout(self.tab_diary)

        # --- Левая часть: Таблица (Колонка 1: ФИО, остальные колонки: дни недели) и поле для работ ---
        left_widget = QWidget()
        self.left_layout = QVBoxLayout(left_widget)
        self.make_table_widget()
        self.make_work_text()

        # --- Правая часть: Группа виджетов (Выставление оценок, назначение работ, проверка посещаемости)
        right_widget = QWidget()
        self.right_layout = QVBoxLayout(right_widget)

        self.gr_class = QGroupBox("Класс")
        self.form_layout_class = QFormLayout(self.gr_class)
        self.make_class()

        # Группа "Оценка"
        self.estimation = QGroupBox("Оценка")
        self.form_layout_estimation = QFormLayout(self.estimation)
        self.make_group_estimation()

        # Группа "Назначение работ"
        self.assignment_works = QGroupBox("Назначение работ")
        self.form_layout_assignment_works = QFormLayout(self.assignment_works)
        self.make_group_assignment_works()

        # Группа "Посещаемость"
        self.attendance = QGroupBox("Посещаемость")
        self.form_layout_attendance = QFormLayout(self.attendance)
        self.make_group_attendance()

        layout_diary.addWidget(left_widget, stretch=3)

        # добавляем right_widget в общий layout
        layout_diary.addWidget(right_widget, stretch=2)

    def make_table_widget(self):
        """Создаём таблицу"""
        self.table_widget = QTableWidget(self)
        self.table_widget.cellClicked.connect(self.con_link_diary.ind_cell)
        self.table_widget.cellDoubleClicked.connect(self.con_link_diary.output_info_estimation)
        self.left_layout.addWidget(self.table_widget, stretch=2)

    def make_work_text(self):
        """Создаём текстовое поле"""
        self.output_work = QTextBrowser(self)
        self.left_layout.addWidget(self.output_work, stretch=1)

    def make_class(self):
        """Функция создаёт группу виджетов 'Класс'"""
        # Виджет(QComboBox) для выбора класс, который будет отображаться в таблице
        self.class_combo = QComboBox(self)
        self.class_combo.addItems(["-"] + ["".join(i) for i in self.db.all_class()])
        self.class_combo.currentTextChanged.connect(self.con_link_diary.output_name_in_table_widget)
        self.form_layout_class.addRow("Класс:", self.class_combo)

        # Виджет(QComboBox) для выбора месяца + года
        self.data_combo = QComboBox(self)
        self.data_combo.addItems(self.con_link_diary.list_mont_year)
        self.data_combo.currentTextChanged.connect(self.con_link_diary.output_name_in_table_widget)
        self.form_layout_class.addRow("Месяц:", self.data_combo)

        self.right_layout.addWidget(self.gr_class)

    def make_group_estimation(self):
        """Функция создаёт группу виджетов 'Оценка'"""
        # Виджет(QSpinBox) для оценки (обязательно)
        self.estimation_spin = QSpinBox(self)
        self.estimation_spin.setRange(2, 5)
        self.form_layout_estimation.addRow("Выберите оценку:", self.estimation_spin)

        # Виджет(QComboBox) для выбора типа работы (обязательно)
        self.type_work_estimation_combo = QComboBox(self)
        self.type_work_estimation_combo.addItems(["Контрольная работа", "Самостоятельная работа",
                                                  "Лабораторная работа", "Ответ на уроке"])
        self.form_layout_estimation.addRow("Выберите тип работы:", self.type_work_estimation_combo)

        # Виджет(QPlainTextEdit) для добавления комментария к, оценки
        self.comment_estimation_plain = QPlainTextEdit(self)
        self.form_layout_estimation.addRow("Комментарий к оценке", self.comment_estimation_plain)

        # Виджет(QPushButton) для подтверждения оценки
        self.verify_estimation_button = QPushButton("✓", self)
        self.verify_estimation_button.clicked.connect(
            self.con_link_diary.output_new_estimation_and_write_sql)  # сигнал для выставления оценки
        self.form_layout_estimation.addRow("Подтвердить оценку", self.verify_estimation_button)
        self.right_layout.addWidget(self.estimation)

    def make_group_assignment_works(self):
        """Функция создаёт группу виджетов 'Назначение работы'"""
        # Виджет(QComboBox) для выбора типа работы
        self.type_work_assignment_combo = QComboBox(self)
        self.type_work_assignment_combo.addItems(
            ["Контрольная работа", "Самостоятельная работа", "Лабораторная работа", "Домашняя работа"])
        self.form_layout_assignment_works.addRow("Тип работы:", self.type_work_assignment_combo)

        # Виджет(QPlainText) для комментария к работе
        self.comment_assignment_plaint = QPlainTextEdit(self)
        self.form_layout_assignment_works.addRow("Комментарий к работе/заданию", self.comment_assignment_plaint)

        # Виджет QLineEdit для установления даты
        self.data_line = QLineEdit(self)
        self.form_layout_assignment_works.addRow("Введите день работы/задания", self.data_line)

        # Виджет(QPushButton) для подтверждения оценки
        self.verify_work_assignment = QPushButton("✓", self)
        self.verify_work_assignment.clicked.connect(self.con_link_diary.output_new_task_and_write_sql)
        self.form_layout_assignment_works.addRow("Подтвердить работу", self.verify_work_assignment)
        self.right_layout.addWidget(self.assignment_works)

    def make_group_attendance(self):
        """Функция создаёт группу виджетов 'Посещаемость'"""
        # Виджет(QPushButton) для подтверждения
        self.verify_attendance_button = QPushButton("✓", self)
        self.verify_attendance_button.clicked.connect(self.con_link_diary.output_new_attendance_and_write_sql)
        self.form_layout_attendance.addRow("Отсутствие на уроке:", self.verify_attendance_button)
        self.right_layout.addWidget(self.attendance)

    def setup_add_class_tab(self):
        """Метод создаёт интерфейс для вкладки 'Добавление нового класса'"""
        layout_add = QHBoxLayout(self.tab_add_class)

        # --- Левая часть: Загрузка таблицы из CSV или Txt
        right_widget = QWidget()
        self.right_layout_add = QVBoxLayout(right_widget)

        self.uploading_file = QGroupBox("Загрузка файла")
        self.form_layout_file = QFormLayout(self.uploading_file)
        self.make_left_widget()

        self.verify_file = QGroupBox("Подтвердить новый класс?")
        self.form_layout_vf = QFormLayout(self.verify_file)
        self.make_verify_file()

        self.change_cl_file = QGroupBox("Изменить класс?")
        self.form_layout_change_cl = QFormLayout(self.change_cl_file)
        self.make_change_student()

        layout_add.addWidget(right_widget, stretch=1)
        self.make_table_widget_add(layout_add)

    def make_left_widget(self):
        """Создаём группу виджетов где можно будет загрузить файл учеников"""
        # Виджет(QRadioButton) для выбора типа файла (Txt)
        self.type_file_txt = QRadioButton(self)
        self.form_layout_file.addRow("Txt:", self.type_file_txt)

        # Виджет(QRadioButton) для выбора типа файла (CSV)
        self.type_file_csv = QRadioButton(self)
        self.form_layout_file.addRow("CSV:", self.type_file_csv)

        # Виджет(QPushButton) по нажатию на неё открывается QFileDialog
        self.open_file_button = QPushButton("Загрузить", self)
        self.open_file_button.clicked.connect(self.con_link_add_cl.save_txt_or_csv_file)
        self.form_layout_file.addRow("Файл с учениками:", self.open_file_button)

        # Виджет(QLineEdit) для буквы и цифры класса
        self.name_class_line = QLineEdit(self)
        self.form_layout_file.addRow("Номер и буква класса:", self.name_class_line)

        self.load_new_class = QPushButton("✓", self)
        self.load_new_class.clicked.connect(self.con_link_add_cl.Checking_correctness_record)
        self.form_layout_file.addRow("Проверить новый класс:", self.load_new_class)
        self.right_layout_add.addWidget(self.uploading_file)

    def make_verify_file(self):
        """Создаём две кнопки для подтверждения нового класса в дневнике"""
        # Виджет(QPushButton) для подтверждения класса
        self.yes_new_class = QPushButton("✓", self)
        self.yes_new_class.clicked.connect(self.con_link_add_cl.final_file_upload)
        self.form_layout_vf.addRow("Подтвердить:", self.yes_new_class)

        # Виджет(QPushButton) для отмены нового класса
        self.no_new_class = QPushButton("✘", self)
        self.no_new_class.clicked.connect(self.con_link_add_cl.canceling_new_class)
        self.form_layout_vf.addRow("Отмена:", self.no_new_class)
        self.right_layout_add.addWidget(self.verify_file)

    def make_change_student(self):
        """Создаём кнопки для изменения класса"""

        self.name_student_line = QLineEdit(self)
        self.ins_name_class_line = QLineEdit(self)
        self.new_student = QLineEdit(self)

        self.form_layout_change_cl.addRow("ФИО ученика", self.name_student_line)
        self.form_layout_change_cl.addRow("Класс", self.ins_name_class_line)

        new_student = QPushButton("✓", self)
        new_student.clicked.connect(self.con_link_add_cl.add_one_student)
        change_student = QPushButton("✓", self)
        change_student.clicked.connect(self.con_link_add_cl.new_full_name_student)

        self.form_layout_change_cl.addRow("Добавить ученика", new_student)
        self.form_layout_change_cl.addRow("Новое ФИО", self.new_student)
        self.form_layout_change_cl.addRow("Изменить ФИО ученика", change_student)

        self.right_layout_add.addWidget(self.change_cl_file)

    def make_table_widget_add(self, layout):
        """Создаём группу виджетов где можно будет посмотреть как это будет выглядеть в таблице"""
        # Виджет(QTableWidget) для просмотра таблицы
        self.table_widget_add = QTableWidget(self)
        layout.addWidget(self.table_widget_add, stretch=3)

    def setup_help_tab(self):
        setup_help_tab(self)

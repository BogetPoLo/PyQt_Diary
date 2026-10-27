import sys
from PyQt6.QtWidgets import QApplication
from Window_Dialog import MyMessage
from Main_Win import ApplicationInterface
from Control_Diary import ConnectingLinkDiary


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        /* Общие стили для всего приложения */
        QMainWindow, QDialog {
            background-color: #121212;  /* Почти чёрный */
            color: #e0e0e0;             /* Светло-серый текст */
        }

        /* Стили для кнопок */
        QPushButton {
            background-color: #006969;  /* Темнее DarkCyan */
            color: white;
            border: 1px solid #008b8b;  /* DarkCyan */
            border-radius: 5px;
            padding: 5px;
            min-width: 80px;
        }

        QPushButton:hover {
            background-color: #008b8b;  /* DarkCyan */
        }

        QPushButton:pressed {
            background-color: #004d4d;  /* Ещё темнее */
        }

        /* Стили для меток */
        QLabel {
            color: #e0e0e0;  /* Светло-серый текст */
            font-family: Arial;
            font-size: 12px;
        }

        /* Стили для текстовых полей */
        QLineEdit, QTextEdit, QPlainTextEdit, QTextBrowser {
            background-color: #1e1e1e;  /* Темно-серый фон */
            border: 1px solid #006969;
            border-radius: 5px;
            padding: 5px;
            color: #e0e0e0;
        }

        /* Стили для QComboBox */
        QComboBox {
            background-color: #1e1e1e;
            border: 1px solid #006969;
            border-radius: 5px;
            padding: 5px;
            color: #e0e0e0;
        }

        QComboBox QAbstractItemView {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #006969;
        }

        /* Стили для QTableWidget */
        QTableWidget {
            background-color: #1e1e1e;  /* Темно-серый фон */
            border: 1px solid #006969;
            gridline-color: #006969;
            color: #e0e0e0;
            alternate-background-color: #191919;
        }

        QHeaderView::section {
            background-color: #006969;  /* Темно-бирюзовый фон */
            color: black;  /* Черный текст для заголовков */
            padding: 5px;
            border: 1px solid #008b8b;
        }

        QTableWidget::item {
            color: black;  /* Черный текст для ячеек */
        }

        QTableWidget::item:selected {
            background-color: #008b8b;  /* Темно-бирюзовый фон для выделенных ячеек */
            color: black;  /* Черный текст для выделенных ячеек */
        }

        /* Стили для QScrollArea */
        QScrollArea {
            border: 1px solid #006969;
            background-color: #121212;
        }

        /* Стили для QGroupBox */
        QGroupBox {
            border: 1px solid #006969;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #121212;
            color: #e0e0e0;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #e0e0e0;
        }

        /* Стили для QTabWidget */
        QTabWidget::pane {
            border: 1px solid #006969;
            background-color: #121212;
        }

        QTabBar::tab {
            background: #006969;
            color: white;
            padding: 5px;
            border: 1px solid #008b8b;
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }

        QTabBar::tab:selected {
            background: #008b8b;
            margin-bottom: -1px;
            color: white;
        }

        QTabBar::tab:hover {
            background: #009999;
        }

        /* Стили для QSpinBox */
        QSpinBox {
            background-color: #1e1e1e;
            border: 1px solid #006969;
            border-radius: 5px;
            padding: 5px;
            color: #e0e0e0;
        }

        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #006969;
            width: 20px;
        }

        QSpinBox::up-arrow, QSpinBox::down-arrow {
            width: 10px;
            height: 10px;
        }

        /* Стили для QRadioButton и QCheckBox */
        QRadioButton, QCheckBox {
            color: #e0e0e0;
            spacing: 5px;
        }

        QRadioButton::indicator, QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }

        QRadioButton::indicator:checked, QCheckBox::indicator:checked {
            background-color: #006969;
            border: 1px solid #008b8b;
        }

        /* Стили для QMessageBox */
        QMessageBox {
            background-color: #121212;
            color: #e0e0e0;
        }

        QMessageBox QLabel {
            color: #e0e0e0;
        }

        QMessageBox QPushButton {
            background-color: #006969;
            color: white;
            border: 1px solid #008b8b;
            border-radius: 5px;
            padding: 5px;
            min-width: 80px;
        }
    """)
    window = ApplicationInterface()  # Создаем экземпляр ApplicationInterface
    my_error = MyMessage(window)
    connecting_link = ConnectingLinkDiary(window, my_error)  # Передаем экземпляр в ConnectingLink
    window.show()
    sys.exit(app.exec())

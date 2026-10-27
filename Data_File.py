import sqlite3


class DateBase:
    """Класс реализует запросы в sql"""

    def __init__(self):
        self.con = sqlite3.connect("school.db")
        self.cur = self.con.cursor()

    def add_estimation_to_sql(self, score: int, name: str, date: str, work: str, name_class: str, comment: str,
                              photo):  # Надо будет дописать способность добавлять фото к оценке
        """Метод реализует добавление новой оценки для определённого ученика в sql"""

        " --- Получаем id класса --- "
        id_cl = self.receiving_id_class(name_class)

        " --- Получаем id ученика --- "
        id_st = self.getting_id_student(name, id_cl)

        " --- Записываем новую оценку в таблицу(Estimation) SQL --- "
        self.cur.execute("""INSERT INTO Estimation(score, id_student_est, id_class_est, date_est, work_es,
         comment_est, photo)
         VALUES(?, ?, ?, ?, ?, ?, ?)""", (score, id_st[0][0], id_cl[0][0], date, work, comment, photo))
        self.confirmation_result()

    def add_new_attendance_to_sql(self, name: str, name_class: str, date: str):
        """Метод реализует добавление Н-ки для определённого ученика в sql"""

        " --- Получение id Класса --- "
        id_cl = self.receiving_id_class(name_class)

        "--- Получение id ученика --- "
        id_st = self.getting_id_student(name, id_cl)

        " --- Записываем Н-ку d таблицу(Attendance) SQL --- "
        self.cur.execute("""INSERT INTO Attendance(id_student_at, id_class_at, flag, date_at)
         VALUES(?, ?, ?, ?)""", (id_st[0][0], id_cl[0][0], "Н", date))
        self.confirmation_result()

    def add_new_word_to_sql(self, work: str, com: str, date: str, name_class: str):
        """Метод реализует назначение работы для класса в sql"""

        " --- Получаем id класса --- "
        id_cl = self.receiving_id_class(name_class)

        " --- Записываем работу/задание в таблицу(Task) SQL --- "
        self.cur.execute("""INSERT INTO Task(work, comment, date_work, id_class_ta)
        VALUES(?, ?, ?, ?)""", (work, com, date, id_cl[0][0]))
        self.confirmation_result()

    def old_work_to_sql(self, now_data):
        """Метод удаляет все прошедшие работы"""
        all_date_work = self.cur.execute("""SELECT date_work FROM Task""").fetchall()

        for dat in all_date_work:
            old_day, old_mon, old_ye = dat[0].split(".")
            now_day, now_mon, now_ye = now_data
            if int(old_ye) < int(now_ye):
                self.cur.execute("""DELETE from Task WHERE date_work = ?""", (dat[0],))
            else:
                if int(old_mon) < int(now_mon):
                    self.cur.execute("""DELETE from Task WHERE date_work = ?""", (dat[0],))
                else:
                    if int(old_day) < int(now_day):
                        self.cur.execute("""DELETE from Task WHERE date_work = ?""", (dat[0],))
        self.confirmation_result()

    def getting_names(self, name_class):
        """Метод возвращает список всех учеников определённого класса"""
        id_cl = self.receiving_id_class(name_class)

        " --- Записываем все имена в список --- "
        all_student = self.cur.execute("""SELECT full_name FROM Student
    WHERE Student.id_class_st = ?""", (id_cl[0][0],)).fetchall()
        return all_student

    def getting_id_student(self, name, id_class):
        """Метод возвращает id ученика"""
        id_st = self.cur.execute("""SELECT id FROM Student
    WHERE Student.full_name = ? AND Student.id_class_st = ?""", (name, id_class[0][0])).fetchall()
        return id_st

    def receiving_id_class(self, name_class):
        """Возвращает id класса"""
        return self.cur.execute("""SELECT id FROM Class
    WHERE Class.name_class = ?""", (name_class,)).fetchall()

    def all_class(self):
        """Метод возвращает имена всех классов"""
        cl = self.cur.execute("""SELECT name_class FROM Class""").fetchall()
        return cl

    def getting_attendance(self, name_class):
        """Возвращает посещаемость класса"""
        id_cl = self.receiving_id_class(name_class)
        """Запрашиваем посещаемость класса"""
        attendance = self.cur.execute("""SELECT id_student_at, flag, date_at FROM Attendance
    WHERE Attendance.id_class_at = ?""", (id_cl[0][0],)).fetchall()
        dict_att = {}

        """Заменяем id ученика на имя ученика"""
        for i in range(len(attendance)):
            name, att, time = attendance[i]
            name = self.cur.execute("""SELECT full_name FROM Student
    WHERE id == ?""", (name,)).fetchall()[0][0]
            if name in dict_att:
                dict_att[name].append([att, time])
            else:
                dict_att[name] = [[att, time]]
        return dict_att

    def getting_estimation_class(self, name_class):
        """Возвращает оценки класса"""
        id_cl = self.receiving_id_class(name_class)
        estimation = self.cur.execute("""SELECT score, id_student_est, date_est FROM Estimation
    WHERE Estimation.id_class_est = ?""", (id_cl[0][0],)).fetchall()
        dict_est = {}

        for i in range(len(estimation)):
            score, name, date_est = estimation[i]
            name = self.cur.execute("""SELECT full_name FROM Student
    WHERE Student.id = ?""", (name,)).fetchall()[0][0]
            if name in dict_est:
                dict_est[name].append([score, date_est])
            else:
                dict_est[name] = [[score, date_est]]
        return dict_est

    def getting_task_class(self, name_class: str):
        """Возвращает все работы для класса"""
        id_cl = self.receiving_id_class(name_class)
        task = self.cur.execute("""SELECT work, comment, date_work FROM Task
    WHERE Task.id_class_ta = ?""", (id_cl[0][0],)).fetchall()

        task = sorted(task, key=lambda x: (int(x[2].split(".")[0]), int(x[2].split(".")[1]), int(x[2].split(".")[2])))
        control_work = []
        independent_work = []
        laboratory_work = []
        home_work = []

        for type_work in task:
            if type_work[0] == "Контрольная работа":
                control_work.append(type_work[1::])
            elif type_work[0] == "Самостоятельная работа":
                independent_work.append(type_work[1::])
            elif type_work[0] == "Лабораторная работа":
                laboratory_work.append(type_work[1::])
            elif type_work[0] == "Домашняя работа":
                home_work.append(type_work[1::])
        return control_work, independent_work, laboratory_work, home_work

    def getting_estimation_for_student(self, name_class, name, date_est):
        """Функция возвращает всё информацию про оценку для определённого ученика"""
        """Получаем id класса"""
        id_cl = self.receiving_id_class(name_class)

        """Получаем id ученика"""
        id_st = self.getting_id_student(name, id_cl)

        """Получаем оценки ученика"""
        est_st = self.cur.execute("""SELECT score, work_es, comment_est, photo FROM Estimation WHERE id_student_est
         = ? and id_class_est = ? and date_est = ?""", (id_st[0][0], id_cl[0][0], date_est)).fetchall()

        return est_st

    def load_new_class_and_student(self, name_class, names_students):
        """Добавляем новый класс в бд"""

        if all([1 if name_class not in i else 0 for i in self.all_class()]):  # Проверяем что такого класса нет
            """Новый класс в таблице Class"""
            self.cur.execute("""INSERT INTO Class(name_class) VALUES(?)""", (name_class,))
            self.confirmation_result()

            """Получаем id нового класса"""
            id_cl = self.receiving_id_class(name_class)

            """Загружаем новые имена в бд"""
            for name in names_students:
                self.cur.execute("""INSERT INTO Student(full_name, id_class_st) VALUES(?, ?)""",
                                 (name, id_cl[0][0]))
            self.confirmation_result()
        else:
            return False

    def add_new_student_to_sql(self, name_class, name):
        """Добавляем нового ученика в sql"""

        """Получаем id нового класса"""
        id_cl = self.receiving_id_class(name_class)

        """Добавляем нового ученика"""
        self.cur.execute("""INSERT INTO Student(full_name, id_class_st) VALUES(?, ?)""",
                         (name, id_cl[0][0]))
        self.confirmation_result()

    def new_full_name_to_sql(self, name_class, new_name, old_name):
        """Изменяем ФИО ученика"""

        """Получаем id класса"""
        id_cl = self.receiving_id_class(name_class)

        """Изменение"""
        self.cur.execute("""UPDATE Student
                            SET full_name = ?
                            WHERE full_name = ? and id_class_st = ?""", (new_name, old_name, id_cl[0][0]))
        self.confirmation_result()

    def confirmation_result(self):
        """Записываем изменения в таблицу"""
        self.con.commit()

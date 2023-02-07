import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5 import QtGui
from setup_table import *
from connect_to_db import *


def define_ids(period_title, period_year,
               surname, name, patr,
               number, letter,
               title,
               type_name):
    period_id = pd.read_sql("SELECT ID "
                            "FROM REPORT_PERIOD "
                            "WHERE TITLE = %s AND YEAR = %s",
                            dbConnection,
                            params=[period_title, period_year]).loc[0]["ID"]
    teacher_id = pd.read_sql("SELECT ID "
                             "FROM TEACHER "
                             "WHERE SURNAME = %s AND NAME = %s AND PATRONIMYC = %s",
                             dbConnection,
                             params=[surname, name, patr]).loc[0]["ID"]
    class_data = pd.read_sql("SELECT ID, QUANTITY "
                             "FROM CLASS "
                             "WHERE NUMBER = %s AND LETTER = %s AND STATUS = 1",
                             dbConnection,
                             params=[number, letter])
    class_id = class_data.loc[0]["ID"]
    class_quantity = class_data.loc[0]["QUANTITY"]
    subject_id = pd.read_sql("SELECT ID "
                             "FROM SUBJECT "
                             "WHERE TITLE = %s",
                             dbConnection,
                             params=[title]).loc[0]["ID"]
    report_type_id = pd.read_sql("SELECT ID "
                                 "FROM REPORT_TYPE "
                                 "WHERE TYPE_NAME = %s",
                                 dbConnection,
                                 params=[type_name]).loc[0]["ID"]
    return [period_id, teacher_id, class_id, subject_id, report_type_id, class_quantity]


class TeacherReport(QDialog):
    def __init__(self, widget):
        super(TeacherReport, self).__init__()
        loadUi("UIs/teacher_report.ui", self)
        self.widget = widget
        self.exit.clicked.connect(self.go_exit)
        set_columns_report(self.tableWidgetreport)
        self.reports = []
        self.data = []
        self.filter = ''
        reports = self.report_queries()
        self.load_data_report(reports)
        self.choose_filter.clicked.connect(self.load_filter)
        self.search_filter.clicked.connect(self.show_filtered_reports)
        self.new_rep.clicked.connect(self.create_new_report)
        self.print_report.clicked.connect(self.show_print_panel)

    def load_data_report(self, reports):
        self.tableWidgetreport.setRowCount(len(reports))
        table_row = 0
        for i in range(len(reports)):
            self.tableWidgetreport.setItem(table_row, 0,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["TITLE"])))
            self.tableWidgetreport.setItem(table_row, 1,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["YEAR"])))
            self.tableWidgetreport.setItem(table_row, 2,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["SURNAME"]))
            self.tableWidgetreport.setItem(table_row, 3,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["NAME"]))
            self.tableWidgetreport.setItem(table_row, 4,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["PATRONIMYC"]))
            self.tableWidgetreport.setItem(table_row, 5,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["NUMBER"])))
            self.tableWidgetreport.setItem(table_row, 6,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["LETTER"]))
            self.tableWidgetreport.setItem(table_row, 7,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["SUBJECT"]))
            self.tableWidgetreport.setItem(table_row, 8,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["TYPE_NAME"]))
            self.tableWidgetreport.setItem(table_row, 9,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_A"])))
            self.tableWidgetreport.setItem(table_row, 10,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_B"])))
            self.tableWidgetreport.setItem(table_row, 11,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_C"])))
            self.tableWidgetreport.setItem(table_row, 12,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_D"])))
            self.tableWidgetreport.setItem(table_row, 13,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["N_A"])))
            self.tableWidgetreport.setItem(table_row, 14,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["NAMES"]))
            self.tableWidgetreport.setItem(table_row, 15,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["QUANTITY"])))
            self.btn1 = QPushButton(self.tableWidgetreport)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./UIs/images/trash_bin.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.btn1.setIcon(icon)
            self.btn1.setStyleSheet("background-color:#FFD1BE;")
            self.btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.tableWidgetreport.setCellWidget(table_row, 16, self.btn1)
            self.btn1.clicked.connect(self.delete_report)
            self.btn2 = QPushButton(self.tableWidgetreport)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./UIs/images/pencilandpaper.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.btn2.setIcon(icon)
            self.btn2.setStyleSheet("background-color:#E4E4E4;")
            self.btn2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btn2.clicked.connect(self.edit_report)
            self.tableWidgetreport.setCellWidget(table_row, 17, self.btn2)
            table_row += 1
        self.reports = []

    def show_print_panel(self):
        import teacher_print
        print_panel = teacher_print.TeacherPrint(self.widget)
        self.widget.addWidget(print_panel)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def create_new_report(self):
        pop = NewReport(self)
        pop.show()

    def show_filtered_reports(self):
        self.data = self.category_res.currentText().split()
        pop = FilteredReports(self, self.filter, self.data)
        pop.show()

    def go_exit(self):
        from ZvitOUT import app, sys
        sys.exit(app.exec())

    def report_queries(self):
        reports = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE "
            "ORDER BY NUMBER, LETTER, SUBJECT.TITLE, SURNAME", dbConnection)
        return reports

    def load_filter(self):
        self.filter = self.categories.currentText()
        if self.filter == "класом":
            self.category_res.clear()
            classes = pd.read_sql("SELECT NUMBER, LETTER, FOUND_YEAR "
                                  "FROM CLASS "
                                  "WHERE STATUS = 1 "
                                  "ORDER BY NUMBER, LETTER, FOUND_YEAR", dbConnection)
            for i in range(len(classes)):
                self.category_res.addItem\
                    (f'{classes.loc[i]["NUMBER"]} {classes.loc[i]["LETTER"]} {classes.loc[i]["FOUND_YEAR"]}')
        elif self.filter == "предметом":
            self.category_res.clear()
            subjects = pd.read_sql("SELECT TITLE "
                                   "FROM SUBJECT "
                                   "ORDER BY TITLE", dbConnection)
            for i in range(len(subjects)):
                self.category_res.addItem(f'{subjects.loc[i]["TITLE"]}')
        elif self.filter == "вчителем":
            self.category_res.clear()
            teachers = pd.read_sql("SELECT SURNAME, NAME, PATRONIMYC "
                                   "FROM TEACHER "
                                   "ORDER BY SURNAME", dbConnection)
            for i in range(len(teachers)):
                self.category_res.addItem\
                    (f'{teachers.loc[i]["SURNAME"]} {teachers.loc[i]["NAME"]} {teachers.loc[i]["PATRONIMYC"]}')
        elif self.filter == "періодом":
            self.category_res.clear()
            periods = pd.read_sql("SELECT TITLE, YEAR "
                                  "FROM REPORT_PERIOD "
                                  "ORDER BY YEAR", dbConnection)
            for i in range(len(periods)):
                self.category_res.addItem \
                    (f'{periods.loc[i]["TITLE"]} {periods.loc[i]["YEAR"]}')
        elif self.filter == "типом звіту":
            self.category_res.clear()
            types = pd.read_sql("SELECT TYPE_NAME "
                                "FROM REPORT_TYPE ", dbConnection)
            for i in range(len(types)):
                self.category_res.addItem \
                    (f'{types.loc[i]["TYPE_NAME"]}')

    def confirm_delete(self):
        pop = ConfirmDelete(self)
        pop.show()

    def delete_report(self):
        self.btn1.clicked = self.sender()
        parent = self.btn1.parent()
        pos = parent.mapToParent(self.btn1.clicked.pos())
        index = self.tableWidgetreport.indexAt(pos)
        row = index.row()
        id_data = define_ids(self.tableWidgetreport.item(row, 0).text(),
                              self.tableWidgetreport.item(row, 1).text(),
                              self.tableWidgetreport.item(row, 2).text(),
                              self.tableWidgetreport.item(row, 3).text(),
                              self.tableWidgetreport.item(row, 4).text(),
                              self.tableWidgetreport.item(row, 5).text(),
                              self.tableWidgetreport.item(row, 6).text(),
                              self.tableWidgetreport.item(row, 7).text(),
                              self.tableWidgetreport.item(row, 8).text())
        dbConnection.execute("DELETE FROM REPORT "
                             "WHERE ID_REPORT_PERIOD = %s AND ID_TEACHER = %s AND "
                             "ID_CLASS = %s AND ID_SUBJECT = %s AND "
                             "ID_REPORT_TYPE = %s ", id_data[0], id_data[1], id_data[2], id_data[3], id_data[4])
        self.tableWidgetreport.setRowCount(0)
        reports = self.report_queries()
        self.load_data_report(reports)

    def show_edit_report(self):
        pop = EditReport(self)
        pop.show()

    def edit_report(self):
        self.btn2.clicked = self.sender()
        parent = self.btn2.parent()
        pos = parent.mapToParent(self.btn2.clicked.pos())
        index = self.tableWidgetreport.indexAt(pos)
        row = index.row()
        self.data = [self.tableWidgetreport.item(row, 0).text(),
                        self.tableWidgetreport.item(row, 1).text(),
                        self.tableWidgetreport.item(row, 2).text(),
                        self.tableWidgetreport.item(row, 3).text(),
                        self.tableWidgetreport.item(row, 4).text(),
                        self.tableWidgetreport.item(row, 5).text(),
                        self.tableWidgetreport.item(row, 6).text(),
                        self.tableWidgetreport.item(row, 7).text(),
                        self.tableWidgetreport.item(row, 8).text(),
                        self.tableWidgetreport.item(row, 9).text(),
                        self.tableWidgetreport.item(row, 10).text(),
                        self.tableWidgetreport.item(row, 11).text(),
                        self.tableWidgetreport.item(row, 12).text(),
                        self.tableWidgetreport.item(row, 13).text(),
                        self.tableWidgetreport.item(row, 14).text()]
        self.id_data = define_ids(self.tableWidgetreport.item(row, 0).text(),
                             self.tableWidgetreport.item(row, 1).text(),
                             self.tableWidgetreport.item(row, 2).text(),
                             self.tableWidgetreport.item(row, 3).text(),
                             self.tableWidgetreport.item(row, 4).text(),
                             self.tableWidgetreport.item(row, 5).text(),
                             self.tableWidgetreport.item(row, 6).text(),
                             self.tableWidgetreport.item(row, 7).text(),
                             self.tableWidgetreport.item(row, 8).text())
        self.show_edit_report()


class FilteredReports(QDialog):
    def __init__(self, parent, filter, data):
        super().__init__(parent)
        loadUi("UIs/teacher_report_filtered.ui", self)
        self.setFixedSize(1250, 761)
        self.setWindowTitle("Звіт OUT|Звіти за фільтром")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs/images/school.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.filter = filter
        self.data = data
        self.parent = parent
        self.filter_name.setText(self.filter)
        set_columns_report(self.tableWidgetfilter)
        reports = self.find_filtered_reports()
        self.load_data_report(reports)

    def find_filtered_reports(self):
        result = ''
        if self.filter == "вчителем":
            result = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE "
            "AND SURNAME = %s AND NAME = %s AND PATRONIMYC = %s",
                dbConnection, params=[self.data[0], self.data[1], self.data[2]])
        elif self.filter == "класом":
            result = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE "
            "AND NUMBER = %s AND LETTER = %s AND FOUND_YEAR = %s",
                dbConnection, params=[self.data[0], self.data[1], self.data[2]])
        elif self.filter == "предметом":
            result = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE  AND TITLE = %s",
                dbConnection, params=[self.data[0:]])
        elif self.filter == "періодом":
            result = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE  AND TITLE = %s AND YEAR = %s",
                dbConnection, params=[self.data[0: -2], self.data[-1]])
        elif self.filter == "типом звіту":
            result = pd.read_sql(
            "SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
            "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
            "CLASS.NUMBER, CLASS.LETTER, "
            "SUBJECT.TITLE AS SUBJECT, "
            "REPORT_TYPE.TYPE_NAME, "
            "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
            "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
            "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
            "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
            "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
            "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE  AND TYPE_NAME = %s",
                dbConnection, params=[self.data[0:]])
        return result

    def load_data_report(self, reports):
        self.tableWidgetfilter.setRowCount(len(reports))
        table_row = 0
        for i in range(len(reports)):
            self.tableWidgetfilter.setItem(table_row, 0,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["TITLE"])))
            self.tableWidgetfilter.setItem(table_row, 1,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["YEAR"])))
            self.tableWidgetfilter.setItem(table_row, 2,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["SURNAME"]))
            self.tableWidgetfilter.setItem(table_row, 3,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["NAME"]))
            self.tableWidgetfilter.setItem(table_row, 4,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["PATRONIMYC"]))
            self.tableWidgetfilter.setItem(table_row, 5,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["NUMBER"])))
            self.tableWidgetfilter.setItem(table_row, 6,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["LETTER"]))
            self.tableWidgetfilter.setItem(table_row, 7,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["SUBJECT"]))
            self.tableWidgetfilter.setItem(table_row, 8,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["TYPE_NAME"]))
            self.tableWidgetfilter.setItem(table_row, 9,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_A"])))
            self.tableWidgetfilter.setItem(table_row, 10,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_B"])))
            self.tableWidgetfilter.setItem(table_row, 11,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_C"])))
            self.tableWidgetfilter.setItem(table_row, 12,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_D"])))
            self.tableWidgetfilter.setItem(table_row, 13,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["N_A"])))
            self.tableWidgetfilter.setItem(table_row, 14,
                                           QtWidgets.QTableWidgetItem(reports.loc[i]["NAMES"]))
            self.tableWidgetfilter.setItem(table_row, 15,
                                           QtWidgets.QTableWidgetItem(str(reports.loc[i]["QUANTITY"])))
            table_row += 1


class NewReport(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("UIs/new_report.ui", self)
        self.setFixedSize(1151, 791)
        self.setWindowTitle("Звіт OUT|Новий звіт")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs/images/school.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.parent = parent

        self.load_filters_data()
        self.close_window.clicked.connect(self.close)
        self.search_types.clicked.connect(self.get_report_types)
        self.save.clicked.connect(self.save_new_report)
        self.a.setText('0')
        self.b.setText('0')
        self.c.setText('0')
        self.d.setText('0')
        self.n.setText('0')

    def load_filters_data(self):
        classes = pd.read_sql("SELECT DISTINCT NUMBER "
                               "FROM CLASS "
                               "WHERE STATUS = 1 "
                               "ORDER BY NUMBER", dbConnection)
        for i in range(len(classes)):
            self.classes.addItem(f'{classes.loc[i]["NUMBER"]}')
        letters = pd.read_sql("SELECT DISTINCT LETTER "
                              "FROM CLASS "
                              "WHERE STATUS = 1 "
                              "ORDER BY LETTER", dbConnection)
        for i in range(len(classes)):
            self.letters.addItem(f'{letters.loc[i]["LETTER"]}')
        subjects = pd.read_sql("SELECT TITLE "
                               "FROM SUBJECT "
                               "WHERE STATUS = 1 "
                               "ORDER BY TITLE", dbConnection)
        for i in range(len(subjects)):
            self.subject.addItem(f'{subjects.loc[i]["TITLE"]}')
        teachers = pd.read_sql("SELECT SURNAME, NAME, PATRONIMYC "
                               "FROM TEACHER "
                               "ORDER BY SURNAME", dbConnection)
        for i in range(len(teachers)):
            self.teacher.addItem(f'{teachers.loc[i]["SURNAME"]} {teachers.loc[i]["NAME"]} {teachers.loc[i]["PATRONIMYC"]}')
        periods = pd.read_sql("SELECT TITLE, YEAR "
                              "FROM REPORT_PERIOD "
                              "WHERE STATUS = 1 "
                              "ORDER BY YEAR", dbConnection)
        for i in range(len(periods)):
            self.period.addItem(f'{periods.loc[i]["TITLE"]} {periods.loc[i]["YEAR"]}')

    def get_report_types(self):
        self.types.clear()
        subj = self.subject.currentText()
        types = pd.read_sql("SELECT TYPE_NAME FROM REPORT_TYPE "
                            "INNER JOIN REPORT_TO_SUBJECT ON REPORT_TYPE.ID = REPORT_TO_SUBJECT.ID_REPORT_TYPE "
                            "INNER JOIN SUBJECT ON REPORT_TO_SUBJECT.ID_SUBJECT = SUBJECT.ID "
                            "WHERE SUBJECT.TITLE = %s ", dbConnection, params=[subj])
        for i in range(len(types)):
            self.types.addItem(f'{types.loc[i]["TYPE_NAME"]}')

    def save_new_report(self):
        teacher = self.teacher.currentText().split()
        id_list = define_ids(" ".join(self.period.currentText().split()[0:-1]), self.period.currentText().split()[-1],
                                  teacher[0], teacher[1], teacher[2],
                                  self.classes.currentText(), self.letters.currentText(),
                                  self.subject.currentText(),
                                  self.types.currentText())
        students_a = int(self.a.text())
        students_b = int(self.b.text())
        students_c = int(self.c.text())
        students_d = int(self.d.text())
        students_na = int(self.n.text())
        students_quantity = students_a + students_b + students_d + students_c + students_d + students_na
        na_names = self.surnames.text()
        is_divide = pd.read_sql("SELECT DIVIDE "
                                "FROM SUBJECT "
                                "WHERE ID = %s",
                                 dbConnection,
                                 params=[id_list[3]]).loc[0]["DIVIDE"]
        if students_quantity != id_list[5] and not is_divide:
            self.all.setText(str(students_quantity))
            self.all_pupils.setText(str(id_list[5]))
            self.notquantity.setText('Кількість учнів не співпадає.')
        else:
            report = {
                "ID_REPORT_PERIOD": [id_list[0]],
                "ID_TEACHER" : [id_list[1]],
                "ID_CLASS": [id_list[2]],
                "ID_SUBJECT": [id_list[3]],
                "ID_REPORT_TYPE": [id_list[4]],
                "STUDENTS_A": [students_a],
                "STUDENTS_B": [students_b],
                "STUDENTS_C": [students_c],
                "STUDENTS_D": [students_d],
                "N_A": [students_na],
                "NAMES": [na_names]
            }
            df = pd.DataFrame(data=report)
            df.to_sql(con=dbConnection, name="REPORT", if_exists='append', index=False)
            self.parent.tableWidgetreport.setRowCount(0)
            reports = self.parent.report_queries()
            self.parent.load_data_report(reports)
            self.close()


class EditReport(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("UIs/update_teacher_report.ui", self)
        self.setFixedSize(806, 580)
        self.setWindowTitle("Звіт OUT|Редагувати звіт")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs/images/school.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.parent = parent
        self.exit.clicked.connect(self.close)
        self.save.clicked.connect(self.save_report)
        self.period.setText(f'{self.parent.data[0]} {self.parent.data[1]}')
        self.surname.setText(self.parent.data[2])
        self.name.setText(self.parent.data[3])
        self.patr.setText(self.parent.data[4])
        self.classes.setText(f'{self.parent.data[5]} - {self.parent.data[6]}')
        self.subject.setText(self.parent.data[7])
        self.report_type.setText(self.parent.data[8])
        self.a.setText(self.parent.data[9])
        self.b.setText(self.parent.data[10])
        self.c.setText(self.parent.data[11])
        self.d.setText(self.parent.data[12])
        self.n_a.setText(self.parent.data[13])
        self.names.setText(self.parent.data[14])

    def save_report(self):
        students_quantity = int(self.a.text()) + int(self.b.text()) + int(self.c.text()) + int(self.d.text()) + int(self.n_a.text())
        is_divide = pd.read_sql("SELECT DIVIDE "
                                "FROM SUBJECT "
                                "WHERE ID = %s",
                                dbConnection,
                                params=[self.parent.id_data[3]]).loc[0]["DIVIDE"]
        if students_quantity != self.parent.id_data[5] and not is_divide:
            self.all.setText(f'Загалом: {str(students_quantity)}')
            self.on_list.setText(f'За списком: {str(self.parent.id_data[5])}')
        else:
            dbConnection.execute("UPDATE REPORT "
                                 "SET STUDENTS_A = %s, "
                                 "STUDENTS_B = %s, "
                                 "STUDENTS_C = %s, "
                                 "STUDENTS_D = %s, "
                                 "N_A = %s, "
                                 "NAMES = %s "
                                 "WHERE ID_REPORT_PERIOD = %s AND ID_TEACHER = %s AND "
                                 "ID_CLASS = %s AND ID_SUBJECT = %s AND "
                                 "ID_REPORT_TYPE = %s ",
                                 self.a.text(), self.b.text(), self.c.text(), self.d.text(), self.n_a.text(), self.names.text(),
                                 self.parent.id_data[0], self.parent.id_data[1], self.parent.id_data[2],
                                 self.parent.id_data[3], self.parent.id_data[4])
            self.parent.tableWidgetreport.setRowCount(0)
            reports = self.parent.report_queries()
            self.parent.load_data_report(reports)
            self.close()











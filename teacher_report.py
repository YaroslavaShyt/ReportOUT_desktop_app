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


class TeacherReport(QDialog):
    def __init__(self, widget):
        super(TeacherReport, self).__init__()
        loadUi("UIs/teacher_report.ui", self)
        self.widget = widget
        self.exit.clicked.connect(self.go_exit)
        set_columns_report(self.tableWidgetreport)
        self.reports = []
        self.data = []
        reports = self.report_queries()
        load_data_report(self.tableWidgetreport, reports)
        self.choose_filter.clicked.connect(self.load_filter)
        self.search_filter.clicked.connect(self.show_filtered_reports)
        self.new_rep.clicked.connect(self.create_new_report)
        self.print_report.clicked.connect(self.show_print_panel)

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

    def go_exit(self):  # take to a "setup" file and import
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


class FilteredReports(QDialog):
    def __init__(self, parent, filter, data):
        super().__init__(parent)
        loadUi("UIs/teacher_report_filtered.ui", self)
        self.setFixedSize(1400, 761)
        self.filter = filter
        self.data = data
        self.filter_name.setText(self.filter)
        set_columns_report(self.tableWidgetfilteredreport)
        reports = self.find_filtered_reports()
        load_data_report(self.tableWidgetfilteredreport, reports)

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


class NewReport(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("UIs/new_report.ui", self)
        self.setFixedSize(1151, 791)
        self.setWindowTitle("Звіт OUT|Новий звіт")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UIs/images/school.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
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
        period_id = pd.read_sql("SELECT ID "
                                "FROM REPORT_PERIOD "
                                "WHERE TITLE = %s AND YEAR = %s",
                                dbConnection,
                                params=[" ".join(self.period.currentText().split()[0:-1]),
                                        self.period.currentText().split()[-1]]).loc[0]["ID"]
        teacher = self.teacher.currentText().split()
        teacher_id = pd.read_sql("SELECT ID "
                                 "FROM TEACHER "
                                 "WHERE SURNAME = %s AND NAME = %s AND PATRONIMYC = %s",
                                 dbConnection,
                                 params=[teacher[0],
                                         teacher[1],
                                         teacher[2]]).loc[0]["ID"]
        class_data = pd.read_sql("SELECT ID, QUANTITY "
                                 "FROM CLASS "
                                 "WHERE NUMBER = %s AND LETTER = %s AND STATUS = 1",
                                  dbConnection,
                                  params=[self.classes.currentText(),
                                          self.letters.currentText()])
        class_id = class_data.loc[0]["ID"]
        class_quantity = class_data.loc[0]["QUANTITY"]
        subject_id = pd.read_sql("SELECT ID "
                                 "FROM SUBJECT "
                                 "WHERE TITLE = %s",
                                  dbConnection,
                                  params=[self.subject.currentText()]).loc[0]["ID"]
        report_type_id = pd.read_sql("SELECT ID "
                                     "FROM REPORT_TYPE "
                                     "WHERE TYPE_NAME = %s",
                                      dbConnection,
                                      params=[self.types.currentText()]).loc[0]["ID"]
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
                                 params=[subject_id]).loc[0]["DIVIDE"]
        if students_quantity != class_quantity and not is_divide:
            self.all.setText(str(students_quantity))
            self.all_pupils.setText(str(class_quantity))
            self.notquantity.setText('Кількість учнів не співпадає.')
        else:
            report = {
                "ID_REPORT_PERIOD": [period_id],
                "ID_TEACHER" : [teacher_id],
                "ID_CLASS": [class_id],
                "ID_SUBJECT": [subject_id],
                "ID_REPORT_TYPE": [report_type_id],
                "STUDENTS_A": [students_a],
                "STUDENTS_B": [students_b],
                "STUDENTS_C": [students_c],
                "STUDENTS_D": [students_d],
                "N_A": [students_na],
                "NAMES": [na_names]
            }
            df = pd.DataFrame(data=report)
            df.to_sql(con=dbConnection, name="REPORT", if_exists='append', index=False)
            self.close()


def load_data_report(tableWidgetreport, reports):
    tableWidgetreport.setRowCount(len(reports))
    table_row = 0
    for i in range(len(reports)):
        tableWidgetreport.setItem(table_row, 0,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["TITLE"])))
        tableWidgetreport.setItem(table_row, 1,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["YEAR"])))
        tableWidgetreport.setItem(table_row, 2,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["SURNAME"]))
        tableWidgetreport.setItem(table_row, 3,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["NAME"]))
        tableWidgetreport.setItem(table_row, 4,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["PATRONIMYC"]))
        tableWidgetreport.setItem(table_row, 5,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["NUMBER"])))
        tableWidgetreport.setItem(table_row, 6,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["LETTER"]))
        tableWidgetreport.setItem(table_row, 7,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["SUBJECT"]))
        tableWidgetreport.setItem(table_row, 8,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["TYPE_NAME"]))
        tableWidgetreport.setItem(table_row, 9,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_A"])))
        tableWidgetreport.setItem(table_row, 10,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_B"])))
        tableWidgetreport.setItem(table_row, 11,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_C"])))
        tableWidgetreport.setItem(table_row, 12,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["STUDENTS_D"])))
        tableWidgetreport.setItem(table_row, 13,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["N_A"])))
        tableWidgetreport.setItem(table_row, 14,
                                       QtWidgets.QTableWidgetItem(reports.loc[i]["NAMES"]))
        tableWidgetreport.setItem(table_row, 15,
                                       QtWidgets.QTableWidgetItem(str(reports.loc[i]["QUANTITY"])))
        btn1 = QPushButton(tableWidgetreport)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./UIs/images/trash_bin.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btn1.setIcon(icon)
        btn1.setStyleSheet("background-color:#FFD1BE;")
        btn1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        tableWidgetreport.setCellWidget(table_row, 16, btn1)
        # self.btn1.clicked.connect(self.go_edit_report)
        btn2 = QPushButton(tableWidgetreport)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./UIs/images/pencilandpaper.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btn2.setIcon(icon)
        btn2.setStyleSheet("background-color:#E4E4E4;")
        btn2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        tableWidgetreport.setCellWidget(table_row, 17, btn2)
        table_row += 1







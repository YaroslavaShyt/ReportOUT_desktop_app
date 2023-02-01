from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5 import QtGui


class TeacherPrint(QDialog):
    def __init__(self, widget):
        super(TeacherPrint, self).__init__()
        loadUi("UIs/teacher_print.ui", self)
        self.widget = widget
        self.report.clicked.connect(self.show_teacher_report_panel)
        self.exit.clicked.connect(self.go_exit)
        self.load_filters_data()

    def show_teacher_report_panel(self):
        import teacher_report
        teacher_report_panel = teacher_report.TeacherReport(self.widget)
        self.widget.addWidget(teacher_report_panel)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_exit(self):
        from ZvitOUT import app, sys
        sys.exit(app.exec())

    def load_filters_data(self):
        from connect_to_db import pd, dbConnection
        self.cath_sub.clear()
        subjects = pd.read_sql("SELECT TITLE "
                               "FROM SUBJECT "
                               "ORDER BY TITLE", dbConnection)
        for i in range(len(subjects)):
            self.cath_sub.addItem(f'{subjects.loc[i]["TITLE"]}')
            self.teach_sub.addItem(f'{subjects.loc[i]["TITLE"]}')
        self.cath_per.clear()
        periods = pd.read_sql("SELECT TITLE, YEAR "
                              "FROM REPORT_PERIOD "
                              "ORDER BY YEAR", dbConnection)
        for i in range(len(periods)):
            self.cath_per.addItem(f'{periods.loc[i]["TITLE"]} {periods.loc[i]["YEAR"]}')
            self.teach_period.addItem(f'{periods.loc[i]["TITLE"]} {periods.loc[i]["YEAR"]}')
        self.teach_teacher.clear()
        teachers = pd.read_sql("SELECT SURNAME, NAME, PATRONIMYC "
                               "FROM TEACHER "
                               "ORDER BY SURNAME", dbConnection)
        for i in range(len(teachers)):
            self.teach_teacher.addItem \
                (f'{teachers.loc[i]["SURNAME"]} {teachers.loc[i]["NAME"]} {teachers.loc[i]["PATRONIMYC"]}')
        self.teach_rep_type.clear()
        types = pd.read_sql("SELECT TYPE_NAME "
                            "FROM REPORT_TYPE ", dbConnection)
        for i in range(len(types)):
            self.teach_rep_type.addItem(f'{types.loc[i]["TYPE_NAME"]}')

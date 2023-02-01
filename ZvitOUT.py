import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5 import QtGui
from connect_to_db import *


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("UIs/authorization.ui", self)
        self.label_2.setScaledContents(True)
        self.teachlogin.clicked.connect(self.go_to_teach_login)
        self.adminlogin.clicked.connect(self.go_to_admin_login)
        self.settings.clicked.connect(self.go_validate_settings)

    def go_validate_settings(self):
        pop = ValidateSettings(self)
        pop.show()

    def go_to_teach_login(self):
        teach_login = LoginScreenTeacher()
        widget.addWidget(teach_login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_admin_login(self):
        admin_login = LoginScreenAdmin()
        widget.addWidget(admin_login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Settings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("UIs/settings.ui", self)
        self.setFixedSize(640, 470)
        self.cancel.clicked.connect(self.close)
        self.approve.clicked.connect(self.validate_connection)

    def validate_connection(self):
        try:
            db_host = self.host.text()
            db_user = self.user.text()
            db = self.database.text()
            db_password = self.dbpassword.text()
            connection = setup_connection(db_host, db_user, db, db_password)
            if connection.open:
                with open('settings/connection_settings.json', 'r') as f:
                    data = json.load(f)
                    data["con_settings"]["host"] = db_host
                    data["con_settings"]["user"] = db_user
                    data["con_settings"]["database"] = db
                    data["con_settings"]["password"] = db_password
                with open('settings/connection_settings.json', 'w') as f:
                    json.dump(data, f, indent=3)
                self.warning.setText('Налаштування збережено.')
        except:
            self.warning.setText('Неможливо встановити підключення до бази даних.')


class ValidateSettings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi("UIs/settings_auth.ui", self)
        self.setFixedSize(431, 311)
        self.cancel.clicked.connect(self.close)
        self.approve.clicked.connect(self.validation)

    def validation(self):
        data = self.safety_password.text()
        if not data:
            self.wrong_password.setText('Поле не може бути пустим')
        elif data != '1111':
            self.wrong_password.setText('Неправильний пароль')
        else:
            self.close()
            settings = Settings(self)
            settings.show()


class LoginScreenTeacher(WelcomeScreen):
    def __init__(self):
        super(LoginScreenTeacher, self).__init__()
        loadUi("UIs/authorization_teacher.ui", self)
        self.valid_query = "SELECT TEACHER_PASSWORD "\
                           "FROM ADMIN"
        self.key = "TEACHER_PASSWORD"
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.teacherlogin.clicked.connect(self.validation)
        self.teacherback.clicked.connect(self.go_back_main)
        self.settings.clicked.connect(self.go_validate_settings)

    def validation(self):
        from connect_to_db import pd, dbConnection
        password = self.password.text()
        result = pd.read_sql(self.valid_query, dbConnection)
        if not password:
            self.warning.setText('Не заповнене поле для паролю!')
        elif self.key == "TEACHER_PASSWORD" and password != result.loc[0]["TEACHER_PASSWORD"]\
             or self.key == "ADMIN_PASSWORD" and password != result.loc[0]["ADMIN_PASSWORD"]:
            self.warning.setText('Неправильний пароль!')
            self.password.setText('')
        else:
            if self.key == "TEACHER_PASSWORD":
                self.go_teacher_panel()
           # elif self.key == "ADMIN_PASSWORD":
           #     self.go_panel()

    def go_panel(self):
        panel = Panel(self.key, self.index)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_teacher_panel(self):
        import teacher_report
        panel = teacher_report.TeacherReport(widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_back_main(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreenAdmin(LoginScreenTeacher):
    def __init__(self):
        super(LoginScreenAdmin, self).__init__()
        loadUi("UIs/authorization_admin.ui", self)
        self.key = "ADMIN_PASSWORD"
        self.valid_query = "SELECT ADMIN_PASSWORD FROM ADMIN"
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
     #   self.login.clicked.connect(self.validation)
        self.adminback.clicked.connect(self.go_back_main)
        self.settings.clicked.connect(self.go_validate_settings)


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(900)
widget.setFixedWidth(1400)
widget.setWindowTitle("Звіт OUT")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("UIs/images/school.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")
from sqlalchemy import create_engine
import pymysql
import pandas as pd

sqlEngine = create_engine('mysql+pymysql://reportbd_usr:0v7uh3K5nK19I6ir@45.145.52.129/reportbd', pool_recycle=3600)
dbConnection = sqlEngine.connect()
frame = pd.read_sql("SELECT REPORT_PERIOD.TITLE, REPORT_PERIOD.YEAR, "
                        "TEACHER.SURNAME, TEACHER.NAME, TEACHER.PATRONIMYC, "
                        "CLASS.NUMBER, CLASS.LETTER, "
                        "SUBJECT.TITLE, "
                        "REPORT_TYPE.TYPE_NAME, "
                        "REPORT.STUDENTS_A, REPORT.STUDENTS_B, REPORT.STUDENTS_C, "
                        "REPORT.STUDENTS_D, REPORT.N_A, REPORT.NAMES, CLASS.QUANTITY "
                        "FROM REPORT_PERIOD, TEACHER, CLASS, SUBJECT, REPORT_TYPE, REPORT "
                        "WHERE REPORT_PERIOD.ID = REPORT.ID_REPORT_PERIOD and TEACHER.ID = REPORT.ID_TEACHER and "
                        "CLASS.ID = REPORT.ID_CLASS and SUBJECT.ID = REPORT.ID_SUBJECT and "
                        "REPORT_TYPE.ID = REPORT.ID_REPORT_TYPE "
                        "ORDER BY NUMBER, LETTER, SUBJECT.TITLE, SURNAME", dbConnection)
pd.set_option('display.expand_frame_repr', False)
print(frame)
dbConnection.close()

"""
           teacher_id = self.teacher.currentText().split()
           classes = self.classes.currentText()
           letters = self.letters.currentText()
           subject = self.subject.currentText()
           rt = self.types.currentText()
           S_A = self.a.text()
           S_B = self.b.text()
           S_C = self.c.text()
           S_D = self.d.text()
           N_A = self.n.text()
           names = self.surnames.text()
           all_pupils = pd.read_sql("SELECT QUANTITY "
                                    "FROM CLASS "
                                    "WHERE NUMBER = %s AND LETTER = %s AND STATUS = 1",
                                    dbConnection, params=[int(classes), letters])
           suma = int(S_A) + int(S_B) + int(S_C) + int(S_D) + int(N_A)
           is_divide = pd.read_sql("SELECT DIVIDE "
                                   "FROM SUBJECT "
                                   "WHERE TITLE = %s",
                                   dbConnection, params=[subject])
           if suma != all_pupils.loc[0]["QUANTITY"] and not is_divide.loc[0]["DIVIDE"]:
               self.all.setText(str(suma))
               self.all_pupils.setText(str(on_list))
               self.notquantity.setText('Кількість учнів не співпадає.')
           else:
               # rewrite query

           #    self.error.setText('Звіт успішно додано.')
    #   except:
    #       self.error.setText('Не вдалось додати звіт.')"""

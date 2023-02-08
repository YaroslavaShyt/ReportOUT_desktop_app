import pandas as pd
from fpdf import FPDF, HTMLMixin
from connect_to_db import *


class HTML2PDF(FPDF, HTMLMixin):
    pass


def get_info_teachers(subject_title, period_title):
    subject_id = pd.read_sql("SELECT ID FROM SUBJECT WHERE TITLE = %s", dbConnection, params=[subject_title]).loc[0]["ID"]
    period_id = pd.read_sql("SELECT ID FROM REPORT_PERIOD WHERE TITLE = %s AND YEAR = %s", dbConnection,
                               params=[' '.join(period_title.split()[0:-1]), period_title.split()[-1]]).loc[0]["ID"]
    reports = pd.read_sql("SELECT SURNAME, NAME, PATRONIMYC, CATEGORY, DEGREE, EXPERIENCE, "
                    "STUDENTS_D, STUDENTS_C, STUDENTS_B, STUDENTS_A "
                    "FROM REPORT "
                    "INNER JOIN TEACHER ON REPORT.ID_TEACHER = TEACHER.ID "
                    "WHERE ID_SUBJECT = %s AND ID_REPORT_PERIOD = %s", dbConnection, params=[subject_id, period_id])
    teachers = {}
    for i in range(len(reports)):
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'] = [None, None, None, [], [], [], []]
    for i in range(len(reports)):
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][0] = reports.loc[i]["CATEGORY"]
        degree = reports.loc[i]["DEGREE"]
        if reports.loc[i]["DEGREE"] == 'вчитель-методист':
            degree = 'вч.-мет'
        elif reports.loc[i]["DEGREE"] == 'старший вчитель':
            degree = 'ст.вчит'
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][1] = degree
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][2] = reports.loc[i]["EXPERIENCE"]
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][3].append(reports.loc[i]["STUDENTS_D"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][4].append(reports.loc[i]["STUDENTS_C"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][5].append(reports.loc[i]["STUDENTS_B"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][6].append(reports.loc[i]["STUDENTS_A"])
    result = []
    for i in teachers:
        result.append(
            [i, teachers[i][0], teachers[i][1], teachers[i][2], sum(teachers[i][3]), sum(teachers[i][4]),
             sum(teachers[i][5]), sum(teachers[i][6])])
    return result


def getCathedraData(subject_title, period_title):
    subject_id = pd.read_sql("SELECT ID FROM SUBJECT WHERE TITLE = %s", dbConnection, params=[subject_title]).loc[0]["ID"]
    period_id = pd.read_sql("SELECT ID FROM REPORT_PERIOD WHERE TITLE = %s AND YEAR = %s", dbConnection,
                            params=[' '.join(period_title.split()[0:-1]), period_title.split()[-1]]).loc[0]["ID"]
    reports = pd.read_sql("SELECT SURNAME, NAME, PATRONIMYC, STUDENTS_A, STUDENTS_B, STUDENTS_C, STUDENTS_D, N_A, QUANTITY "
                          "FROM REPORT "
                          "INNER JOIN TEACHER ON REPORT.ID_TEACHER = TEACHER.ID "
                          "INNER JOIN CLASS ON REPORT.ID_CLASS = CLASS.ID "
                          "WHERE REPORT.ID_SUBJECT = %s AND REPORT.ID_REPORT_PERIOD = %s AND "
                          "REPORT.ID_REPORT_TYPE = %s",
                          dbConnection, params=[subject_id, period_id, 1])
    teachers = {}
    for i in range(len(reports)):
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'] = [[], [], [], [], []]
    for i in range(len(reports)):
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][0].append(reports.loc[i]["STUDENTS_A"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][1].append(reports.loc[i]["STUDENTS_B"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][2].append(reports.loc[i]["STUDENTS_C"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][3].append(reports.loc[i]["STUDENTS_D"])
        teachers[f'{reports.loc[i]["SURNAME"]} {reports.loc[i]["NAME"][0]}. {reports.loc[i]["PATRONIMYC"][0]}.'][4].append(reports.loc[i]["N_A"])
    result = []
    for i in teachers:
        result.append([i, sum(teachers[i][0]), sum(teachers[i][1]), sum(teachers[i][2]), sum(teachers[i][3]),
                       sum(teachers[i][4])])
    return result


def get_classes_data(subject_title, period_title):
    subject_id = pd.read_sql("SELECT ID FROM SUBJECT WHERE TITLE = %s", dbConnection, params=[subject_title]).loc[0]["ID"]
    period_id = pd.read_sql("SELECT ID FROM REPORT_PERIOD WHERE TITLE = %s AND YEAR = %s",
                            dbConnection,
                            params=[' '.join(period_title.split()[0:-1]), period_title.split()[-1]]).loc[0]["ID"]
    reports = pd.read_sql("SELECT NUMBER, LETTER, STUDENTS_A, STUDENTS_B, STUDENTS_C, STUDENTS_D, N_A "
                          "FROM REPORT "
                          "INNER JOIN CLASS ON REPORT.ID_CLASS = CLASS.ID "
                          "WHERE REPORT.ID_SUBJECT = %s AND REPORT.ID_REPORT_PERIOD = %s",
                          dbConnection,
                          params=[subject_id, period_id])
    classes = {}
    for i in range(len(reports)):
        classes[f'{reports.loc[i]["NUMBER"]}'] = [[], [], [], [], []]
    for i in range(len(reports)):
        classes[f'{reports.loc[i]["NUMBER"]}'][0].append(reports.loc[i]["STUDENTS_A"])
        classes[f'{reports.loc[i]["NUMBER"]}'][1].append(reports.loc[i]["STUDENTS_B"])
        classes[f'{reports.loc[i]["NUMBER"]}'][2].append(reports.loc[i]["STUDENTS_C"])
        classes[f'{reports.loc[i]["NUMBER"]}'][3].append(reports.loc[i]["STUDENTS_D"])
        classes[f'{reports.loc[i]["NUMBER"]}'][4].append(reports.loc[i]["N_A"])
    result = []
    for i in classes:
        result.append(
            [i, sum(classes[i][0]), sum(classes[i][1]), sum(classes[i][2]),
             sum(classes[i][3]), sum(classes[i][4])])
    return result


def get_classesTeacher_data(subject_title, period_title, teacher, report_type):
    subject_id = pd.read_sql("SELECT ID FROM SUBJECT WHERE TITLE = %s", dbConnection, params=[subject_title]).loc[0]["ID"]
    period_id = pd.read_sql("SELECT ID FROM REPORT_PERIOD WHERE TITLE = %s AND YEAR = %s", dbConnection,
                            params=[' '.join(period_title.split()[0:-1]), period_title.split()[-1]]).loc[0]["ID"]
    teacher_id = pd.read_sql("SELECT ID FROM TEACHER WHERE SURNAME = %s AND NAME = %s AND PATRONIMYC = %s", dbConnection,
                             params=[teacher.split()[0], teacher.split()[1], teacher.split()[2]]).loc[0]["ID"]
    report_type_id = pd.read_sql("SELECT ID FROM REPORT_TYPE WHERE TYPE_NAME = %s", dbConnection,
                                 params=[report_type]).loc[0]["ID"]
    reports = pd.read_sql("SELECT NUMBER, LETTER, STUDENTS_A, STUDENTS_B, STUDENTS_C, STUDENTS_D, N_A, NAMES "
                          "FROM REPORT "
                          "INNER JOIN CLASS ON REPORT.ID_CLASS = CLASS.ID "
                          "WHERE REPORT.ID_SUBJECT = %s AND REPORT.ID_REPORT_PERIOD = %s "
                          "AND REPORT.ID_TEACHER = %s AND REPORT.ID_REPORT_TYPE = %s",
                          dbConnection,
                          params=[subject_id, period_id, teacher_id, report_type_id])
    classes = {}
    for i in range(len(reports)):
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'] = [[], [], [], [], [], []]
    for i in range(len(reports)):
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][0].append(reports.loc[i]["STUDENTS_A"])
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][1].append(reports.loc[i]["STUDENTS_B"])
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][2].append(reports.loc[i]["STUDENTS_C"])
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][3].append(reports.loc[i]["STUDENTS_D"])
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][4].append(reports.loc[i]["N_A"])
        classes[f'{reports.loc[i]["NUMBER"]}-{reports.loc[i]["LETTER"]}'][5].append(reports.loc[i]["NAMES"])
    result = []
    for i in classes:
        result.append(
            [i, sum(classes[i][0]), sum(classes[i][1]), sum(classes[i][2]),
             sum(classes[i][3]), sum(classes[i][4]), classes[i][5]])
    return result


def getPdfTeacherTable(subject_title, period_title, teacher, report_type):
    teacherData = get_classesTeacher_data(subject_title, period_title, teacher, report_type)

    pdf = HTML2PDF(orientation='L', unit='mm', format='A4')
    pdf.add_font("Sans", style="", fname="Noto_Sans/NotoSans-Regular.ttf")
    pdf.add_font("Sans", style="B", fname="Noto_Sans/NotoSans-Bold.ttf")
    pdf.set_font("Sans", size=12)

    pdf.add_page()
    # header
    pdf.cell(278, 10, 'Комунальний заклад "Вінницький ліцей №32"', border=0, align='C')
    pdf.ln()
    pdf.cell(278, 10, f'Результативність за {period_title.split()[0]} {period_title.split()[1]} {period_title.split()[2]}-{int(period_title.split()[2]) + 1}',
             border=0, align='C')
    pdf.ln()
    pdf.cell(278, 10,
             f'вчитель: {teacher.split()[0]} {teacher.split()[1][0]}. {teacher.split()[2][0]}., предмет: {subject_title}',
             border=0, align='C')
    pdf.ln()
    pdf.multi_cell(18, 20, 'Клас', border=1, align='C', new_x='RIGHT', new_y='LAST')
    pdf.set_font("Sans", size=9)
    pdf.multi_cell(20, 10, 'К-ть учнів, що навч-ся', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'високий рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'достатній рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'середній рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'початковий рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, 'н/а', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 20, '% якості', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(16, 10, '% успіш- ності', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(44, 20, 'неатестовані', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    #
    # rows
    i = 0
    allLevel = 0
    levelA = 0
    levelB = 0
    levelC = 0
    levelD = 0
    levelE = 0

    for item in teacherData:
        i = i + 1
        allPupils = item[1] + item[2] + item[3] + item[4] + item[5]
        allLevel += allPupils
        levelA += item[1]
        levelB += item[2]
        levelC += item[3]
        levelD += item[4]
        levelE += item[5]
        pdf.set_font("Sans", size=11)
        pdf.multi_cell(18, 8, item[0], border=1, align='C', new_x='RIGHT', new_y='LAST')
        pdf.multi_cell(20, 8, str(allPupils), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(item[1]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[1] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[2]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[2] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[3]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[3] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[4]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[4] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[5]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[5] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(20, 8, str(round((item[1] + item[2]) / allPupils * 100, 1)) + '%', border=1, align='C',
                       new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(16, 8, str(round((item[1] + item[2] + item[3]) / allPupils * 100, 1)) + '%', border=1, align='C',
                       new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(44, 8, ', '.join(item[6]), border=1, align='C', new_x='LMARGIN', new_y='NEXT')
        # All

    pdf.set_font("Sans", size=11)
    pdf.multi_cell(18, 8, 'Всього', border=1, align='C', new_x='RIGHT', new_y='LAST')
    pdf.multi_cell(20, 8, str(allLevel), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelA), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelA / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelB), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelB / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelC), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelC / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelD), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelD / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelE), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelE / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 8, str(round((levelA + levelB) / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                   new_y='TOP')
    pdf.multi_cell(16, 8, str(round((levelA + levelB + levelC) / allLevel * 100, 1)) + '%', border=1, align='C',
                   new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(44, 8, '', border=1, align='L', new_x='LMARGIN', new_y='NEXT')
    # ======Footer=======

    #    pdf.write_html(table)
    pdf.output(f'{subject_title}-{teacher.split()[0]} {teacher.split()[1][0]}. {teacher.split()[2][0]}.pdf')


def getPdfAnaliticsTable(subject_title, period_title, title):
    cathedraData = getCathedraData(subject_title, period_title)

    pdf = HTML2PDF(orientation='L', unit='mm', format='A4')
    pdf.add_font("Sans", style="", fname="Noto_Sans/NotoSans-Regular.ttf")
    pdf.add_font("Sans", style="B", fname="Noto_Sans/NotoSans-Bold.ttf")
    pdf.set_font("Sans", size=12)

    pdf.add_page()
    # header
    pdf.cell(278, 10,
             f'Аналітична таблиця результативності з  {title} за {period_title.split()[0]} {period_title.split()[1]} {period_title.split()[2]}-{int(period_title.split()[2]) + 1}',
             border=1, align='C')
    pdf.ln()
    pdf.multi_cell(10, 20, '№', border=1, align='C', new_x='RIGHT', new_y='LAST')
    pdf.multi_cell(52, 20, 'П.І.Б вчителів катедри', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.set_font("Sans", size=9)
    pdf.multi_cell(20, 10, 'К-ть учнів, що навч-ся', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'високий рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'достатній рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'середній рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 10, 'початковий рівень', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, 'н/а', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 20, '% якості', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(16, 20, 'рейтинг', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    #
    # rows
    i = 0
    allLevel = 0
    levelA = 0
    levelB = 0
    levelC = 0
    levelD = 0
    levelE = 0

    for item in cathedraData:
        i = i + 1
        allPupils = item[1] + item[2] + item[3] + item[4] + item[5]
        allLevel += allPupils
        levelA += item[1]
        levelB += item[2]
        levelC += item[3]
        levelD += item[4]
        levelE += item[5]
        pdf.set_font("Sans", size=10)
        pdf.multi_cell(10, 8, str(i), border=1, align='C', new_x='RIGHT', new_y='LAST')
        pdf.multi_cell(52, 8, item[0], border=1, align='L', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(20, 8, str(allPupils), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(item[1]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[1] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[2]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[2] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[3]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[3] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[4]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[4] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[5]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[5] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(20, 8, str(round((levelA + levelB) / allLevel * 100, 1)) + '%', border=1, align='C',
                       new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(16, 8, '', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
        # All

    pdf.set_font("Sans", size=10)
    pdf.multi_cell(10, 8, '', border=1, align='C', new_x='RIGHT', new_y='LAST')
    pdf.multi_cell(52, 8, 'Всього', border=1, align='L', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 8, str(allLevel), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelA), border=1, align='C', new_x='RIGHT', new_y='TOP')
    print('allLevel', allLevel)
    pdf.multi_cell(14, 8, str(round(levelA / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelB), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelB / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelC), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelC / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelD), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelD / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 8, str(levelE), border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 8, str(round(levelE / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 8, str(round((levelA + levelB) / allLevel * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                   new_y='TOP')
    pdf.multi_cell(16, 8, '', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    # ======Footer=======
    classData = get_classes_data(subject_title, period_title)
    for item in classData:
        allClass = item[1] + item[2] + item[3] + item[4] + item[5]
        pdf.set_font("Sans", size=10)
        if int(item[0]) in [5, 6, 9, 10, 11]:
            ending = '-ті'
        else:
            ending = '-мі'
        pdf.multi_cell(10, 8, '', border=1, align='C', new_x='RIGHT', new_y='LAST')
        pdf.multi_cell(52, 8, str(item[0]) + ending, border=1, align='L', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(20, 8, str(allClass), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(item[1]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[1] / allClass * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[2]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[2] / allClass * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[3]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[3] / allClass * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[4]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[4] / allClass * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(18, 8, str(item[5]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(round(item[5] / allClass * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(20, 8, str(round((levelA + levelB) / allLevel * 100, 1)) + '%', border=1, align='C',
                       new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(16, 8, '', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    print(period_title)
    #    pdf.write_html(table)
    pdf.output(f'analytics.{title}-{period_title.split()[0]}.{period_title.split()[2]}-{int(period_title.split()[2]) + 1}.pdf')


def getPdfResultsTable(subject_title, period_title, title):
    cathedraData = get_info_teachers(subject_title, period_title)

    pdf = HTML2PDF(orientation='L', unit='mm', format='A4')
    pdf.add_font("Sans", style="", fname="Noto_Sans/NotoSans-Regular.ttf")
    pdf.add_font("Sans", style="B", fname="Noto_Sans/NotoSans-Bold.ttf")
    pdf.set_font("Sans", size=12)

    pdf.add_page()
    # header
    pdf.cell(278, 10,
             f'Результати навчальних досягнень з  {title} за {period_title.split()[0]} {period_title.split()[1]} {period_title.split()[2]}-{int(period_title.split()[2]) + 1}',
             border=1, align='C')
    pdf.ln()
    pdf.multi_cell(10, 20, '№', border=1, align='C', new_x='RIGHT', new_y='LAST')
    pdf.multi_cell(52, 20, 'П.І.Б вчителів катедри', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.set_font("Sans", size=9)
    pdf.multi_cell(20, 20, 'Категорія', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, 'Звання', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, 'Стаж', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, 'К-ть уч.', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, 'поч', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, 'сер', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, 'дост', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(18, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(14, 20, 'вис', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(20, 20, '%', border=1, align='C', new_x='RIGHT', new_y='TOP')
    pdf.multi_cell(16, 20, 'рейтинг', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    #
    # rows
    i = 0
    for item in cathedraData:
        i = i + 1
        allPupils = item[4] + item[5] + item[6] + item[7]
        pdf.set_font("Sans", size=10)
        pdf.multi_cell(10, 8, str(i), border=1, align='C', new_x='RIGHT', new_y='LAST')
        pdf.multi_cell(52, 8, item[0], border=1, align='L', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(20, 8, item[1], border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, item[2], border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(item[3]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(allPupils), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(14, 8, str(item[4]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(round(item[4] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(14, 8, str(item[5]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(round(item[5] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(14, 8, str(item[6]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(18, 8, str(round(item[6] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(14, 8, str(item[7]), border=1, align='C', new_x='RIGHT', new_y='TOP')
        pdf.multi_cell(20, 8, str(round(item[7] / allPupils * 100, 1)) + '%', border=1, align='C', new_x='RIGHT',
                       new_y='TOP')
        pdf.multi_cell(16, 8, '', border=1, align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.output(f'result.{title}-{period_title.split()[0]}.{period_title.split()[2]}-{int(period_title.split()[2]) + 1}.pdf')

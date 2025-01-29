from conf.database import session
from conf.models import *
from sqlalchemy import func, desc, and_, select


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01():
    result = session.query(Students.name, func.round(func.avg(GradesBook.grade), 2).label('avg_grade')) \
        .select_from(GradesBook).join(Students).group_by(Students.id).order_by(desc('avg_grade')).limit(5).all()

    return result

    # Знайти студента із найвищим середнім балом з певного предмета.
def select_02():
    result = session.query(Students.name, func.round(func.avg(GradesBook.grade), 2).label("best_avg_student")) \
        .select_from(GradesBook).join(Students).filter(GradesBook.subject_id == 4) \
        .group_by(Students.id).order_by(desc("best_avg_student")).limit(1).all()

    return result


#    Знайти середній бал у групах з певного предмета.
def select_03():
    result = session.query(Groups.group_name, func.round(func.avg(GradesBook.grade), 2).label("group_avg")) \
        .select_from(GradesBook).join(Students, GradesBook.student_id == Students.id) \
        .join(Groups, Students.group_id == Groups.id) \
        .filter(GradesBook.subject_id == 2).group_by(Groups.group_name).order_by("group_avg").all()

    return result

    # Знайти середній бал на потоці (по всій таблиці оцінок).
def select_04():
    result = session.query(func.round(func.avg(GradesBook.grade), 2).label("avg_grade")) \
        .select_from(GradesBook).all()

    return result

    # Знайти які курси читає певний викладач.
def select_05():
    result = session.query(Subjects.subject, Teachers.name).select_from(TeacherSubjects) \
        .join(Subjects, TeacherSubjects.subject_id == Subjects.id) \
        .join(Teachers, TeacherSubjects.teacher_id == Teachers.id).filter(Teachers.id == 3).all()

    return result

    # Знайти список студентів у певній групі.
def select_06():
    result = session.query(Students.name).select_from(Students).join(Groups).filter(Groups.id == 2).all()

    return result

    # Знайти оцінки студентів у окремій групі з певного предмета.
def select_07():
    result = session.query(Students.name, GradesBook.grade).select_from(Students).join(Groups).join(GradesBook) \
        .filter(Groups.id == 2, GradesBook.subject_id == 3).all()

    return result

    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_08():
    result = session.query(Subjects.subject, func.round(func.avg(GradesBook.grade), 2).label("teacher_avg_grade")) \
        .select_from(GradesBook).join(Subjects, GradesBook.subject_id == Subjects.id).filter(
        GradesBook.teacher_id == 3).group_by(Subjects.subject).order_by("teacher_avg_grade").all()

    return result

    # Знайти список курсів, які відвідує студент.
def select_09():
    result = session.query(Subjects.subject).select_from(Subjects).join(GradesBook) \
        .filter(GradesBook.student_id == 26).distinct().all()

    return result

    # Список курсів, які певному студенту читає певний викладач.
def select_10():
    result = session.query(Subjects.subject).select_from(TeacherSubjects) \
        .join(Subjects, TeacherSubjects.subject_id == Subjects.id) \
        .join(StudentSubjects, Subjects.id == StudentSubjects.subject_id) \
        .filter(StudentSubjects.student_id == 3, TeacherSubjects.teacher_id == 3) \
        .group_by(Subjects.subject).all()

    return result

    # Середній бал, який певний викладач ставить певному студентові.
def select_11():
    result = session.query(func.round(func.avg(GradesBook.grade), 2).label("avg_by_t_to_s")) \
                .select_from(GradesBook).join(Students, GradesBook.student_id == Students.id) \
                .join(Teachers, GradesBook.teacher_id == Teachers.id).filter(Students.id == 4, Teachers.id == 2) \
                .order_by("avg_by_t_to_s").all()

    return result

    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    subquery = (select(func.max(GradesBook.date)).join(Students)
                .filter(and_(GradesBook.subject_id == 4, Students.group_id == 2))).scalar_subquery()
    result = session.query(Students.name, GradesBook.grade, GradesBook.date).select_from(GradesBook) \
        .join(Students).filter(Subjects.id == 4, Groups.id == 2, GradesBook.date == subquery).all()

    return result


if __name__ == "__main__":
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_11())
    print(select_12())


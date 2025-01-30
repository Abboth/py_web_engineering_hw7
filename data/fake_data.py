from faker import Faker
import logging
from datetime import timedelta, date
from random import randint, choice
from conf.database import session
from conf.models import Students, GradesBook, Teachers, TeacherSubjects, StudentSubjects, Groups, Subjects

logging.basicConfig(level=logging.INFO)

fake = Faker()

subjects = [("Algebra",), ("Biology",), ("Drawing",), ("Chemistry",), ("Geography",), ("Geometry",),
            ("History",), ("Literature",), ("Mathematics",), ("Music",), ("Physical education",),
            ("Physics",), ("Technology",), ("Physical education",)]

with session:
    def fake_students():
        try:
            for _ in range(randint(30, 40)):
                student = Students(
                    name=fake.name(),
                    group_id=randint(1, 4))
                session.add(student)
            session.commit()
            logging.info("Students table fulfilled with data successfully")
        except Exception as e:
            logging.error(f"Error occurred while inserting data into Students: {e}")
            session.rollback()
            raise e


    def fake_teachers():
        try:
            for i in range(randint(4, 5)):
                teacher = Teachers(
                    name=fake.name())
                session.add(teacher)
            session.commit()
            logging.info("Teachers table fulfilled with data successfully")
        except Exception as e:
            logging.error(f"Error occurred while inserting data into Teachers: {e}")
            session.rollback()
            raise e


    def add_subjects():
        try:
            for subject in subjects:
                subj = Subjects(
                    subject=subject)
                session.add(subj)
            session.commit()
            logging.info("Subject table fulfilled with data successfully")
        except Exception as e:
            logging.error(f"Error occurred while inserting data into Subjects: {e}")
            session.rollback()
            raise e


    def teach_subj_associations():
        try:
            teachers_count = session.query(Teachers).count()
            for i in range(len(subjects)):
                teacher_subject = TeacherSubjects(
                    teacher_id=randint(1, teachers_count),
                    subject_id=i + 1)
                session.add(teacher_subject)
            session.commit()
            logging.info("Association of teachers and subjects created successfully")
        except Exception as e:
            logging.error(f"Error occurred while creating associations of subjects and teachers: {e}")
            session.rollback()
            raise e


    def student_subj_associations():
        try:
            students_count = len(session.query(Students).all())
            for student in range(students_count):
                student_subj = set()

                while len(student_subj) < 6:
                    random_subject = randint(1, len(subjects))
                    if random_subject not in student_subj:
                        student_subj.add(random_subject)
                        student_subject = StudentSubjects(
                            student_id=student + 1,
                            subject_id=random_subject
                        )
                        session.add(student_subject)
            session.commit()
            logging.info("Association of students and subjects created successfully")
        except Exception as e:
            logging.error(f"Error occurred while creating associations of subjects and students: {e}")
            session.rollback()
            raise e


    def fake_grades():
        try:
            students_count = len(session.query(Students).all())
            teachers_count = len(session.query(Teachers).all())

            for student in range(students_count):
                student_grades_count = []
                target_grades_count = randint(15, 20)
                while len(student_grades_count) < target_grades_count:
                    teacher_id = randint(1, teachers_count)
                    get_joint_subjects = session.query(Subjects.id).select_from(TeacherSubjects) \
                        .join(Subjects, TeacherSubjects.subject_id == Subjects.id) \
                        .join(StudentSubjects, Subjects.id == StudentSubjects.subject_id) \
                        .filter(StudentSubjects.student_id == student + 1,
                                TeacherSubjects.teacher_id == teacher_id) \
                        .group_by(Subjects.id).all()

                    if not get_joint_subjects:
                        continue
                    grade = randint(1, 5)
                    date_of_grade = date.today() - timedelta(days=randint(0, 365))
                    grade_book = GradesBook(
                        student_id=student + 1,
                        subject_id=choice(get_joint_subjects)[0],
                        grade=grade,
                        date=date_of_grade,
                        teacher_id=teacher_id
                    )
                    student_grades_count.append(grade)
                    session.add(grade_book)
            session.commit()
            logging.info("Grades book fulfilled with data successfully")

        except Exception as e:
            logging.error(f"Error occurred while inserting data into GradesBook: {e}")
            session.rollback()
            raise e


    def fake_groups():
        try:
            for i in range(4):
                group = Groups(
                    group_name=f"Group #{i + 1}")
                session.add(group)
            session.commit()
            logging.info("Groups table fulfilled with data successfully")
        except Exception as e:
            logging.error(f"Error occurred while inserting data into Groups: {e}")
            session.rollback()
            raise e


def main():
    add_subjects()
    fake_groups()
    fake_teachers()
    fake_students()
    teach_subj_associations()
    student_subj_associations()
    fake_grades()


if __name__ == "__main__":
    main()

from conf.database import session
from conf.models import *
from data.fake_data import subjects
from random import randint
import logging
from conf.models import Students



def add_data(obj, **kwargs):
    try:
        if obj.__name__ == "Students" and "group_id" in kwargs:
            group_id = kwargs.pop("group_id")
            group = session.query(Groups).get(group_id)
            if not group:
                raise ValueError(f"Group with id={group_id} not found.")
            kwargs["group"] = group

            new_student = obj(**kwargs)
            session.add(new_student)
            session.flush()

            student_subj = set()
            subjects_count = session.query(Subjects).count()

            while len(student_subj) < 6:
                random_subject = randint(1, subjects_count)
                if random_subject not in student_subj:
                    student_subj.add(random_subject)
                    student_subject = StudentSubjects(
                        student_id=new_student.id,
                        subject_id=random_subject
                    )
                    session.add(student_subject)

            session.commit()
            logging.info(f"To {obj.__name__}'s added record for {new_student.name}")
        elif obj.__name__ == "Teachers":

            new_teacher = obj(**kwargs)
            session.add(new_teacher)
            session.flush()

            count_of_subjects = randint(1, 3)
            for i in range(count_of_subjects):
                teacher_subject = TeacherSubjects(
                    teacher_id=new_teacher.id,
                    subject_id=i + 1)
                session.add(teacher_subject)

            session.commit()
            logging.info(f"To {obj.__name__}'s added record: {new_teacher.name}")
    except Exception as e:
        logging.error(f"Error occurred while adding data: {e}")
        session.rollback()
        raise e


def data_update(obj, obj_id: str, **kwargs) -> None:
    record = session.query(obj).get(obj_id)
    try:
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        logging.info(f"Data for {obj.__name__} updated")
    except ValueError as e:
        logging.error(f"Error occurred while updating data for {obj.__name__}: {e}")
        session.rollback()
        raise e


def remove_record(obj, obj_id):
    record = session.query(obj).get(obj_id)

    try:
        session.delete(record)
        session.commit()
        logging.info(f"{obj.__name__} with ID {obj_id} removed successfully")
    except ValueError as e:
        logging.error(f"Error occurred while removing {obj.__name__}: {e}")
        session.rollback()
        raise e

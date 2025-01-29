from conf.database import session
from conf.models import *
import logging

objects_dict = {"teacher": Teachers, "subject": Subjects, "student": Students, "group": Groups}


def find_all(obj) -> str:
    print("i start to fetch data")
    result = session.query(obj).all()
    print("i finished fetching data")
    return result


def find_teacher(obj, obj_id: int) -> tuple:

    try:
        result = session.query(obj.id, obj.name).filter(obj.id == obj_id).all()
        return result
    except ValueError:
        logging.error(f"Invalid ID: {obj_id}")


def find_student(obj, obj_id: int) -> tuple:

    try:
        result = session.query(obj.id, obj.name, Students.group_id).filter(obj.id == obj_id).all()
        return result
    except ValueError:
        logging.error(f"Invalid ID: {obj_id}")


def find_group_members(obj, obj_id: str) -> str:
    try:
        expression = session.query(obj.id, obj.group_name, Students.name).join(Students).filter(
            obj.id == obj_id).all()
        result = ""
        for record in expression:
            students = ""
            for student in expression:
                students += f"{student[2]}, "
            result += f"Group id {record[0]}, group name {record[1]} members: {students}"
            break

        return result
    except ValueError:
        logging.error(f"Group with ID - {obj_id} not exist")



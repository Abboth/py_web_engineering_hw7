from conf.database import session
from conf.models import *
import logging


def add_data(obj, **kwargs):
    try:
        if obj.__name__ == "Student" and "group_id" in kwargs:
            group_id = kwargs.pop("group_id")
            group = session.query(Groups).get(group_id)
            if not group:
                raise ValueError(f"Group with id={group_id} not found.")
            kwargs["group"] = group

        new_record = obj(**kwargs)
        session.add(new_record)
        session.commit()
        logging.info(f"{obj.__name__} added record: {new_record}")
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

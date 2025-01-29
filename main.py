import logging
import argparse
from crud_expressions.update_data import *
from crud_expressions.search_data import *

objects_dict = {"teacher": Teachers, "subject": Subjects, "student": Students, "group_id": Groups, "members": Groups}

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="managing of database")
    parser.add_argument("--action", "-a", required=True,
                        choices="create, update, delete, remove, list, find",
                        help="action: create, list, update, remove")
    parser.add_argument("--model", "-m", required=True, choices=objects_dict.keys(),
                        help="models: teacher, subject, student, group_id, members")

    parser.add_argument("--id", type=int)
    parser.add_argument("--name", "-n", type=str)
    parser.add_argument("--group_id", "-g", type=int)

    args = parser.parse_args()
    model = objects_dict[args.model]

    try:
        if model:
            if args.action == "create":
                if args.model == "student":
                    add_data(model, name=args.name, group_id=args.group_id)
                else:
                    add_data(model, name=args.name)

            elif args.action == "list":
                print(find_all(model))
            elif args.action == "find":
                if args.model == "student":
                    print(find_student(model, args.id))

                elif args.model == "members":
                    print(find_group_members(model, args.id))

                elif args.model == "teacher":
                    print(find_teacher(model, args.id))

            elif args.action == "update":
                if not args.id:
                    logging.info("ID needed to update")
                    return
                if args.model == "student":
                    data_update(model, args.id, name=args.name, group=args.group)
                else:
                    data_update(model, args.id, name=args.name)

            elif args.action == "remove":
                if not args.id:
                    logging.error("ID needed to remove")
                    return
                remove_record(model, args.id)
    except ValueError as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    main()

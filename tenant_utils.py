import argparse
import subprocess


def do_task(db_name, task):
    # return subprocess.run(f"python manage.py {task} --database={db_name}", shell=True)
    try:
        if task == "dumpdata":
            print(f"Performing {task} on {db_name}")
            task = subprocess.run(
                f"python3 tenant_context_manage.py {db_name} {task} --database={db_name} --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > ./db_dump/{db_name}.json",
                shell=True,
            )
            return task

        if task == "loaddata":
            print(f"Performing {task} on {db_name}")
            # subprocess.run(f"python manage.py shell --command='from django.contrib.contenttypes.models import ContentType; ContentType.objects.using(\"{db_name}\").all().delete();'",shell=True)
            task = subprocess.run(
                f"python3 manage.py {task} --database={db_name} ./db_dump/{db_name}.json",
                shell=True,
            )
            print(task)
            return task

        else:
            print(f"Performing {task} on {db_name}")
            return subprocess.run(
                f"python3 tenant_context_manage.py {db_name}  {task} --database={db_name}",
                shell=True,
            )
    except Exception:
        import traceback

        return "Unexpected error:", traceback.format_exc()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Helper for tenant task")

    parser.add_argument(
        "-d",
        "--database",
        metavar="",
        dest="database",
        type=str,
        required=False,
        help="database name",
    )

    parser.add_argument(
        "-t",
        "--task",
        metavar="",
        dest="task",
        required=True,
        type=str,
        help="task to be done. e.g flush, migrate, createsuperuser, dumpdata, loaddb",
    )

    args = parser.parse_args()

    if args.database == None:
        db = [
            "test",
            # "janasewagas",
            # "janasewakirana",
            # "babajagdishowr",
            # "dipshikaoil",
            # "mashantitrade",
            # "skgaurishankaroil",
            # "syasekalikaoil",
            # "bhawanisuppliers",
            # "ghanist",
            # "shreedeep",
            # "tiwarihardware",
            # "psgas",
            # "skmotors",
            # "siddhibinayak",
            # "jbgas",
            # "jagatradevi",
            # "jaymalika",
        ]
        for db_name in db:
            result = do_task(db_name, args.task)
    else:
        result = do_task(args.database, args.task)

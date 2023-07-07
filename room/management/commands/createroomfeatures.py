from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.db import DEFAULT_DB_ALIAS

from companyinfo.models import CompanyInfo
from room.models import RoomFeature


class Command(BaseCommand):
    help = "Create Room Service"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".',
        )
        parser.add_argument("--branchid", default=1, help="Branch id")

    def handle(self, *args: Any, **options: Any) -> str | None:
        if not options["branchid"]:
            raise CommandError("Branch Id is missing.")

        database = options["database"]

        try:
            branch = CompanyInfo.objects.using(database).get(
                id=int(options["branchid"])
            )
        except CompanyInfo.DoesNotExist:
            raise CommandError("Branch with given branch id doesnot exist")

        features = [
            "Feature 1",
            "Feature 2",
            "Feature 3",
        ]

        for feature in features:
            try:
                RoomFeature.objects.using(database).create(name=feature, branch=branch)
            except:
                raise CommandError(
                    "Could not create room features due to unknown error"
                )

        self.stdout.write(self.style.SUCCESS("Room features created successfully"))

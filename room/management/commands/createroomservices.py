from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.db import DEFAULT_DB_ALIAS

from companyinfo.models import CompanyInfo
from room.models import RoomService


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
            raise CommandError("value for 'branchid' is given.")

        database = options["database"]

        try:
            branch = CompanyInfo.objects.using(database).get(
                id=int(options["branchid"])
            )
        except CompanyInfo.DoesNotExist:
            raise CommandError("Branch with given branch id doesnot exist")

        services = [
            "Service 1",
            "Service 2",
            "Service 3",
        ]

        for service in services:
            try:
                RoomService.objects.using(database).create(name=service, branch=branch)
            except:
                raise CommandError(
                    "Could not create room services due to unknown error"
                )

        self.stdout.write(self.style.SUCCESS("Room services created successfully"))

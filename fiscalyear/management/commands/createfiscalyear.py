from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.db import IntegrityError
from fiscalyear.models import FiscalYear
from fiscalyear.utils import fiscal_year_generator


class Command(BaseCommand):
    help = "Create Fiscal Year"

    def add_arguments(self, parser: CommandParser) -> None:
        return parser.add_argument("--fiscalyear", help="Add given fiscal year")

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            if options["fiscalyear"]:
                FiscalYear.objects.create(
                    fiscal_year=options["fiscalyear"], is_active=True
                )
            else:
                FiscalYear.objects.create(
                    fiscal_year=fiscal_year_generator(), is_active=True
                )

            self.stdout.write(self.style.SUCCESS("Fiscal year created successfully"))
        except IntegrityError:
            raise CommandError("Same fiscal year already exist")
        except:
            raise CommandError("Could not create fiscal year due to unknown error")

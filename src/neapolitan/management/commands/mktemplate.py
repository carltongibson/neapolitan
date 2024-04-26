import shutil
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import TemplateDoesNotExist, get_template
from django.template.engine import Engine
from django.apps import apps

class Command(BaseCommand):
    help = "Bootstrap a CRUD template for a model, copying from the active neapolitan default templates."

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            type=str,
            help="The <app_name.ModelName> to bootstrap a template for.",
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-l",
            "--list",
            action="store_const",
            const="list",
            dest="role",
            help="List role",
        )
        group.add_argument(
            "-d",
            "--detail",
            action="store_const",
            const="detail",
            dest="role",
            help="Detail role",
        )
        group.add_argument(
            "-c",
            "--create",
            action="store_const",
            const="form",
            dest="role",
            help="Create role",
        )
        group.add_argument(
            "-u",
            "--update",
            action="store_const",
            const="form",
            dest="role",
            help="Update role",
        )
        group.add_argument(
            "-f",
            "--form",
            action="store_const",
            const="form",
            dest="role",
            help="Form role",
        )
        group.add_argument(
            "--delete",
            action="store_const",
            const="delete",
            dest="role",
            help="Delete role",
        )

    def handle(self, *args, **options):
        model = options["model"]
        role = options["role"]

        if role == "list":
            suffix = "_list.html"
        elif role == "detail":
            suffix = "_detail.html"
        elif role == "form":
            suffix = "_form.html"
        elif role == "delete":
            suffix = "_confirm_delete.html"

        app_name, model_name = model.split(".")
        template_name = f"{app_name}/{model_name.lower()}{suffix}"
        neapolitan_template_name = f"neapolitan/object{suffix}"

        # Check if the template already exists.
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            # Get the filesystem path of neapolitan's object template.
            neapolitan_template = get_template(neapolitan_template_name)
            neapolitan_template_path = neapolitan_template.origin.name

            # Find target directory.
            # 1. If  f"{app_name}/templates" exists, use that.
            # 2. Otherwise, use first project level template dir.
            app_config = apps.get_app_config(app_name)
            target_dir = f"{app_config.path}/templates"
            if not Path(target_dir).exists():
                try:
                    target_dir = Engine.get_default().template_dirs[0]
                except (ImproperlyConfigured, IndexError):
                    raise CommandError(
                        "No app or project level template dir found."
                    )
            # Copy the neapolitan template to the target directory with template_name.
            shutil.copyfile(neapolitan_template_path, f"{target_dir}/{template_name}")
        else:
            self.stdout.write(
                f"Template {template_name} already exists. Remove it manually if you want to regenerate it."
            )
            raise CommandError("Template already exists.")

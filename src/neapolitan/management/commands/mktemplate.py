import shutil
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import TemplateDoesNotExist, get_template
from django.template.engine import Engine
from django.apps import apps
from django.conf import settings


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
        group.add_argument(
            "--all",
            action="store_const",
            const="all",
            dest="role",
            help="Generate all CRUD templates (list, detail, form, delete)",
        )

    def handle(self, *args, **options):
        model = options["model"]
        role = options["role"]

        # Handle --all option
        if role == "all":
            roles = ["list", "detail", "form", "delete"]
            for r in roles:
                options["role"] = r
                try:
                    self._handle_single_template(*args, **options)
                except CommandError as e:
                    # Continue with other templates even if one exists
                    if "already exists" in str(e):
                        continue
                    else:
                        raise
            return

        # Handle single template
        self._handle_single_template(*args, **options)

    def _handle_single_template(self, *args, **options):
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
                    # FIX: Access DIRS from the template settings instead of template_dirs
                    template_settings = settings.TEMPLATES[0]
                    if template_settings.get('DIRS'):
                        target_dir = template_settings['DIRS'][0]
                    else:
                        # No project-level template dir, so create app-level templates
                        target_dir = f"{app_config.path}/templates"
                except (ImproperlyConfigured, IndexError, KeyError):
                    # Fallback to creating app-level templates
                    target_dir = f"{app_config.path}/templates"

            # Ensure the full directory path exists
            target_path = Path(target_dir) / Path(template_name).parent
            target_path.mkdir(parents=True, exist_ok=True)

            # Copy the neapolitan template to the target directory with template_name.
            shutil.copyfile(neapolitan_template_path, f"{target_dir}/{template_name}")
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created template: {target_dir}/{template_name}")
            )
        else:
            self.stdout.write(
                f"Template {template_name} already exists. Remove it manually if you want to regenerate it."
            )
            raise CommandError("Template already exists.")
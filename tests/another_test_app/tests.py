import os

from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

APP_ROOT = Path(__file__).parent
PROJECT_ROOT = APP_ROOT.parent

class MktemplateCommandTest(TestCase):
    def test_mktemplate_command_with_project_template_dir(self):
        # Run the command
        call_command("mktemplate", "another_test_app.IceCream", "--list")

        # Check if the file was created
        file_path = PROJECT_ROOT / "templates/another_test_app/icecream_list.html"
        self.assertTrue(os.path.isfile(file_path))

        # Remove the created file
        os.remove(file_path)

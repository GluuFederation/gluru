#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

sys.path.append('app')
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

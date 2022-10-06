"""
This file provides zest.releaser entrypoints using when releasing new
django-countries versions.
"""
import os
import re
import shutil

from django.core.management import call_command
from txclib.commands import cmd_pull  # type: ignore
from txclib.log import logger  # type: ignore
from txclib.utils import find_dot_tx  # type: ignore
from zest.releaser.utils import ask, execute_command  # type: ignore

import django_countries


def translations(data) -> None:
    if data["name"] != "django-countries":
        return

    if not ask("Pull translations from transifex and compile", default=True):
        return

    _handlers = logger.handlers
    logger.handlers = []
    try:
        cmd_pull(argv=["-a", "--minimum-perc=60"], path_to_tx=find_dot_tx())
    finally:
        logger.handlers = _handlers
    _cwd = os.getcwd()
    os.chdir(os.path.dirname(django_countries.__file__))
    try:
        call_command("compilemessages")
        execute_command(["git", "add", "locale"])
    finally:
        os.chdir(_cwd)


if __name__ == "__main__":
    translations({"name": "django-countries"})

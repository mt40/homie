#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys

from google.auth.exceptions import DefaultCredentialsError

logger = logging.getLogger(__name__)

def _setup_cloud_debugger():
    try:
        import googleclouddebugger
        googleclouddebugger.enable(
            breakpoint_enable_canary=True
        )
    except DefaultCredentialsError as error:
        logger.error(str(error))


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homie.settings.local')
    logger.warning(f"DJANGO_SETTINGS_MODULE={os.environ['DJANGO_SETTINGS_MODULE']}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    _setup_cloud_debugger()
    main()

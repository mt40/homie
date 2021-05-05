#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import logging
from google.auth.exceptions import DefaultCredentialsError


logger = logging.getLogger(__name__)


def main():
    # for GCP Cloud Debugger
    try:
        import googleclouddebugger
        googleclouddebugger.enable(
            breakpoint_enable_canary=True
        )
    except ImportError:
        pass
    except DefaultCredentialsError as error:
        logger.error(str(error))

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homie.settings.local')
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
    main()

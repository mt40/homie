#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from google.auth.exceptions import DefaultCredentialsError


def _setup_cloud_logging():
    """
    See https://cloud.google.com/logging/docs/setup/python#using_the_python_root_logger
    """

    # Imports the Cloud Logging client library
    import google.cloud.logging

    try:
        # Instantiates a client
        client = google.cloud.logging.Client()

        # Retrieves a Cloud Logging handler based on the environment
        # you're running in and integrates the handler with the
        # Python logging module. By default this captures all logs
        # at INFO level and higher
        client.get_default_handler()
        client.setup_logging()
    except DefaultCredentialsError as error:
        print(str(error))


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
    _setup_cloud_logging()
    import logging
    logger = logging.getLogger(__name__)

    _setup_cloud_debugger()
    main()

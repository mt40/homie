import os

from google.cloud import secretmanager

PROJECT_ID = os.environ['PROJECT_ID']


def get_latest(secret_id: str, prefer_env: bool = True) -> str:
    if prefer_env:
        if secret_id in os.environ:
            return os.environ[secret_id]
        return get_latest(secret_id, prefer_env=False)

    return _access_secret_version(PROJECT_ID, secret_id, "latest")


def _access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").

    Notes:
        This function authenticates with GCP using credential of the default service
        account of App Engine. This credential is provided automatically IN App Engine.
        Therefore, if you want to run this in external environment (e.g. locally), you
        have to set variable GOOGLE_APPLICATION_CREDENTIALS to the path of json key file.
    """
    # Create the Secret Manager client.
    # Credential is automatically provided by App Engine
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    return payload

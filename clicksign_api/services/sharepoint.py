from pathlib import Path
from urllib.parse import quote

import msal
import requests

from clicksign_api.config import (
    SHAREPOINT_HOSTNAME,
    SHAREPOINT_SITE_PATH,
    SHAREPOINT_DRIVE_NAME,
    SHAREPOINT_FILE_PATH,
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
)

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0/"
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]

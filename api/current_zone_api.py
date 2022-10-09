import requests
import logging
from jsonschema import validate

logger = logging.getLogger("api")


class CurrentZone:
    def __init__(self, url):
        self.url = url

    def current_zone(self, zone, schema: dict):
        """
        https://timeapi.io/api/Time/current/zone?timeZone=
        """
        response = requests.get(f"{self.url}{zone}")
        validate(instance=response.json(), schema=schema)
        logger.info(response.text)
        return response

    def invalid_zone(self, zone):
        """
        https://timeapi.io/api/Time/current/zone?timeZone=
        """
        response = requests.get(f"{self.url}{zone}")
        assert isinstance(response.json(), str)
        logger.info(response.text)
        return response

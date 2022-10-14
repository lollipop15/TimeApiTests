import requests
import logging
import allure
from jsonschema import validate

logger = logging.getLogger("api")


class CurrentZone:
    def __init__(self, url):
        self.url = url

    def current_zone(self, zone, schema: dict):
        """
        The function makes a GET request https://timeapi.io/api/Time/current/zone?timeZone= with the specified valid
        timeZone and checks that a valid JSON response has been returned.
        :param zone: the zone in which to get the time.
        :param schema: JSON response validation scheme.
        :return: response.
        """
        with allure.step("Sending a GET request, getting a response"):
            response = requests.get(f"{self.url}{zone}")

        with allure.step("JSON schema validation"):
            validate(instance=response.json(), schema=schema)

        logger.info(response.text)
        return response

    def invalid_zone(self, zone):
        """
        The function makes a GET request https://timeapi.io/api/Time/current/zone?timeZone= with the specified invalid
        timeZone and checks that an error message was returned in str format.
        :param zone: the zone in which to get the time.
        :return: response.
        """

        with allure.step("Sending a GET request, getting a response"):
            response = requests.get(f"{self.url}{zone}")

        with allure.step("Checking that an error message was returned in str format"):
            assert isinstance(response.json(), str)

        logger.info(response.text)
        return response

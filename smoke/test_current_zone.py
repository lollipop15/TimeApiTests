import pytest
import allure
from datetime import datetime, timedelta
import pytz
import calendar
from helper.help_functions import is_dst
from schemas.current_zone import valid_schema
from api.current_zone_api import CurrentZone

URL = "https://timeapi.io/api/Time/current/zone?timeZone="


class TestCurrentZone:
    """
    This class is designed to test the GET /api/Time/current/zone method (https://timeapi.io/swagger/index.html).
    The method gets the current time of the time zone.
    """

    @allure.feature('TestCurrentZone')
    @allure.story('test_valid_current_zone')
    @pytest.mark.parametrize("zone",
                             ["Europe/Amsterdam", "Africa/Lagos", "America/Toronto", "Pacific/Auckland",
                              "Asia/Shanghai", "Atlantic/Faroe", "Australia/Sydney", "Indian/Maldives"])
    def test_valid_current_zone(self, zone):
        """
        A function to check the 200 response code and the correctness of the returned fields.
        :param zone: the zone in which to get the time.
        """

        with allure.step("Sending a GET request, getting a response, and checking the response code"):
            response = CurrentZone(url=URL).current_zone(zone=zone, schema=valid_schema)
            assert response.status_code == 200

        with allure.step("Convert the received datetime, time and date from str to datetime format"):
            res_json = response.json()
            response_datetime = datetime.strptime(res_json.get('dateTime')[:-1], '%Y-%m-%dT%H:%M:%S.%f')
            response_date = datetime.strptime(res_json.get('date'), '%m/%d/%Y')
            response_time = datetime.strptime(res_json.get('time'), '%H:%M')

        with allure.step("Using pytz and datetime.now(), we get the date and time in the desired time zone and convert "
                         "them to the format '%Y-%m-%d %H:%M:%S.%f'"):
            cur_zone = pytz.timezone(zone)
            cur_zone_datetime = datetime.strptime(datetime.now(cur_zone).strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                  '%Y-%m-%d %H:%M:%S.%f')

        with allure.step("Checking that the difference between the dates received using the GET request and the python "
                         "libraries is no more than 10 seconds"):
            assert (response_datetime - cur_zone_datetime) <= timedelta(seconds=10)

        with allure.step("Checking that the data from the request is logically correct and matches each other"):
            assert res_json.get('year') == response_datetime.year == response_date.year
            assert res_json.get('month') == response_datetime.month == response_date.month
            assert res_json.get('day') == response_datetime.day == response_date.day
            assert res_json.get('hour') == response_datetime.hour == response_time.hour
            assert res_json.get('minute') == response_datetime.minute == response_time.minute
            assert res_json.get('seconds') == response_datetime.second
            assert res_json.get('milliSeconds') == response_datetime.microsecond // 1000
            assert res_json.get('timeZone') == zone
            assert res_json.get('dayOfWeek') == calendar.day_name[cur_zone_datetime.weekday()]
            assert res_json.get('dstActive') == is_dst(cur_zone_datetime, zone)

    @allure.story('test_invalid_current_zone')
    @pytest.mark.parametrize("zone",
                             ["Europe/Amsterd", ""])
    def test_invalid_current_zone(self, zone):
        """
        A function to check the 400 response code and the correctness of error message.
        :param zone: the zone in which to get the time.
        """

        with allure.step("Sending a GET request, getting a response, and checking the response code"):
            response = CurrentZone(url=URL).invalid_zone(zone=zone)
            assert response.status_code == 400

        with allure.step("Checking the error message"):
            assert response.json() in ["Invalid Timezone", "Missing Timezone"]


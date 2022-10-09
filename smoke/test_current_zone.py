import requests
import pytest
from datetime import datetime, timedelta
import pytz
import calendar
from helper.help_functions import is_dst
from schemas.current_zone import valid_schema
from api.current_zone_api import CurrentZone

URL = "https://timeapi.io/api/Time/current/zone?timeZone="


class TestCurrentZone:
    @pytest.mark.parametrize("zone",
                             ["Europe/Amsterdam", "Africa/Lagos", "America/Toronto", "Pacific/Auckland",
                              "Asia/Shanghai", "Atlantic/Faroe", "Australia/Sydney", "Indian/Maldives"])
    def test_current_zone_europe_amsterdam(self, zone):
        cur_zone = pytz.timezone(zone)
        cur_zone_datetime = datetime.strptime(datetime.now(cur_zone).strftime('%Y-%m-%d %H:%M:%S.%f'),
                                              '%Y-%m-%d %H:%M:%S.%f')
        response = CurrentZone(url=URL).current_zone(zone=zone, schema=valid_schema)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/json; charset=utf-8"

        response_datetime = datetime.strptime(response.json().get('dateTime')[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        assert (response_datetime - cur_zone_datetime) <= timedelta(seconds=10)

        response_date = datetime.strptime(response.json().get('date'), '%m/%d/%Y')
        response_time = datetime.strptime(response.json().get('time'), '%H:%M')

        assert response.json().get('year') == response_datetime.year == response_date.year
        assert response.json().get('month') == response_datetime.month == response_date.month
        assert response.json().get('day') == response_datetime.day == response_date.day
        assert response.json().get('hour') == response_datetime.hour == response_time.hour
        assert response.json().get('minute') == response_datetime.minute == response_time.minute
        assert response.json().get('seconds') == response_datetime.second
        assert response.json().get('milliSeconds') == response_datetime.microsecond // 1000
        assert response.json().get('timeZone') == zone
        assert response.json().get('dayOfWeek') == calendar.day_name[cur_zone_datetime.weekday()]
        assert response.json().get('dstActive') == is_dst(cur_zone_datetime, zone)

        print(response.text)

    @pytest.mark.parametrize("zone",
                             ["Europe/Amsterd", ""])
    def test_invalid_zone(self, zone):
        response = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterd")
        assert response.status_code == 400
        assert response.json() == "Invalid Timezone"


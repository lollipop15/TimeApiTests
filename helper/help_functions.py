from datetime import datetime
import pytz
import allure


def is_dst(dt=None, timezone="UTC"):
    """
    The function checks for daylight savings time or not in the timezone.
    :param dt: date and time in the timezone in datetime format.
    :param timezone: timezone.
    :return: True or False.
    """

    with allure.step("If the date and time are not transferred, then we take the current UTC date"):
        if dt is None:
            dt = datetime.utcnow()

    with allure.step("In the specified timezone, we get the date, taking into aware the timezone"):
        timezone = pytz.timezone(timezone)
        timezone_aware_date = timezone.localize(dt, is_dst=None)

    return timezone_aware_date.tzinfo._dst.seconds != 0
from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(
    AnonRateThrottle
):
    rate = "5/min"

class PasswordResetRateThrottle(
    AnonRateThrottle
):
    rate = "3/min"
from core.exceptions import CustomException


class ErrorGettingExchangeRateException(CustomException):
    code = 400
    error_code = "NO_EXCHANGE_RATE"
    message = "Error getting the exchange rate"

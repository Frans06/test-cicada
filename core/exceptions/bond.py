from core.exceptions import CustomException


class BondAlreadySoldException(CustomException):
    code = 400
    error_code = "BOND_ALREADY_SOLD"
    message = "bond has been sold"


class SameUserBuyException(CustomException):
    code = 400
    error_code = "SAME_USER_BUY"
    message = "You can not buy your bond"
